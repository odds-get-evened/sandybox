import random
import sys
import time
import warnings
from hashlib import sha256

import cryptography.utils
from pgpy import PGPKey, PGPMessage, PGPSignature
from pgpy.types import SignatureVerification

from org.odds.test.realm import Realm, RealmUser, DEFAULT_DELIMITER
from org.odds.util import crc32

# lousy warnings from PGPy need to get the fuck out!!! fuckin shit-dev!
warnings.filterwarnings("ignore", category=cryptography.utils.CryptographyDeprecationWarning, module="pgpy")
warnings.filterwarnings("ignore", category=UserWarning, module="pgpy")


def main():
    realm = Realm()
    user1 = RealmUser()

    # share public keys and make sure they are signed and verified before usage
    user1.key_ring.load(realm.get_encryption_key())
    realm.key_ring.load(user1.get_encryption_key())

    # user knocks: sends encrypted message to realm
    secret_msg = PGPMessage.new("i want in, please")
    # sign before encryption
    secret_sig = user1.key.sign(secret_msg)
    payload = None
    with user1.key_ring.key(realm.id) as enc_1_key:  # get user's public key for realm sending
        payload = {
            'signature': secret_sig.__str__(),
            'message': enc_1_key.encrypt(secret_msg, user=realm.id).__str__()
        }

    '''
    user initiates interaction with realm by sending a secret, and when realm successfully
    decrypts, and verifies message signature, realm will send back a new signed message with
    a hash of the user's initial message joined with a random token (as a message) 
    (i.e hash([original message]:[random token]:[timestamp])). this will be signed
    and encrypted to be passed back to user. one more round back to realm from the user to 
    confirm matching hashes. this will be the authorization check
    '''
    answered_door = False
    msg1 = None
    if payload is not None:
        with realm.key_ring.key(realm.id) as dec_1_key:
            dec1 = dec_1_key.decrypt(PGPMessage.from_blob(payload['message']))
            msg1 = dec1.message
            with realm.key_ring.key(user1.id) as sig_check_pub:
                valid_msg: SignatureVerification = sig_check_pub.verify(msg1, PGPSignature.from_blob(
                    payload['signature'])).__bool__()
                if valid_msg:
                    # success
                    answered_door = True
                    print(f"verified and decrypted: `{msg1}`")

    token_payload = None
    if answered_door is True and msg1 is not None:
        re_msg1 = ("%.3f" % (time.time()) + DEFAULT_DELIMITER + msg1 + DEFAULT_DELIMITER + crc32(random.randbytes(256))
                   .decode())
        msg1_token: str = sha256(re_msg1.encode()).hexdigest()
        print(msg1_token)
        token_msg: PGPMessage = PGPMessage.new(msg1_token)

        with realm.key_ring.key(realm.id) as sig_2_key:
            user1_pub_key: PGPKey = sig_2_key
            token_sig: PGPSignature = user1_pub_key.sign(token_msg)
            token_payload = {
                'signature': token_sig.__str__(),
                'message': user1_pub_key.encrypt(token_msg, user=user1.id).__str__()
            }

    # verify that hashes match
    if token_payload is not None:
        # decrypt message from realm containing our token
        with user1.key_ring.key(user1.id) as user1_priv_key:
            u1_priv_key: PGPKey = user1_priv_key
            dec_token: PGPMessage = u1_priv_key.decrypt(PGPMessage.from_blob(token_payload['message']))
            msg_token = dec_token.message
            with user1.key_ring.key(realm.id) as token_check_pub:
                token_pub: PGPKey = token_check_pub
                valid_token: SignatureVerification = token_pub.verify(
                    msg_token,
                    PGPSignature.from_blob(token_payload['signature'])
                )

                if valid_token.__bool__():
                    print(msg_token)
                    print()

    sys.exit(0)


def main2():
    realm = Realm()


if __name__ == "__main__":
    # main()
    main2()
