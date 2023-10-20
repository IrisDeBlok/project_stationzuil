import random
import psycopg2
import time

DB_HOST = "localhost"
DB_NAME = "stationzuil"
DB_USER = "postgres"
DB_PASS = "Koeskoes123123!"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

date = time.strftime("%Y/%m/%d")
time = time.strftime("%H:%M:%S")

locationList = [
                'Amsterdam',
                'Gouda',
                'Groningen',
                'Den Haag',
                'Den Bosch',
                'Leeuwarden',
                'Maastricht',
                'Utrecht',
                ]
location = random.choice(locationList)
name = input('Vul hier uw naam in: ')
message = input('Vul hier uw bericht in: ')

def leavingMessage():
    if len(name) == 0:
        print('Hallo anoniem')
    else:
        print('Hallo ' + name)

    print('Datum:', date, time)
    print('Locatie:', location)

    if len(message) == 0:
        print('Bericht is verplicht')
    elif len(message) > 140:
        print('Bericht is te lang. Houd het bericht onder 140 karakters')
    else:
        print('Bericht:', message)

    cur.execute("INSERT INTO bericht(naam, datum, tijd, locatie, bericht) VALUES(%s, %s, %s, %s, %s);", (name, date, time, location, message))
    conn.commit()

leavingMessage()

cur.close()
conn.close()




# conceptioneel, functioneel en logisch database
# deze moet info uit het csv bestand lezen en daar goedkeuring over vragen
# lege regel of die  goed gekeurd is
# als die leeg is moet die nog nagekeken worden
