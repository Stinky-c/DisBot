import os
import anyconfig

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_CONFIG = anyconfig.load("./config.toml")
