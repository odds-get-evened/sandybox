import random
import string

from pgpy import PGPKey, PGPUID
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

from org.odds.test.user import RealmUser

DEFAULT_USAGE = {KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage, KeyFlags.Sign}
DEFAULT_HASHES = [HashAlgorithm.SHA256, HashAlgorithm.SHA512]
DEFAULT_CIPHERS = [SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192]
DEFAULT_COMPRESSION = [
    CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2,
    CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed
]
DEFAULT_DELIMITER = "|"


def create_key(uid: str, key_size=2048) -> PGPKey:
    k = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, key_size)
    k.add_uid(
        PGPUID.new(uid),
        usage=DEFAULT_USAGE,
        hashes=DEFAULT_HASHES,
        ciphers=DEFAULT_CIPHERS,
        compression=DEFAULT_COMPRESSION
    )

    return k


class Realm(RealmUser):
    def __init__(self):
        rand_id = ''.join(random.SystemRandom().choices(string.digits + string.ascii_letters, k=8))
        super().__init__(uid='realm_' + rand_id)
