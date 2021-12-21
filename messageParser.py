from datetime import timedelta
import databaseAccess

# calculate hours for the day and return them. return error string if necessary
def calculate_time(start: str, end: str, less: float, more: float=0):
    # length of times should be 6 or 7  -->  00:00xm or 0:00xm
    if len(start) < 6 or len(start) > 7 or len(end) < 6 or len(end) > 7:
        return False

    # build clock-in time
    arr = start.split(":")

    # validate the start hours and meridiem
    startHours = int(arr[0])
    if startHours < 1 or startHours > 12:
        return False

    if arr[1].endswith("am"):
        arr[1] = arr[1].replace("am", "")
    elif arr[1].endswith("pm"):
        startHours += 12
        arr[1] = arr[1].replace("pm", "")
    else: # neither am nor pm detected
        return False

    # validate the start minutes
    startMinutes = int(arr[1])
    if startMinutes < 0 or startMinutes > 59:
        return False

    startTime = timedelta(hours=startHours, minutes=startMinutes)


    # build clock-out time
    arr = end.split(":")

    # validate end hours and meridiem
    endHours = int(arr[0])
    if endHours < 1 or endHours > 12:
        return False

    if arr[1].endswith("am"):
        arr[1] = arr[1].replace("am", "")
    elif arr[1].endswith("pm"):
        endHours += 12
        arr[1] = arr[1].replace("pm", "")
    else: # neither am nor pm detected
        return False

    # validate end minutes
    endMinutes = int(arr[1])
    if endMinutes < 0 or endMinutes > 59:
        return False

    endTime = timedelta(hours=endHours, minutes=endMinutes)


    # compute hours for the day and return as a float rounded to 2 decimal places
    if endTime < startTime:
        return False
    else:
        hours = endTime - startTime - timedelta(hours=less) + timedelta(hours=more)

    return round(hours / timedelta(hours=1), 2)



def process_message(message: str) -> bool:
    # break the message apart into an array
    mess = message.split()

    # handle a time submission
    if mess[0] == "time":
        # get the employee id or return False if they don't exist
        employeeId = databaseAccess.get_employee_id(mess[1], mess[2])
        if not employeeId:
            return False
        
        # get the start time, end time, break time, and drive time
        # and calculate the hours to be store in the database
        time = calculate_time(mess[3], mess[4], mess[5], mess[6])
        
        # check if we got errors or if we got hours
        if type(time) is float:
            databaseAccess.insert_time(employeeId, time, message)

    # handle a draw submission
    elif mess[0] == "draw":
        # submit a draw
        pass

    # ignore the message because it isn't meant for us
    else:
        return True

    

    

    
