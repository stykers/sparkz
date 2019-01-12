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
from modules.utils.writer import Writer
from modules.utils.formatting import code_single
from collections import Counter
from io import TextIOWrapper

