
from datetime import timedelta
from sqlalchemy.sql.sqltypes import String
import databaseAccess
import exceptions


# calculate hours for the day and return them
def calculate_time(start: str, end: str, less: str, more: str = "") -> float:
    # length of times should be 6 or 7  -->  00:00xm or 0:00xm
    if len(start) < 6 or len(start) > 7 or len(end) < 6 or len(end) > 7:
        raise exceptions.TimeFormatException

    # build clock-in time
    arr = start.split(":")

    # validate the start hours and meridiem
    startHours = int(arr[0])
    if startHours < 1 or startHours > 12:
        raise exceptions.HoursException

    if arr[1].endswith("am"):
        arr[1] = arr[1].replace("am", "")
    elif arr[1].endswith("pm"):
        startHours += 12
        arr[1] = arr[1].replace("pm", "")
    else: # neither am nor pm detected
        raise exceptions.MeridiemException

    # validate the start minutes
    startMinutes = int(arr[1])
    if startMinutes < 0 or startMinutes > 59:
        raise exceptions.MinutesException

    startTime = timedelta(hours=startHours, minutes=startMinutes)


    # build clock-out time
    arr = end.split(":")

    # validate end hours and meridiem
    endHours = int(arr[0])
    if endHours < 1 or endHours > 12:
        raise exceptions.HoursException

    if arr[1].endswith("am"):
        arr[1] = arr[1].replace("am", "")
    elif arr[1].endswith("pm"):
        endHours += 12
        arr[1] = arr[1].replace("pm", "")
    else: # neither am nor pm detected
        raise exceptions.MeridiemException

    # validate end minutes
    endMinutes = int(arr[1])
    if endMinutes < 0 or endMinutes > 59:
        raise exceptions.MinutesException

    endTime = timedelta(hours=endHours, minutes=endMinutes)

    # check for any other exceptions in the message
    if endTime < startTime:
        raise exceptions.IllegalTimeException
    
    try:
        subtract = float(less)
    except:
        raise exceptions.LunchException
    
    try:
        add = float(more)
    except:
        raise exceptions.ExtraException

    # compute hours for the day and return as a float rounded to 2 decimal places
    hours = endTime - startTime - timedelta(hours=subtract) + timedelta(hours=add)
    return round(hours / timedelta(hours=1), 2)


def process_time(message: str):
    mess = message.split()

    # get the employee id
    employeeId = databaseAccess.get_employee_id(mess[1], mess[2])
    if not employeeId:
        raise exceptions.NoSuchUserException
    
    # get the start time, end time, break time, and drive time
    # and calculate the hours to be stored in the database
    time = calculate_time(mess[3], mess[4], mess[5], mess[6])

    # add the hours to the database
    databaseAccess.insert_time(employeeId, time, message)


def process_draw(message: str):
    mess = message.split()

    # get the employee id or return False if they don't exist
    employeeId = databaseAccess.get_employee_id(mess[1], mess[2])
    if not employeeId:
        raise exceptions.NoSuchUserException

    if "$" in mess[3]:
        mess[3].replace("$", "")

    try: # cast the dollar amount to a float    
        draw = float(mess[3])
    except:
        raise exceptions.DrawException

    databaseAccess.insert_draw(employeeId, draw, message)



def process_message(message: str) -> bool:
    # break the message apart into an array
    mess = message.split()

    # handle a time submission
    if mess[0] == "time":
        process_time(message)
        return True

    # handle a draw submission
    elif mess[0] == "draw":
        process_draw(mess)
        return True

    # ignore the message because it isn't meant for us
    else:
        return False

    