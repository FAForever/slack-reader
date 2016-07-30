import json

from redis import StrictRedis


class _RedisClient(StrictRedis):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flushall()

    def hget_or_slack(self, name: str, key: str, slack_func: callable, **kwargs):
        """
        Retrieves value from redis, if retrieval is a miss or expired then
        it will fetch from the slack callback
        :param name: Redis store name
        :param key: key to value
        :param slack_func: Slack api callback
        :return: Appropriate result
        """
        result = self.hget(name, key)
        if result:
            return json.loads(result)
        result = slack_func(key, **kwargs)
        redis_client.hset(name, key, json.dumps(result))
        return result

redis_client = _RedisClient(host='redis', decode_responses=True)
