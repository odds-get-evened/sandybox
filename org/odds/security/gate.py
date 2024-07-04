import dbm
import json
import sys
from pathlib import Path

from pgpy import PGPKey, PGPUID
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

from org.odds.util import crc32


class RealmUser:
    def __init__(self, i, s):
        self.secret = s
        self.id: bytes = i
        self.key = None

        self.gen_key()

    def gen_key(self):
        if self.key is None:
            self.key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
            uid = PGPUID.new(self.id.decode())
            self.key.add_uid(
                uid,
                usage={KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA512],
                ciphers=[SymmetricKeyAlgorithm.AES256],
                compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed]
            )


class Realm:
    REALM_ID = 'realm0'

    def __init__(self):
        self.key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
        uid = PGPUID.new(self.REALM_ID)
        self.key.add_uid(
            uid,
            usage={KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA512],
            ciphers=[SymmetricKeyAlgorithm.AES256],
            compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed]
        )

        self.db_path = Path(Path(__file__).parent, "permits")

        self.store_key(uid.name)

    def store_key(self, i):
        with dbm.open(self.db_path.__str__(), 'c') as db:
            if db.get(i) is None:
                db[i] = json.dumps({'key': self.key.__str__()})

    def user(self, u: RealmUser):
        with dbm.open(self.db_path.__str__(), 'c') as db:
            if db.get(u.id) is None:  # is not known
                # make a sub key for this user
                subkey = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
                subkey.add_uid(
                    PGPUID.new(u.id.decode()),
                    usage={KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                    hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA512],
                    ciphers=[SymmetricKeyAlgorithm.AES256],
                    compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed]
                )
                # load original realm private key from DB
                realm = json.loads(db[self.REALM_ID].decode())
                realm_key, _ = PGPKey.from_blob(realm['key'])
                # add subkey to O.G. key
                realm_key.add_subkey(subkey)
                # assign altered key to this instance
                self.key = realm_key
                # store it again
                self.store_key(self.REALM_ID)


def main():
    realm = Realm()

    is_reset = False

    if not is_reset:
        realm.user(RealmUser(crc32("user1".encode()), "secret"))

    '''
    with dbm.open(realm.db_path.__str__(), 'r') as db:
        [print(x, ": ", db[x]) for x in db]
    '''
    if is_reset:
        with dbm.open(realm.db_path.__str__(), 'c') as db:
            db.clear()


if __name__ == "__main__":
    main()
