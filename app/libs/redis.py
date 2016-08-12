import json
import os

from redis import StrictRedis
from emitter import Emitter


# TODO use message pack instead of json serializing

class RedisService(StrictRedis):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flushall()
        self.emitter = Emitter({'client': self})

    def get_list(self, name: str, slack_func: callable, *args, **kwargs):
        result = self.lrange(name, 0, -1)
        if result:
            return [json.loads(item) for item in result]
        result = slack_func(*args, **kwargs)
        self.lpush(name, *[json.dumps(item) for item in result])
        self.ltrim(name, 0, 500)
        return result

    def get_hash_item(self, name: str, key: str, slack_func: callable, **kwargs):
        """self
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
        self.hset(name, key, json.dumps(result))
        return result

host = os.environ.get('REDIS_HOST', 'localhost')
port = os.environ.get('REDIS_PORT', '6379')
redis = RedisService(host=host, port=port, decode_responses=True)

