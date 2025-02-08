import argparse

import argcomplete

from k16s.config import Config
from k16s.job import Job
from k16s.rclone import Rclone


def main():

    parser = argparse.ArgumentParser(description='K16S')
    subparser = parser.add_subparsers(dest='command')

    rclone_parser = subparser.add_parser('rclone')
    rclone_parser.add_argument('--config',
                               help='rclone config file',
                               required=True)
    rclone_parser.add_argument('--destination-remote',
                               help='Name of destination remote',
                               required=True)
    rclone_parser.add_argument('--source-remote',
                               help='Name of source remote',
                               required=True)
    rclone_parser.add_argument('--source-bucket',
                               help='name of source bucket',
                               required=True)
    rclone_parser.add_argument('--destination-bucket',
                               help='Name of destination bucket',
                               required=True)
    rclone_parser.add_argument('--key', help='Key', required=False)
    rclone_parser.add_argument('--name', help='Name of the job', required=True)

    cli_parser = subparser.add_parser('cli')
    cli_parser.add_argument('--destination-bucket',
                            help='Destination bucket',
                            required=True)
    cli_parser.add_argument('--destination-endpoint',
                            help='Destination endpoint',
                            required=True)
    cli_parser.add_argument('--destination-key',
                            help='Destination key id',
                            required=True)
    cli_parser.add_argument('--destination-secret',
                            help='Destination secret',
                            required=True)
    cli_parser.add_argument('--key', help='Key', required=False)
    cli_parser.add_argument('--name', help='Name of the job', required=True)
    cli_parser.add_argument('--source-bucket',
                            help='Source bucket',
                            required=True)
    cli_parser.add_argument('--source-endpoint',
                            help='Source endpoint',
                            required=True)
    cli_parser.add_argument('--source-key',
                            help='Source key id',
                            required=True)
    cli_parser.add_argument('--source-secret',
                            help='Source secret',
                            required=True)
    args = parser.parse_args()

    argcomplete.autocomplete(parser)
    if args.key:
        key = args.key
    else:
        config = Config()
        key = config.get_key()
    print(key)

    if args.command == 'cli':
        destination_bucket: str = args.destination_bucket
        destination_endpoint: str = args.destination_endpoint
        destination_key: str = args.destination_key
        destination_secret: str = args.destination_secret
        name: str = args.name
        source_bucket: str = args.source_bucket
        source_endpoint: str = args.source_endpoint
        source_key: str = args.source_key
        source_secret: str = args.source_secret
    elif args.command == 'rclone':
        rclone = Rclone(args.config)
        dest_remote = rclone.get_remote(args.destination_remote)
        src_remote = rclone.get_remote(args.source_remote)
        destination_bucket: str = args.destination_bucket
        destination_endpoint: str = dest_remote["endpoint"]
        destination_key: str = dest_remote["access_key_id"]
        destination_secret: str = dest_remote["secret_access_key"]
        name: str = args.name
        source_bucket: str = args.source_bucket
        source_endpoint: str = src_remote["endpoint"]
        source_key: str = src_remote["access_key_id"]
        source_secret: str = src_remote["secret_access_key"]
    else:
        raise ValueError('Invalid command')
    job = Job(destination_bucket, destination_endpoint, destination_key,
              destination_secret, name, source_bucket, source_endpoint,
              source_key, source_secret, key)
    job.set_rclone_env()


if __name__ == '__main__':
    main()
