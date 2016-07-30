import os

from slacker import Slacker


class _SlackApiClient(object):
    def __init__(self, token: str):
        self._slack = Slacker(token)

    def get_channels(self) -> list:
        return self._slack.channels.list().body['channels']

    def get_channel(self, channel_id: str) -> dict:
        return self._slack.channels.info(channel_id).body['channel']

    def get_history(self, channel_id: str, count=200, **kwargs) -> list:
        return self._slack.channels.history(channel_id, count=count, **kwargs).body['messages']

    def get_users(self) -> list:
        return self._slack.users.list().body['members']

    def get_user(self, user_id) -> dict:
        return self._slack.users.info(user_id).body['user']

    def get_bot_info(self, bot_id: str) -> list:
        return self._slack.bots.info(bot_id).body["bot"]


token = os.environ['API_KEY']
if not token:
    raise Exception('Slack Api Key required')

slack_api_client = _SlackApiClient(token)
