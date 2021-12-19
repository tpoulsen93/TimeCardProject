from datetime import time
import databaseAccess.py
    

def __calculate_time(start: time, end: time, lunch: float, drive: float=0):
    pass



def parse_message(message: str) -> bool:
    # break the message apart into an array
    arr = message.split()

    # get the employee id or return False if they don't exist
    id = databaseAccess._get_employee_id(arr[0], arr[1])
    if not id:
        return False

    # get the start time, end time, break time, and drive time and
    # calculate the time they worked that day to be store in the database
