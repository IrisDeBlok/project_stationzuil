import PySimpleGUI as sg
import psycopg2
import requests
import random

DB_HOST = "localhost"
DB_NAME = "stationzuil"
DB_USER = "postgres"
DB_PASS = "Koeskoes123123!"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

def getStation():
    with open('stations.txt', 'r') as station_file:
        return random.choice(station_file.read().splitlines())


def getWeather(location):
    apikey = '7be294282644886c765523cec21b15ad'
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location},nl&units=metric&appid={apikey}")
    response_data = response.json()
    return round(response_data['main']['temp'])



cur.execute(
    "SELECT * FROM bericht JOIN beoordeling ON bericht.berichtId = beoordeling.berichtId WHERE beoordeling.beoordeling = True ORDER BY beoordeling.berichtId DESC LIMIT 5")

sg.set_options(font=("Arial Bold", 14))
station = getStation()

layout_berichten = []

for bericht in cur.fetchall():
    layout_berichten.append([
        [
            sg.Column([
                [sg.Text(bericht[1]), sg.Text(bericht[2]), sg.Text(bericht[3])],
                [sg.Text(bericht[4])]
            ], background_color="white", size=(100, 100), expand_x=True)
        ]
    ])

layout = [
    [sg.Text(getWeather(station)), sg.Text(station)],
    layout_berichten
]

window = sg.Window(
    "Stationszuil",
    layout,
    background_color="#FFC917",
    # no_titlebar=True
).Finalize()
window.Maximize()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()

cur.close()
conn.close()
