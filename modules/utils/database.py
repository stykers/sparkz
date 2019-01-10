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
    def database(username, password, database, host):
        """Connects to and gets the database."""
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
                database = None
                print(e)
                print('\nCould not recover, exiting!')
                quit(1)
        return database

    @staticmethod
    def cursor(database):
        """Gets the cursor for MySQL."""
        try:
            cursor = database.cursor()
        except InvalidCredentials:
            raise InvalidCredentials('Failed to login to mysql with given credentials!')
        except DatabaseNotFound:
            raise DatabaseNotFound('Database not found!')
        except Exception as e:
            cursor = None
            print(e)
            print('\nCould not recover, exiting!')
            quit(1)
        return cursor