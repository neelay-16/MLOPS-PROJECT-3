import redis
import json
import os

class RedisFeatureStore:
    def __init__(self, host=None, port=None, db=0):
        # Use environment variables with defaults
        self.host = host or os.getenv("REDIS_HOST", "redis")  # Default to 'redis' for Docker
        self.port = port or int(os.getenv("REDIS_PORT", "6379"))
        self.db = db

        self.client = redis.StrictRedis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

    # Storing row by row
    def store_features(self, entity_id, features):
        key = f"entity:{entity_id}:features"
        self.client.set(key, json.dumps(features))

    # Getting row one by one
    def get_features(self, entity_id):
        key = f"entity:{entity_id}:features"
        features = self.client.get(key)
        if features:
            return json.loads(features)
        return None
    
    def store_batch_features(self, batch_data):
        for entity_id, features in batch_data.items():
            self.store_features(entity_id, features)

    def get_batch_features(self, entity_ids):
        batch_features = {}
        for entity_id in entity_ids:
            batch_features[entity_id] = self.get_features(entity_id)
        return batch_features
    
    def get_all_entity_ids(self):
        keys = self.client.keys('entity:*:features')
        ### entity entity_id feature
        entity_ids = [key.split(':')[1] for key in keys]
        return entity_ids