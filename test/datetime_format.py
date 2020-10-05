from datetime import datetime


# output = "{:%Y%m%d%H%M%S}"
datestr_format = "{:%Y-%m-%d_%H%M%S}"
datestr = datestr_format.format(datetime.now())


print(datestr.format(datetime.now()))
