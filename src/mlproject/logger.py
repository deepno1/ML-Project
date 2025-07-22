import logging
from datetime import datetime
import os

LOG_FILE = "{}.log".format(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
log_dir = os.path.join(os.getcwd(),"logs")
os.makedirs(log_dir,exist_ok=True)

LOG_FILE_PATH = os.path.join(log_dir,LOG_FILE)

logging.basicConfig(
    filename= LOG_FILE_PATH,
    format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)