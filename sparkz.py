import os
import sys
import asyncio

sys.path.insert(0, 'lib')
import logging
import logging.handlers
import traceback
import datetime
import subprocess
from discord.ext import commands
import discord
from modules.utils.configuration import Configuration