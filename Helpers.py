from datetime import datetime, time

#Converts date to datetime format:  24-09-2020 -> 24-09-2020 00:00:00
def date2datetime(date):
    t = time() #Returns time 00:00:00
    return(datetime.combine(date, t))
