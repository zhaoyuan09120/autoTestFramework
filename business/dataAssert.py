import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


print(int((datetime.now()- relativedelta(months=1)).timestamp() * 1000))
print(type(int((datetime.now()- relativedelta(months=1)).timestamp() * 1000)))