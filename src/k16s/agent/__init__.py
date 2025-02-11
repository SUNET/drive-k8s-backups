import os
import time

import age.primitives.encrypt as AgeCrypt
from age.keys.agekey import AgePrivateKey


class Agent():
    def __init__(self, keyfile='~/.config/age/key.txt'):
        self.private_key = None
        if os.path.exists(os.path.expanduser(keyfile)):
            with open(os.path.expanduser(keyfile), 'r') as f:
                for line in f.readlines():
                    if line.startswith('AGE-SECRET-KEY-'):
                        self.private_key = AgePrivateKey.from_private_string(
                            line.strip())
                        break

        if self.private_key is None:
            self.private_key = AgePrivateKey.generate()
            strftimestr = time.strftime(
                "%Y-%m-%dT%H:%M:%S%z", time.localtime())
            keystr = f'''# created: {strftimestr}
        # public key: {self.private_key.public_key().public_string()}
        {self.private_key.private_string()}
        '''
            with open(os.path.expanduser(keyfile), 'a') as f:
                f.write(keystr)
        self.public_key = self.private_key.public_key()

    def encrypt(self, input):
        return AgeCrypt.encrypt(self.private_key.private_bytes(), input)

    def decrypt(self, input):
        return AgeCrypt.decrypt(self.private_key.private_bytes(), input)

    def public_key_string(self):
        return self.public_key.public_string()
