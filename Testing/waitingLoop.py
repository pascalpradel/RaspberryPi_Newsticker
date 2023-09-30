from datetime import datetime, timedelta


def customSleep(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    
    while datetime.now() < end_time:
        pass


customSleep(0.5)
print("Test")