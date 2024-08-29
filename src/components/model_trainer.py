

#import custom exception handling, logger, utils and dataclass
from src.exception import CustomException
from src.logger import logging
import sys
import os
from dataclasses import dataclass
from src.utils import save_obj,evaluate_model

#import regression model linraries and mertrics
from sklearn.ensemble import (AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

@dataclass
class ModelTrainerConfig:
    '''this dataclass configures model pickle file path
    '''
    trained_model_file_path=os.path.join("artifact","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_arr,test_arr):
        '''Initiate model trainer function '''
        try:


            logging.info("Splitting train and test input data")

            #split test train data 
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            #create model dictionary
            models={
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            logging.info("Calling evaluate model")
            model_report:dict=evaluate_model(x_train,y_train,x_test,y_test,models)
            logging.info("Report created")

            #Get best model score from dic
            best_model_score=max(sorted(model_report.values()))

            #Get best model name
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model=models[best_model_name]

            if best_model_score<0.7:
                raise CustomException("No best model found")
            
            logging.info("Best model found on training and testing dataset")

            #save model obj
            save_obj(file_path=self.model_trainer_config.trained_model_file_path,
                     obj=best_model)
            logging.info("Model saved")

            predicted=best_model.predict(x_test)

            r2=r2_score(y_test,predicted)
            logging.info("r2 score determined")

            return r2
        
        except Exception as e:
            raise CustomException(e,sys)













