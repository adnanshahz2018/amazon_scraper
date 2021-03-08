import schedule, time, datetime
from amazon import kindle, audible

def scheduler():
    kind = kindle()
    audi = audible()
    kind.scrape_category()
    audi.scrape_category()
    tm = str(datetime.datetime.now()).split(':')
    tim = 'Last Updated = ' + tm[0] + ':' + tm[1]
    print( '\n---------------------------------------------------\n', tim, '\n---------------------------------------------------\n')

schedule.every().day.do(scheduler)
print('scheduled for tommorow '+ str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) )
while True:
    schedule.run_pending()
    time.sleep(1)