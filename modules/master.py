import discord
from discord.ext import commands
from modules.utils import permissions
from modules.utils.converters import GlobalUser
from .utils.writer import writer
from .utils.formatting import pages, code

import importlib
import traceback
import logging
import asyncio
import threading
import datetime
import glob
import os
import aiohttp

log = logging.getLogger('sparkz.master')


class ModuleNotFound(Exception):
    pass


class ModuleLoadError(Exception):
    pass


class NoSetup(ModuleLoadError):
    pass


class ModuleUnload(Exception):
    pass


class MasterUnloadWithoutReload(ModuleUnload):
    pass