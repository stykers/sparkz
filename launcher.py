from __future__ import print_function
import os
import sys
import subprocess
try:
    import urllib.request
    from importlib.util import find_spec
except ImportError:
    pass
import platform
import webbrowser
import hashlib
import argparse
import shutil
import stat
import time
try:
    import pip
except ImportError:
    pip = None

if os.name is "nt":
    print('This bot does not support Windows for now, please use Linux based operating systems.')
    quit(1)

sys.path.insert(0, 'lib')

if sys.version_info < (3, 5):
    print('This bot requires Python 3.5+, please upgrade your python installation.')
    quit(1)


def cli_args():
    parser = argparse.ArgumentParser(description='Sparkz - PreInitialization sequence')
    parser.add_argument('--start', '-s',
                        help='Add this parameter to start Sparkz directly.',
                        action='store_true')
    parser.add_argument('--auto-restart', '-r',
                        help='Add this parameter to make Sparkz automatically restart on crash.',
                        action='store_true')
    parser.add_argument('--update', '--upgrade',
                        help='Add this parameter to make the launcher update the bot to latest version.',
                        action='store_true')
    parser.add_argument('--fix-req', '-f',
                        help='Add this parameter to make the bot install/fix the requirements')
    return parser.parse_args()


def fix_req():
    interpreter = sys.executable

    if interpreter is None:
        print('Error: No python interpreter found!')
        return

    args = [
        interpreter, '-m',
        'pip', 'install',
        '--upgrade',
        '--target', 'lib',
        '-r', 'requirements.txt'
    ]

    return_value = subprocess.call(args)

    if return_value is 0:
        print('\nRequirements are fixed.')
    else:
        print('\nSomething went wrong while trying to fix requirements, check your logs for more details or create an '
              'issue at https://git.syskiller.io/Stykers/sparkz/issues if you think this is a bug.\n')


def update_pip():
    interpreter = sys.executable

    if interpreter is None:
        print('Error: No python interpreter found!')
        return

    args = [
        interpreter, "-m",
        "pip", "install",
        "--upgrade", "pip"
    ]

    return_value = subprocess.call(args)

    if return_value is 0:
        print('\nPip has been updated successfully.')
    else:
        print('\nPip upgrade failed successfully.')


def update_sparkz():
    try:
        return_value = subprocess.call(("git", "pull", "--ff-only"))
    except FileNotFoundError:
        print('\nGit is not installed or is not in $PATH, install git using a native package manager or download it '
              'from https://git-scm.com/')
        return
    if return_value is 0:
        print('\nSparkz is now the latest version!')
    else:
        print('\nUpdate failed! If you modified the code please backup data/ and plugins/ and manually download the '
              'newest version.')


def wipe_sparkz(reqs=False, data=False, plugins=False, revert_changes=False):
    if reqs:
        try:
            shutil.rmtree('lib')
            print('Wiped pip packages for this bot instance.')
        except FileNotFoundError:
            pass
        except Exception:
            print('Something went wrong while wiping packages, please check permissions of lib/ or create an issue at '
                  'https://git.syskiller.io/Stykers/sparkz/issues if you think this is a bug.')

    if data:
        try:
            shutil.rmtree('data')
            print('Wiped config and data for this bot instance.')
        except FileNotFoundError:
            pass
        except Exception:
            print('Something went wrong while wiping packages, please check permissions of lib/ or create an issue at '
                  'https://git.syskiller.io/Stykers/sparkz/issues if you think this is a bug.')

    if plugins:
        try:
            shutil.rmtree("plugins")
            print('Wiped all user plugins for this bot instance.')
        except FileNotFoundError:
            pass
        except Exception:
            print('Something went wrong while wiping packages, please check permissions of lib/ or create an issue at '
                  'https://git.syskiller.io/Stykers/sparkz/issues if you think this is a bug.')

    if revert_changes:
        return_value = subprocess.call(('git', 'reset', '--hard'))

        if return_value is 0:
            print('Reverted all changes you have made.')
        else:
            print('Could not fix the code, you probably broke something, please backup data/ and plugin/ and manually '
                  'download the official source.')


def check_requirements():
    sys.path_importer_cache = {}
    if not find_spec('discord'):
        return None
    elif not find_spec('nacl'):
        return None
    else:
        return True


def check_git():
    try:
        subprocess.call(['git', '--version'], stdout=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return False
    else:
        return True


def main_menu():
    os.system('clear')
    while True:
        print('Sparkz - PreInitialization sequence')
        print('Stuff you can do:')
        print('1. Start sparkz')
        print('2. Start sparkz with auto restart')
        print('3. Install requirements')
        print('4. Update pip')
        print('5. Update sparkz')
        print('6. Wipe sparkz')
        print('7. Check requirements')
        print('8. Check git')