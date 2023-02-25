from dotenv import dotenv_values
import os


config = {
    **dotenv_values(".env"),
    **os.environ,
    "token_valid_time": 60 * 60 * 24 * 2 # in [s]  -  2 Days  
}