import json
from collections import defaultdict
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
        self._last_request = defaultdict(int, {channel: 0 for channel in channels.keys()})

        redis_client.hmset('users', users)
        redis_client.hmset('channels', channels)
        for channel_id in channels:
            redis_client.hget_or_slack('messages', channel_id, slack_api_client.get_history)

    def get_messages(self, channel: str) -> list:
        channel_id = self.get_channel_ids_by_name()[channel]
        channels = self.get_channel_ids_by_name()

        # Slack request if 15 minutes passed
        last_request = self._last_request[channel_id] + 15 * MINUTE
        current_ts = datetime.now().timestamp()
        oldest = current_ts if last_request < current_ts else None
        messages = redis_client.hget_or_slack('messages', channel_id,
                                              slack_api_client.get_history, oldest=oldest)

        serialized_messages = []
        for message in messages:
            serialized_messages.insert(0, Message(message, _Archive.get_user, channels))
        return serialized_messages

    @staticmethod
    def get_user(user_id: str) -> dict:
        return redis_client.hget_or_slack('users', user_id, slack_api_client.get_user)

    @staticmethod
    def get_channel_ids_by_name() -> dict:
        channels = redis_client.hgetall('channels')
        return {json.loads(channel)['name']: id for id, channel in channels.items()}

archive = _Archive()
