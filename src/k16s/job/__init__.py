import os
import sqlite3
import time

from cryptography.fernet import Fernet
import mysql.connector


class JobTable():

    def __init__(self, db_path: str = 'jobs.db', table_name: str = 'jobs'):
        self.db_path = db_path
        self.table_name = table_name
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination_bucket TEXT,
                destination_endpoint TEXT,
                destination_key TEXT,
                destination_secret TEXT,
                name TEXT,
                source_bucket TEXT,
                source_endpoint TEXT,
                source_key TEXT,
                source_secret TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)


class Job():

    def __init__(self,
                 destination_bucket: str,
                 destination_endpoint: str,
                 destination_key: str,
                 destination_secret: str,
                 name: str,
                 source_bucket: str,
                 source_endpoint: str,
                 source_key: str,
                 source_secret: str,
                 key: str,
                 job_table: JobTable = JobTable()):
        self.cipher_suite = Fernet(key)
        self.job_table = job_table
        self.name = name
        self.destination_bucket = destination_bucket
        self.destination_endpoint = destination_endpoint
        self.destination_key = self.cipher_suite.encrypt(
            destination_key.encode('utf-8'))
        self.destination_secret = self.cipher_suite.encrypt(
            destination_secret.encode('utf-8'))
        self.source_bucket = source_bucket
        self.source_endpoint = source_endpoint
        self.source_key = self.cipher_suite.encrypt(source_key.encode('utf-8'))
        self.source_secret = self.cipher_suite.encrypt(
            source_secret.encode('utf-8'))
        self.id = self.select_id()
        if self.id == -1:
            self.insert_job()

    def select_id(self):
        select_query: str = f"""
        SELECT
            id
        FROM
            {self.job_table.table_name}
        WHERE
            destination_bucket = '{self.destination_bucket}'
        AND
            destination_endpoint = '{self.destination_endpoint}'
        AND
            name = '{self.name}'
        AND
            source_bucket = '{self.source_bucket}'
        AND
            source_endpoint = '{self.source_endpoint}'
        """
        self.job_table.cursor.execute(select_query)
        row = self.job_table.cursor.fetchone()

        if row is None:
            return -1
        return int(row[0])

    def insert_job(self):
        insert_query: str = f"""
            INSERT INTO {self.job_table.table_name}
            (
                destination_bucket,
                destination_endpoint,
                destination_key,
                destination_secret,
                name,
                source_bucket,
                source_endpoint,
                source_key,
                source_secret
            )
            VALUES(
                '{self.destination_bucket}',
                '{self.destination_endpoint}',
                '{self.destination_key.decode()}',
                '{self.destination_secret.decode()}',
                '{self.name}',
                '{self.source_bucket}',
                '{self.source_endpoint}',
                '{self.source_key.decode()}',
                '{self.source_secret.decode()}'
            );
        """
        try:
            self.job_table.cursor.execute(insert_query)
            self.job_table.conn.commit()
            self.id = self.job_table.cursor.lastrowid
        except Exception as e:
            print(e)
            self.id = -1
        return self.id

    def upsert_job(self):
        update_query = f"""
            UPDATE jobs
            SET
                destination_bucket = '{self.destination_bucket}',
                destination_endpoint = '{self.destination_endpoint}',
                destination_key = '{self.destination_key.decode()}',
                destination_secret = '{self.destination_secret.decode()}',
                name = '{self.name},'
                source_bucket = '{self.source_bucket}',
                source_endpoint = '{self.source_endpoint}',
                source_key = '{self.source_key.decode()}',
                source_secret = '{self.source_secret.decode()}',
                updated_at = {time.now()}
            WHERE
                id = {self.id}
        """
        if self.id != -1:
            self.job_table.cursor.execute(update_query)
            self.job_table.conn.commit()
        else:
            self.insert_job()

    def delete_job(self):
        delete_query = f"""
            DELETE FROM
                jobs
            WHERE
                id = {self.id}
        """
        if self.id != -1:
            self.job_table.cursor.execute(delete_query)
            self.job_table.conn.commit()

    def decrypt(self, cipher_text):
        return self.cipher_suite.decrypt(cipher_text).decode()

    def set_rclone_env(self):
        dest_name_base = f'RCLONE_CONFIG_DESTINATION{self.name.upper()}_'
        os.environ[f'{dest_name_base}_TYPE'] = 's3'
        os.environ[f'{dest_name_base}_PROVIDER'] = 'Ceph'
        os.environ[f'{dest_name_base}_ACL'] = 'private'
        os.environ[f'{dest_name_base}_ACCESS_KEY_ID'] = self.decrypt(
            self.destination_key)
        os.environ[f'{
            dest_name_base}_SECRET_ACCESS_KEY'] = self.decrypt(self.destination_secret)
        os.environ[f'{dest_name_base}_ENDPOINT'] = self.destination_endpoint
        source_name_base = f'RCLONE_CONFIG_SOURCE{self.name.upper()}_'
        os.environ[f'{source_name_base}_TYPE'] = 's3'
        os.environ[f'{source_name_base}_PROVIDER'] = 'Ceph'
        os.environ[f'{source_name_base}_ACL'] = 'private'
        os.environ[f'{source_name_base}_ACCESS_KEY_ID'] = self.decrypt(
            self.source_key)
        os.environ[f'{
            source_name_base}_SECRET_ACCESS_KEY'] = self.decrypt(self.source_secret)
        os.environ[f'{source_name_base}_ENDPOINT'] = self.source_endpoint
