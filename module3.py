import PySimpleGUI as sg
import psycopg2
import requests
import random
import time

DB_HOST = "localhost"
DB_NAME = "stationzuil"
DB_USER = "postgres"
DB_PASS = "Koeskoes123123!"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()
cur.execute(
    "SELECT * FROM bericht JOIN beoordeling ON bericht.berichtId = beoordeling.berichtId WHERE beoordeling.beoordeling = True ORDER BY beoordeling.berichtId DESC LIMIT 5")


def getStation():
    with open('stations.txt', 'r') as station_file:
        return random.choice(station_file.read().splitlines())


station = getStation()


def getWeather(location):
    apikey = '7be294282644886c765523cec21b15ad'
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={location},nl&units=metric&appid={apikey}")
    response_data = response.json()
    return round(response_data['main']['temp'])


layout_berichten = []

for bericht in cur.fetchall():
    topText = f"{bericht[1]} / {bericht[2]} / {bericht[3]}"
    layout_berichten.append([
        sg.Column(layout=[
            [sg.Text(topText, background_color="white", text_color="grey")],
            [sg.Text(" ", size=(4, 0), background_color="white", text_color="black"),
             sg.Multiline(default_text=bericht[4], size=(50, 10), no_scrollbar=True, background_color="white",
                          border_width=0, disabled=True)
             ]
        ], background_color="white", size=(700, 120), key="-COLUMN-")
    ])

layout = [
    [sg.Push("#FFC917"),
    sg.Text('', size=(7, 3), background_color="#003082",
                 justification='c', key='-CLOCK-'),
     sg.Text(f"\n{getWeather(station)}°C   {station}", background_color="#003082", size=(30, 3), justification="c")],
    [*layout_berichten, sg.Text(station)],
]

font = ("Montserrat", 13)

window = sg.Window(
    "Stationszuil",
    layout,
    background_color="#FFC917",
    font=font
    # no_titlebar=True
).Finalize()
window.Maximize()
column_element = window['-COLUMN-']
while True:
    event, values = window.read(timeout=1000)
    if event == sg.WIN_CLOSED:
        break
    current_time = time.strftime('\n %H:%M')
    window['-CLOCK-'].update(current_time)
    window['-COLUMN-'].update(layout_berichten)

window.close()

cur.close()
conn.close()
