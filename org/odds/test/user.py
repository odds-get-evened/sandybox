import random

from pgpy import PGPKey, PGPKeyring

from org.odds.test.realm import Realm, create_key
from org.odds.util import crc32


class RealmUser:
    def __init__(self, auth: Realm, uid: str = None):
        self.realm = auth
        self.current_public_key = None
        self.id: str = uid if uid is not None else crc32(random.randbytes(256)).decode()
        self.key: PGPKey = create_key(self.id)
        # add initial key to keyring
        self.keyring = PGPKeyring(self.key)

    def knock(self, msg):
        pass
