import os
import hashlib
import hmac
import binascii


class PasswordHasher:
    SALT_SIZE = 16
    ITERATIONS = 100000
    ALGORITHM = "sha256"

    @staticmethod
    def hash_password(password: str) -> str:
        salt = os.urandom(PasswordHasher.SALT_SIZE)
        pwd_hash = hashlib.pbkdf2_hmac(
            PasswordHasher.ALGORITHM,
            password.encode(),
            salt,
            PasswordHasher.ITERATIONS
        )
        return binascii.hexlify(salt + pwd_hash).decode()

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        stored_bytes = binascii.unhexlify(stored_password.encode())
        salt = stored_bytes[:PasswordHasher.SALT_SIZE]
        stored_hash = stored_bytes[PasswordHasher.SALT_SIZE:]

        new_hash = hashlib.pbkdf2_hmac(
            PasswordHasher.ALGORITHM,
            provided_password.encode(),
            salt,
            PasswordHasher.ITERATIONS
        )

        return hmac.compare_digest(stored_hash, new_hash)