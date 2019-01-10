from modules.utils.writer import Writer
from copy import deepcopy
import discord
import os
import argparse
import mysql.connector

config_path = 'data/configuration.json'


class Configuration:

    def __init__(self, path=config_path, parse_args=True):
        self.path = path
        self.check_dirs(self=self)
        self.default_config = {
            'TOKEN': None,
            'EMAIL': None,
            'PASSWORD': None,
            'MASTER': None,
            'PREFIXES': ['s!', '/'],
            'ADMIN': 'Administrator',
            'MOD': 'Moderator',
            'database': {
                'username': 'sparkz',
                'password': 'password',
                'database': 'sparkz',
                'host': '127.0.0.1'
            }
        }
        self._runtime_config = False

        if not Writer.validate_json(modules.utils.writer.validate_json(), self.path):
            self.bot_config = deepcopy(self.default_config)
            self.save_config(self=self)
        else:
            current = Writer.load_json(modules.utils.writer.load_json(), self.path)
            if current.keys() is not self.default_config.keys():
                for key in self.default_config.keys():
                    if key not in current.keys():
                        current[key] = self.default_config[key]
                        print('Added ' + str(key) + "to config.json as it was missing.")
                Writer.write_json(modules.utils.writer.write_json(), self.path, current)
            self.bot_config = Writer.load_json(modules.utils.writer.load_json(), self.path)

        if parse_args:
            self.parse_command_arguments(self=self)

    @staticmethod
    def parse_command_arguments(self):
        parser = argparse.ArgumentParser(description='Sparkz - A multi-function plugin based discord bot.')
        parser.add_argument('--master', help='Discord user ID of the master which have access to all commands, only '
                                             'the person that maintains the server that hosts this bot is supposed to '
                                             'be master.')
        parser.add_argument('--auditor', action='append', default=[],
                            help='Discord user ID of the auditor which have access to all commands, only the person '
                                 'who have access to the instance files/database is supposed to be auditor. There can '
                                 'be multiple auditors.')
        parser.add_argument('--prefix', '-p', action='append',
                            help='The prefix of this bot, can have multiple prefixes.')
        parser.add_argument('--admin', help='Defines administrator role for sparkz.')
        parser.add_argument('--mod', help='Defines moderator role for sparkz.')
        parser.add_argument('--safe-mode',
                            action='store_true',
                            help='Disables all plugins and starts sparkz, use this if something caused a crash loop.')
        parser.add_argument('--self-bot',
                            action='store_true',
                            help='Specifies if sparkz should treat the account as a normal user account.')
        parser.add_argument('--runtime-config',
                            action='store_true',
                            help='This will make config get saved in memory and not write to hard disk.')
        parser.add_argument('--dry-run',
                            action='store_true',
                            help='Makes sparkz quit after loading all plugins with exit code 0.')
        parser.add_argument('--debug',
                            action='store_true',
                            help='Enables debug mode, do not use unless you know what you are doing.')

        args = parser.parse_args()

        if args.master:
            self.master = args.master
        if args.prefix:
            self.prefixes = sorted(args.prefix, reverse=True)
        if args.admin:
            self.admin = args.admin
        if args.mod:
            self.mod = args.mod

        self.self_bot = args.self_bot
        self._runtime_config = args.runtime_config
        self._safe_mode = args.safe_mode
        self.debug = args.debug
        self._dry_run = args.dry_run
        self.auditors = args.auditor

        self.save_config()

    @staticmethod
    def check_dirs(self):
        directories = ('data', os.path.dirname(self.path), 'modules', 'modules/utils')
        for directory in directories:
            if not os.path.exists(directory):
                print('Creating ' + directory + ' for the first time.')
                os.makedirs(directory)

    @staticmethod
    def save_config(self):
        if not self._safe_mode:
            Writer.write_json(modules.utils.writer.write_json(), self.path, self.bot_config)

    @property
    def database(self):
        return self.bot_config

    @property
    def master(self):
        return self.bot_config['MASTER']

    @master.setter
    def master(self, value):
        self.bot_config['MASTER'] = value

    @property
    def token(self):
        return os.environ.get('DISCORD_TOKEN', self.bot_config['TOKEN'])

    @token.setter
    def token(self, value):
        self.bot_config['TOKEN'] = value
        self.bot_config['EMAIL'] = None
        self.bot_config['PASSWORD'] = None

    @property
    def email(self):
        return os.environ.get('DISCORD_EMAIL', self.bot_config['EMAIL'])

    @email.setter
    def email(self, value):
        self.bot_config['EMAIL'] = value
        self.bot_config['TOKEN'] = None

    @property
    def password(self):
        return os.environ.get('DISCORD_PASSWORD', self.bot_config['PASSWORD'])

    @password.setter
    def password(self, value):
        self.bot_config['PASSWORD'] = value

    @property
    def prefixes(self):
        return self.bot_config['PREFIXES']

    @prefixes.setter
    def prefixes(self, value):
        assert isinstance(value, list)
        self.bot_config['PREFIXES'] = value

    @property
    def admin(self):
        return self.bot_config['ADMIN']

    @admin.setter
    def admin(self, value):
        self.bot_config['ADMIN'] = value

    @property
    def mod(self):
        return self.bot_config['MOD']

    @mod.setter
    def mod(self, value):
        self.bot_config['MOD'] = value