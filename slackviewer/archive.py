import json
from datetime import datetime
from slackviewer.message import Message
from slackviewer.redis import redis_client
from slackviewer.slack import slack_api_client
from slackviewer.util import MINUTE


class _Archive(object):
    def __init__(self):
        channels = slack_api_client.get_channels()
        channels = {channel["id"]: json.dumps(channel) for channel in channels if not channel['is_archived']}
        users = {user["id"]: json.dumps(user) for user in slack_api_client.get_users()}
        self._last_request = {}

        redis_client.hmset('users', users)
        redis_client.hmset('channels', channels)
        for channel_id in channels:
            key = channel_id + '_messages'
            redis_client.get_list(key, slack_api_client.get_history, channel_id)
            redis_client.expire(key, 15 * MINUTE)
            self._last_request[channel_id] = datetime.now().timestamp()

    def get_messages(self, channel: str) -> list:
        channel_id = self.get_channel_ids_by_name()[channel]

        # Slack request if 15 minutes passed
        last_request = self._last_request[channel_id]
        current_ts = datetime.now().timestamp()
        oldest = last_request if current_ts - last_request > 15 * MINUTE else None

        key = channel_id + '_messages'
        messages = redis_client.get_list(key, slack_api_client.get_history, channel_id, oldest=oldest)
        self._last_request[channel_id] = current_ts if oldest else last_request

        serialized_messages = []
        for message in messages:
            serialized_messages.append(Message(message, _Archive.get_user, _Archive.get_channel))
        return serialized_messages

    @staticmethod
    def get_user(user_id: str) -> dict:
        user = redis_client.get_hash_item('users', user_id, slack_api_client.get_user)
        # It's a bot
        if not user:
            user = slack_api_client.get_bot_info(user_id)
            redis_client.hset('users', user['id'], json.dumps(user))
        return user

    @staticmethod
    def get_channel(channel_id: str) -> dict:
        return redis_client.get_hash_item('channels', channel_id, slack_api_client.get_channel)

    @staticmethod
    def get_channel_ids_by_name() -> dict:
        channels = redis_client.hgetall('channels')
        return {json.loads(channel)['name']: id for id, channel in channels.items()}

archive = _Archive()
