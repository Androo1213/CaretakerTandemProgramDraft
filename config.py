import os
import sys
import pathlib
from dotenv import dotenv_values

# Paths for finding env files
cwd_path = os.path.join(os.getcwd(), '.env')
global_path = os.path.join(pathlib.Path.home(), '.config/CaretakerTandemProgram/.env')

values = {}

if os.path.exists(cwd_path):
    values = dotenv_values(cwd_path)
elif os.path.exists(global_path):
    values = dotenv_values(global_path)
else:
    values = dotenv_values()


# Get config values
def get(val, default=None):
    return os.environ.get(val, values.get(val, default))


def get_one_of(name, default=None, options=[]):
    val = get(name, default)
    if val not in options:
        print(f"Error: {name} must be one of: {options}")
        print(f"Current value: {val}")
        sys.exit(1)
    return val


def get_number(name, default):
    val = get(name, default)
    try:
        return float(val)
    except ValueError:
        print(f"Error: {name} must be a number.")
        print(f"Current value: {val}")
        sys.exit(1)


def get_bool(name, default):
    return str(get(name, default) or '').lower() in ('true', '1')


# req config params
TCONNECT_EMAIL = input("Please enter your t:connect email: ")
TCONNECT_PASSWORD = input("Please enter your t:connect password: ")

# Optional configs
AUTOUPDATE_DEFAULT_SLEEP_SECONDS = get_number('AUTOUPDATE_DEFAULT_SLEEP_SECONDS', '300')  # 5 mins
AUTOUPDATE_MAX_SLEEP_SECONDS = get_number('AUTOUPDATE_MAX_SLEEP_SECONDS', '1500')  # 25 mins
AUTOUPDATE_USE_FIXED_SLEEP = get_bool('AUTOUPDATE_USE_FIXED_SLEEP', 'false')
