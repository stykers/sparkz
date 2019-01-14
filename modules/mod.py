import discord
from discord.ext import commands
from .utils.writer import Writer
from .utils import permissions
from datetime import datetime
from collections import deque, defaultdict, OrderedDict
from modules.utils.formatting import escape_mass_mentions, box, pages
import os
import re
import logging
import asyncio