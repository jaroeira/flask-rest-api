import hashlib
import os



def generate_random_hash() -> str:
    random_data = os.urandom(32)
    hash_object = hashlib.sha256(random_data)
    random_hash = hash_object.hexdigest()
    return random_hash