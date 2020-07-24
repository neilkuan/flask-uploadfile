from datetime import datetime, timezone, timedelta
import os
import platform

tz = timezone(timedelta(hours=+8))

def what_time_is():
    tz = timezone(timedelta(hours=+8))
    datetime.now(tz).isoformat()
    time = datetime.now(tz).isoformat(timespec="seconds")
    return str("This time is  " + time )

def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def get_file_size(path_to_file):
    try:
        size = os.path.getsize(path_to_file)
        if size <= 1024:
            return str(size) + " bytes "
        elif size > 1024 and 1024*1024 >= size:
            return str(round(size/1024, 2)) + " KB "
        elif size > 1024*1024 and 1024*1024*1024 >= size:
            return str(round(size/(1024*1024),2)) + " MB "
        else:
            return "None"
    except:
        return "have nothing wrong !!!"


print(datetime.fromtimestamp(creation_date('./pic/knative_logpng.png')).isoformat(timespec="seconds"))
print(what_time_is())
print(get_file_size('./pic/knative_logpng.png'))