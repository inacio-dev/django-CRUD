import json
import datetime
import decimal

from django.core.cache import cache
from django.conf import settings
from django_redis import get_redis_connection

CACHE_TTL = getattr(settings, "CACHE_TTL", 60 * 15)


class CacheManager:
    def __init__(self):
        self.redis = get_redis_connection("default")

    def set(self, key, value, tags=[], timeout=CACHE_TTL):
        try:
            serialized_value = json.dumps(value, default=self.default_serializer)

            cache.set(key, serialized_value, timeout)

            for tag in tags:
                tag_key = f"tag:{tag}"
                self.redis.sadd(tag_key, key)
                self.redis.expire(tag_key, timeout)
        except Exception:
            pass

    def get(self, key):
        try:
            value = cache.get(key)
            if value is not None:
                value = json.loads(value)
            return value
        except Exception:
            return None

    def delete(self, key):
        try:
            cache.delete(key)
            keys_to_remove = self.redis.keys("tag:*")
            for tag_key in keys_to_remove:
                self.redis.srem(tag_key, key)
        except Exception:
            pass

    def delete_by_tags(self, tags):
        try:
            for tag in tags:
                tag_key = f"tag:{tag}"

                keys = self.redis.smembers(tag_key)

                for key in keys:
                    key_str = key.decode("utf-8")
                    cache.delete(key_str)
                    self.redis.srem(tag_key, key_str)
                self.redis.delete(tag_key)
        except Exception:
            pass

    @staticmethod
    def default_serializer(obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")
