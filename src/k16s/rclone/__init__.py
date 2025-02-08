import configparser


class Rclone():

    def __init__(self, config_file: str):
        config = configparser.ConfigParser()
        self.config = config
        self.config_file = config_file
        self.config.read(self.config_file)

    def get_remote(self, remote: str):
        dict_remote = {
            "type": self.config.get(remote, "type"),
            "provider": self.config.get(remote, "provider"),
            "endpoint": self.config.get(remote, "endpoint"),
            "access_key_id": self.config.get(remote, "access_key_id"),
            "secret_access_key": self.config.get(remote, "secret_access_key"),
            "acl": self.config.get(remote, "acl"),
        }
        print(dict_remote)
        return dict_remote
