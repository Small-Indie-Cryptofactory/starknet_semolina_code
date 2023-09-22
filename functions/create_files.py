from utils.files_utils import touch
from data import config


def create_files():
    touch(path=config.FILES_DIR)
    touch(path=config.DEBUG_PATH, file=True)


create_files()
