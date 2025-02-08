import os

import yaml
from cryptography.fernet import Fernet


class Config():

    def __init__(self,
                 config_file=os.path.join(os.environ['HOME'], '.config',
                                          'k16s', 'config.yaml')):
        self.config_dir = os.path.dirname(config_file)
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.config_file = config_file
        if not os.path.exists(self.config_file):
            self.write_default_config()
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f.read())

    def write_default_config(self):
        key = Fernet.generate_key()
        config = {'key': key.decode()}
        with open(self.config_file, 'w') as f:
            yaml.safe_dump(config, f)

    def get_key(self):
        return self.config['key']
