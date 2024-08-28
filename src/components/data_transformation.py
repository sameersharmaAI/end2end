import sys
from dataclasses import dataclass
import os

#import data transformation libraries and modules
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

#import custom exception handling, logger and save object
from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj

#use dataclass decorator for initializing path variable
@dataclass
class DataTransformationConfig:
    preprocessor_obj_filepath=os.path.join("artifact","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_config(self):

        '''
        This function is responsible for transformating data using transformation pipelines inside a column transformer, which returns a preprocessor object
        '''
        try:
            logging.info("Initiating Data Transformation")

            #define numerical columns
            numerical_columns=['writing_score',"reading_score"]

            #define categorical columns
            categorical_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
                ]
            

            #create numerical pipeline
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            #create categorical pipeline
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("onehot",OneHotEncoder()),
                    ("standardscaling",StandardScaler(with_mean=False))
                ]
            )

            #log progress
            logging.info("Numerical columns standard scaling completed")
            logging.info("Categorical columns transformed")

            #call column transformer with numerical and categorical pipelines to transform data
            preprocessor=ColumnTransformer(
                [
                    ("num_pipepine",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]

            )
            logging.info("Preprocessor created")
            
            #return preprocessor object
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):
        '''
        This function initiates data transformation by reading train and test data, obtaining preprocessor object, 
        applying fit and transform and returning train/test arrays
        as well as preprocessor object
        '''
        try:

            #read train and test data
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            #log progress
            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            #obtain preprocessor object
            preprocessing_obj=self.get_data_transformer_config()

            #create constant target variable
            target_column_name='math_score'

            #create input df for train 
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            #create input df for test
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            

            logging.info("Applying preprocessor object on train and test data")

            #get input feature arrays for test and train df by fit transform using preproccesor obj
            intput_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            intput_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            
            #create train and test array by concatenating input feature array and target feature array converted by numpy
            train_arr=np.c_[intput_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[intput_feature_test_arr,np.array(target_feature_test_df)]

            #call save object function to save preprocessor obj
            save_obj(

                file_path=self.data_transformation_config.preprocessor_obj_filepath,
                obj=preprocessing_obj
            )

            logging.info("Saved preprocessing object")

            #return train, test arrays and preprocessor pickle file
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_filepath
            )



        except Exception as e:
            raise CustomException(e,sys)
            

