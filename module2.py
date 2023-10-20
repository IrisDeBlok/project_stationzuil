import psycopg2
import time

date = time.strftime("%Y/%m/%d")
time = time.strftime("%H:%M")

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
    cur.execute("SELECT * FROM bericht WHERE NOT EXISTS (SELECT goedkeuring.berichtid FROM goedkeuring WHERE bericht.berichtid = goedkeuring.berichtid)")
    berichten = cur.fetchall()

    for bericht in berichten:
        cur.execute("SELECT * from moderator WHERE naam = %s", (name,))
        activeModerators = cur.fetchall()
        for activeModerator in activeModerators:
            print(activeModerator[0])
            print(bericht[5])
            goedkeuring = input("Wilt u dit bericht goedkeuren?(y/n)")
            if goedkeuring == "y" or goedkeuring == "n":
                cur.execute("INSERT INTO goedkeuring (berichtid, moderatorid, datum, tijd, goedkeuring) VALUES(%s, %s, %s, %s, %s);", (bericht[0], activeModerator[0], date, time, goedkeuring))
                conn.commit()
            elif goedkeuring == "break" or goedkeuring == "exit" or goedkeuring == "stop":
                return
            else:
                print("niet een juiste invoer")



approvingMessage()

cur.close()
conn.close()
