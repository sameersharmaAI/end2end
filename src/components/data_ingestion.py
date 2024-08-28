import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

#used for creating class variables 
from dataclasses import dataclass

#import custom exception and logger
from src.exception import CustomException
from src.logger import logging 


#dataclass lets you create variables without using a constructor to define variables. Use decorator if class has no or less functions. Use __init__ for classes with functions
#define save(output) paths for train, test and raw data files
@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join("artificat","train.csv")
    test_data_path:str=os.path.join("artificat","test.csv")
    raw_data_path:str=os.path.join("artificat","raw.csv")

#create dataingestion class that has functions to ingest data and save data to the paths defined by dataingestionconfig class
class DataIngestion:
    def __init__(self):
        self.injestion_config=DataIngestionConfig

    def initiate_data_ingestion(self):
        logging.info("Entered data ingestion component")
        try:
            #read data from csv and create log
            df=pd.read_csv(r"notebooks\stud.csv")
            logging.info("Read dataset as dataframe")

            #check if folder is created, if not create it
            os.makedirs(os.path.dirname(self.injestion_config.train_data_path),exist_ok=True)

            #save raw data to path
            df.to_csv(self.injestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")

            #create training set and testing set
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            #save training and test sets  as csv to paths
            train_set.to_csv(self.injestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.injestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of data completed")

            #return paths for train.csv and test.csv 
            return self.injestion_config.train_data_path,self.injestion_config.test_data_path
        
        except Exception as e:
            raise CustomException(e,sys)

if __name__=='__main__':
    data_obj=DataIngestion()
    data_obj.initiate_data_ingestion()
