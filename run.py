from pricedropalert.alert import Alert
import time

while True:
    one = Alert()
    one.execute()
    if one.mail_sent == True:
        break
    time.sleep(10)










