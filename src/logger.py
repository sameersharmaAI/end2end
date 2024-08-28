import logging
import os
from datetime import datetime

#log file common format
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


#logs  path inside log folder
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)

#keep appending files in logs folder
os.makedirs(logs_path,exist_ok=True)

#individual log file
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

#setup basic config to create custom logging. Format varibale has a common format defined. 
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s -%(message)s",
    level=logging.INFO
    )


