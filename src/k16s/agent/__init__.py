import os
import time

import age.primitives.encrypt as AgeCrypt
from age.keys.agekey import AgePrivateKey


class Agent():
    def __init__(
            self,
            keyfile='~/.config/age/key.txt',
            db_user=None,
            db_host=None,
            db_pass=None,
            db_name=None
    ):
        self.keyfile = keyfile
        self.private_key = self.fix_private_key()
        self.public_key = self.private_key.public_key()
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_name = db_name

    def fix_private_key(self):
        private_key = None
        if os.path.exists(os.path.expanduser(self.keyfile)):
            with open(os.path.expanduser(self.keyfile), 'r') as f:
                for line in f.readlines():
                    if line.startswith('AGE-SECRET-KEY-'):
                        private_key = AgePrivateKey.from_private_string(
                            line.strip())
                        break

        if private_key is None:
            private_key = AgePrivateKey.generate()
            strftimestr = time.strftime(
                "%Y-%m-%dT%H:%M:%S%z", time.localtime())
            keystr = f'''# created: {strftimestr}
        # public key: {private_key.public_key().public_string()}
        {private_key.private_string()}
        '''
            with open(os.path.expanduser(self.keyfile), 'a') as f:
                f.write(keystr)
        return private_key

    def encrypt(self, input):
        return AgeCrypt.encrypt(self.private_key.private_bytes(), input)

    def decrypt(self, input):
        return AgeCrypt.decrypt(self.private_key.private_bytes(), input)

    def public_key_string(self):
        return self.public_key.public_string()

    def db_creds(self):
        if None in [self.db_user, self.db_pass, self.db_host, self.db_name]:
            return None
        return {
            'user': self.db_user,
            'password': self.db_pass,
            'host': self.db_host,
            'database': self.db_name,
        }
