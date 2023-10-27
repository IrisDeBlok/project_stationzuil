import psycopg2
import time

date = time.strftime("%Y/%m/%d %H:%M")

DB_HOST = "localhost"
DB_NAME = "stationzuil"
DB_USER = "postgres"
DB_PASS = "Koeskoes123123!"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

def approvingMessage():
    name = input("Vul uw naam in: ")
    email = input("Vul uw email in: ")
    # controleer op naam en email
    # als die er in staat, id pakken
    # anders in database zetten
    cur.execute("SELECT * FROM bericht WHERE NOT EXISTS (SELECT beoordeling.berichtid FROM beoordeling WHERE bericht.berichtid = beoordeling.berichtid)")
    berichten = cur.fetchall()


    for bericht in berichten:
        berichtId = bericht[0]
        cur.execute("SELECT * from moderator WHERE naam = %s AND email = %s", (name, email))
        activeModerators = cur.fetchall()
        for activeModerator in activeModerators:
            moderatorId = activeModerator[0]
            print(bericht[4])
            beoordeling = input("Wilt u dit bericht goedkeuren?(y/n)")
            if beoordeling == "y":
                cur.execute("INSERT INTO beoordeling (berichtid, moderatorid, datum, beoordeling) VALUES(%s, %s, %s, %s);", (berichtId, moderatorId, date, True))
                conn.commit()
            elif beoordeling == "n":
                cur.execute("INSERT INTO beoordeling (berichtid, moderatorid, datum, beoordeling) VALUES(%s, %s, %s, %s);", (berichtId, moderatorId, date, False))
                conn.commit()
            elif beoordeling == "break" or beoordeling == "exit" or beoordeling == "stop":
                return
            else:
                print("niet een juiste invoer")
        # print("Geen nieuwe berichten!")



approvingMessage()

cur.close()
conn.close()
