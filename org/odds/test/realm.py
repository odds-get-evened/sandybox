import json
import random
import string

from pgpy import PGPKey, PGPUID, PGPKeyring, PGPMessage
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm

from org.odds.util import crc32

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


class Realm:
    def __init__(self):
        self.id = 'realm_' + crc32(random.SystemRandom().randbytes(256)).decode()
        init_key = create_key(self.id)
        self.key_ring = PGPKeyring(init_key)
