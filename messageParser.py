from datetime import timedelta
import databaseAccess

# calculate hours for the day and return them. return error string if necessary
def calculate_time(start: str, end: str, less: float, more: float=0):
    errors = []

    # length of times should be 6 or 7  -->  00:00xm or 0:00xm
    if len(start) < 6 or len(start) > 7:
        errors.append("Clock-in time formatted incorrectly")
    if len(end) < 6 or len(end) > 7:
        errors.append("Clock-out time formatted incorrectly")


    # build clock-in time
    arr = start.split(":")

    # validate the start hours and meridiem
    startHours = int(arr[0])
    if startHours < 1 or startHours > 12:
        errors.append("Clock-in hours out of bounds")
        startHourGood = False
    else:
        startHourGood = True
        if arr[1].endswith("am"):
            arr[1] = arr[1].replace("am", "")
            startMeridiemGood = True
        elif arr[1].endswith("pm"):
            startHours += 12
            arr[1] = arr[1].replace("pm", "")
            startMeridiemGood = True
        else: # neither am nor pm detected
            errors.append("Clock-in missing am/pm")
            startMeridiemGood = False

    # validate the start minutes
    startMinutes = int(arr[1])
    if startMinutes < 0 or startMinutes > 59:
        errors.append("Clock-in minutes out of bounds")
        startMinuteGood = False
    else:
        startMinuteGood = True

    if startHourGood and startMinuteGood and startMeridiemGood:
        startTime = timedelta(hours=startHours, minutes=startMinutes)
        startTimeGood = True
    else:
        startTimeGood = False


    # build clock-out time
    arr = end.split(":")

    # validate end hours and meridiem
    endHours = int(arr[0])
    if endHours < 1 or endHours > 12:
        errors.append("end hour out of bounds")
        endHourGood = False
    else:
        endHourGood = True
        if arr[1].endswith("am"):
            arr[1] = arr[1].replace("am", "")
            endMeridiemGood = True
        elif arr[1].endswith("pm"):
            endHours += 12
            arr[1] = arr[1].replace("pm", "")
            endMeridiemGood = True
        else: # neither am nor pm detected
            errors.append("end time missing am/pm")
            endMeridiemGood = False

    # validate end minutes
    endMinutes = int(arr[1])
    if endMinutes < 0 or endMinutes > 59:
        errors.append("end minutes out of bounds")
        endMinuteGood = False
    else:
        endMinuteGood = True

    if endHourGood and endMinuteGood and endMeridiemGood:
        endTime = timedelta(hours=endHours, minutes=endMinutes)
        endTimeGood = True
    else:
        endTimeGood = False

    # compute hours for the day and return as a float rounded to 2 decimal places
    if startTimeGood and endTimeGood:
        if endTime < startTime:
            errors.append("End time is earlier than start time")
        else:
            hours = endTime - startTime - timedelta(hours=less) + timedelta(hours=more)

    if len(errors) == 0:
        return round(hours / timedelta(hours=1), 2)
    else:
        return errors



def process_message(message: str) -> bool:
    # break the message apart into an array
    mess = message.split()

    # get the employee id or return False if they don't exist
    id = databaseAccess._get_employee_id(mess[0], mess[1])
    if not id:
        return False

    # check if this is a submission for hours or a draw
    if mess[2] == "time":
        # get the start time, end time, break time, and drive time and
        # calculate the time they worked that day to be store in the database
        time = calculate_time(mess[3], mess[4], mess[5], mess[6])
    elif mess[2] == "draw":
        # submit a draw
        pass
