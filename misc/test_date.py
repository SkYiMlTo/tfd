import time
from datetime import datetime

a = time.time() + 3600
while True:
    print(a - time.time())
    time.sleep(0.5)
