import redis
from dotenv import load_dotenv
import os
load_dotenv()

redis_connection = redis.from_url(os.environ.get('REDIS_URL'))
