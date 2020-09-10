from datetime import datetime, time, timedelta

#Converts date to datetime format:  24-09-2020 -> 24-09-2020 00:00:00
def date2datetime(date):
    t = time() #Returns time 00:00:00
    return(datetime.combine(date, t))


#Date iterator: used to loop through intervals of time -> for t in daterange(start, end): doSomething 
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)