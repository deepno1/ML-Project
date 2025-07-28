from src.mlproject.logger import logging
import sys

def error_msg_detail(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occured in Python Script name [{0}] Line No. [{1}] Error Message [{2}]".format(file_name, exc_tb.tb_lineno, str(error))

    return error_message

class CustomException(Exception):
    def __init__(self,error_msg,error_detail : sys):
        super.__init__(error_msg)
        self.error_msg = error_msg_detail(error_msg,error_detail)

    def __str__(self):
        return self.error_msg

