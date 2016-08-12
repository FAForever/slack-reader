import logging
import os
import time
from threading import Thread

import sys
from slackclient import SlackClient

from .. import socketio


class SlackService(Thread):
    def __init__(self, token: str):
        super().__init__()
        self._slack = SlackClient(token)
        self._connection = None
        self._ignored_events = ['reconnect_url']

    def run(self):
        self._connection = self._slack.rtm_connect()
        if not self._connection:
            raise ConnectionError('Failed to connect to Slack RTM session')

        ping_counter = time.time()
        logging.info('Starting slack RTM connection')
        while True:
            for event in self._slack.rtm_read():
                if event:
                    print(event)
                    if event['type'] not in self._ignored_events:
                        socketio.emit('event', event)
            if ping_counter - time.time() > 3:
                self._slack.server.ping()
                logging.info('PING - slack', sys.stderr)
                ping_counter = time.time()

    def get_channels(self) -> list:
        return self._slack.server.channels.list().body['channels']

    def get_channel(self, channel_id: str) -> dict:
        return self._slack.server.channels.info(channel_id).body['channel']

    def get_history(self, channel_id: str, **kwargs) -> list:
        return self._slack.server.channels.history(channel_id, **kwargs).body['messages']

    def get_users(self) -> list:
        return self._slack.server.users.list().body['members']

    def get_user(self, user_id) -> dict:
        return self._slack.server.users.info(user_id).body['user']

    def get_bot_info(self, bot_id: str) -> list:
        return self._slack.server.bots.info(bot_id).body['bot']

slack = SlackService(os.environ['API_KEY'])
