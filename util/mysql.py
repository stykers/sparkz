import pymysql.cursors, json
from util import essential


class Mysql:

    def __init__(self):
        self.config = essential.get("config.yml")
        self.host = self.config.mysql.host
        try:
            self.port = int(self.config.mysql.port)
        except KeyError:
            self.port = 3306
        self.username = self.config.mysql.username
        self.password = self.config.mysql.password
        self.db = self.config.mysql.db
        self.connected = 1
        self.connection = None
        self.build_connection()

    def build_connection(self):
        if self.connected == 0:
            print("Database connection is lost, attempting reconnect...")
        elif self.connected == 1:
            print("Connected to the database.")
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            db=self.db
        )
