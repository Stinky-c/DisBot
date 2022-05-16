import os
import anyconfig
import pathlib

# define

# configs
ROOT_CONFIG = anyconfig.load("./config.toml")
_ROOT_CONFIG_PATH = pathlib.Path(".\\config.toml")

# paths
FFMPEG_PATH = pathlib.Path(".\\ffmpeg-win64-lgpl\\bin\\ffmpeg.exe") if "music" not in ROOT_CONFIG["cogs"]["disabled"] else True
TEMP_PATH = pathlib.Path(".\\temp")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# check

# configs
assert os.path.exists(_ROOT_CONFIG_PATH)


# paths
assert os.path.exists(ROOT_DIR)
assert os.path.exists(FFMPEG_PATH)
assert os.path.exists(TEMP_PATH)
