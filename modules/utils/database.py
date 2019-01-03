import os
import mysql.connector


class InvalidCredentials(Exception):
    pass


class DatabaseNotFound(Exception):
    pass


class Database:
    def __init__(self):
        self.logger = logging.getLogger('sparkz')

    @staticmethod
    def connect(username, password, database, host):
        try:
            database = mysql.connector.connect(user=username,
                                               password=password,
                                               host=host,
                                               database=database)
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise InvalidCredentials('Failed to login to mysql with given credentials!')
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                raise DatabaseNotFound('Specified database does not exist!')
            else:
                print(e)
                print('\nCould not recover, exiting!')
                exit(1)
        return database