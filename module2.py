import psycopg2
import time
import PySimpleGUI as sg
import random
import requests

date = time.strftime("%Y/%m/%d")
nsGeel = "#FFC917"
nsBlauw = "#003082"

DB_HOST = "localhost"
DB_NAME = "stationzuil"
DB_USER = "postgres"
DB_PASS = "Koeskoes123123!"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

def getStation():
    with open('stations.txt', 'r') as stationFile:
        return random.choice(stationFile.read().splitlines())

location = getStation()

def getWeather(location):
    try:
        apikey = '7be294282644886c765523cec21b15ad'
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location},nl&units=metric&appid={apikey}")
        responseData = response.json()
        return round(responseData['main']['temp'])
    except:
        return 'N/A'

def approvingMessage(name, email):
    cur.execute("SELECT * FROM bericht WHERE NOT EXISTS (SELECT beoordeling.berichtid FROM beoordeling WHERE bericht.berichtid = beoordeling.berichtid)")
    berichten = cur.fetchall()

    if not berichten:
        sg.popup(f"Geen nieuwe berichten!\n", button_color=nsGeel, background_color=nsBlauw, no_titlebar=True)
    else:
        for bericht in berichten:
            berichtId = bericht[0]
            cur.execute("SELECT * from moderator WHERE naam = %s AND email = %s", (name, email))
            activeModerators = cur.fetchall()
            for activeModerator in activeModerators:
                moderatorId = activeModerator[0]
                beoordeling = sg.popup_yes_no(f'\n\n\n\tBericht: {bericht[4]}\n\tWilt u dit bericht goedkeuren?\t\n\n\n', button_color=nsGeel, background_color=nsBlauw, text_color="white", no_titlebar=True)
                if beoordeling == "Yes":
                    cur.execute(
                        "INSERT INTO beoordeling (berichtid, moderatorid, datum, beoordeling) VALUES(%s, %s, %s, %s);",
                        (berichtId, moderatorId, date, True))
                    conn.commit()
                elif beoordeling == "No":
                    cur.execute(
                        "INSERT INTO beoordeling (berichtid, moderatorid, datum, beoordeling) VALUES(%s, %s, %s, %s);",
                        (berichtId, moderatorId, date, False))
                    conn.commit()
                else:
                    print("niet een juiste invoer")

# totaal aantal berichten

topLayout = [[sg.Image('ns.png', size=(100, 100), subsample=(5), background_color=nsGeel),
               sg.Push(background_color=nsGeel),
               sg.Column(layout=[
                   [sg.Text(f"\n {getWeather(location)}°C   {location}", size=(16, 3), background_color=nsBlauw,
                            font=("Montserrat", 22), justification="c"),
                    sg.VSeparator(),
                    sg.Text(f'\n {date}', size=(10, 3), background_color=nsBlauw,
                            font=("Montserrat", 22), justification="c"),
                    sg.Text('', size=(7, 3), font=('Montserrat', 22), background_color=nsBlauw,
                            justification='c', key='-CLOCK-')],
               ], background_color=nsBlauw)]]

cur.execute("SELECT * FROM bericht WHERE NOT EXISTS (SELECT beoordeling.berichtid FROM beoordeling WHERE bericht.berichtid = beoordeling.berichtid)")
berichten = cur.fetchall()

layout = [
    [topLayout],
    [sg.T('Uw naam:', key='-OUT-', expand_x=True, justification='center', background_color=nsBlauw)],
    [sg.Input('', enable_events=True, key='-NAME-', expand_x=True, justification='center')],
    [sg.T('Uw e-mail:', key='-OUT-', expand_x=True, justification='center', background_color=nsBlauw)],
    [sg.Input('', enable_events=True, key='-EMAIL-', size=(5, 5), expand_x=True, justification='center')],
    [sg.Push(background_color=nsGeel), sg.Button('Inloggen', button_color=nsBlauw),
     sg.Push(background_color=nsGeel)]
]

font = ("Montserrat", 18)

window = sg.Window(
    "Stationszuil",
    layout,
    background_color=nsGeel,
    font=font,
    no_titlebar=True
).Finalize()
window.Maximize()

while True:
    event, values = window.read(timeout=1000)  # Update every 1000 milliseconds (1 second)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Inloggen':
        name = values['-NAME-']
        email = values['-EMAIL-']
        approvingMessage(name, email)

    currentTime = time.strftime('\n %H:%M')
    window['-CLOCK-'].update(currentTime)

cur.close()
conn.close()
window.close()
