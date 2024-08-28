import sys
from src.logger import logging


def error_message_details(error,error_detail:sys):
    '''
    This function creates a format for our custom exception handling
    '''
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occurered in Python Script [{0}] line number [{1}] error message [{2}]".format(file_name,exc_tb.tb_lineno,str(error))
    return error_message


#Create a custom class inheriting from Exception class and call error function defined above when raised and print the error message"
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_details(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    


