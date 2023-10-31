import psycopg2
import time
import PySimpleGUI as sg
import random
import requests

date = time.strftime("%Y/%m/%d %H:%M")
#
DB_HOST = "localhost"
DB_NAME = "stationzuil"
DB_USER = "postgres"
DB_PASS = "Koeskoes123123!"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

def getStation():
    with open('stations.txt', 'r') as station_file:
        return random.choice(station_file.read().splitlines())

location = getStation()

def getWeather(location):
    apikey = '7be294282644886c765523cec21b15ad'
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={location},nl&units=metric&appid={apikey}")
    response_data = response.json()
    return round(response_data['main']['temp'])

#totaal aantal berichten

#threading timer

layout = [
    [sg.Push(background_color="#FFC917"),
     sg.Column(layout=[
         [sg.Text(f"\n {getWeather(location)}°C   {location}", size=(16, 3), background_color="#003082",
              font=("Montserrat", 22), justification="c"),
          sg.VSeparator(),
          sg.Text(f'\n {date}', size=(10, 3), background_color="#003082",
              font=("Montserrat", 22), justification="c"),
          sg.Text('', size=(7, 3), font=('Montserrat', 22), background_color="#003082",
                 justification='c', key='-CLOCK-')],
    ], background_color="#003082", key="_COLUMN_")],
    [sg.T('Uw naam:', key='-OUT-', expand_x=True, justification='center', background_color="#003082")],
    [sg.Input('', enable_events=True, key='-NAME-', expand_x=True, justification='center')],
    [sg.T('Uw e-mail:', key='-OUT-', expand_x=True, justification='center', background_color="#003082")],
    [sg.Input('', enable_events=True, key='-MESSAGE-', size=(5, 5), expand_x=True, justification='center')],
    [sg.Push(background_color="#FFC917"), sg.Button('Goedgekeurd', button_color="#003082"), sg.Button('Afgekeurd', button_color="#003082"), sg.Push(background_color="#FFC917")]
]

max_chars = 140
font = ("Montserrat", 18)

window = sg.Window(
    "Stationszuil",
    layout,
    background_color="#FFC917",
    font=font,
    # no_titlebar=True
).Finalize()
window.Maximize()
while True:
    event, values = window.read(timeout=1000)  # Update every 1000 milliseconds (1 second)
    name = values['-NAME-']
    message = values['-MESSAGE-']
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "goedgekeurd":
        cur.execute("INSERT INTO beoordeling (berichtid, moderatorid, datum, beoordeling) VALUES(%s, %s, %s, %s);",
                    (berichtId, moderatorId, date, True))
        conn.commit()
    elif event == "afgekeurd":
        cur.execute("INSERT INTO beoordeling (berichtid, moderatorid, datum, beoordeling) VALUES(%s, %s, %s, %s);",
                    (berichtId, moderatorId, date, False))
        conn.commit()
        break
    current_time = time.strftime('\n %H:%M')
    window['-CLOCK-'].update(current_time)
cur.close()
conn.close()
window.close()
