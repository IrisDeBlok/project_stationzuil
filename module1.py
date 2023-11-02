import random
import requests
import psycopg2
import time
import PySimpleGUI as sg

date = time.strftime("%Y/%m/%d %H:%M")
today = time.strftime("%d/%m/%Y")
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

layout = [
    [sg.Image('ns.png', size=(100,100), subsample=(5), background_color=nsGeel),
     sg.Push(background_color=nsGeel),
     sg.Column(layout=[
         [sg.Text(f"\n {getWeather(location)}°C   {location}", size=(16, 3), background_color=nsBlauw,
              font=("Montserrat", 22), justification="c"),
          sg.VSeparator(),
          sg.Text(f'\n {today}', size=(10, 3), background_color=nsBlauw,
              font=("Montserrat", 22), justification="c"),
          sg.Text('', size=(7, 3), font=('Montserrat', 22), background_color=nsBlauw,
                 justification='c', key='-CLOCK-')],
    ], background_color=nsBlauw, key="_COLUMN_")],
    [sg.T('Uw naam:', key='-OUT-', expand_x=True, justification='center', background_color=nsBlauw)],
    [sg.Input('', enable_events=True, key='-NAME-', expand_x=True, justification='center')],
    [sg.T('Uw bericht:', key='-OUT-', expand_x=True, justification='center', background_color=nsBlauw)],
    [sg.Multiline('', enable_events=True, key='-MESSAGE-', size=(5, 5), no_scrollbar=True, expand_x=True, justification='c')],
    [sg.T("*Dit bericht wordt nagekeken door een moderator en mag bestaan uit maximaal 140 karakters", expand_x=True, justification="c", background_color=nsGeel, text_color="black", font=("Montserrat", 10))],
    [sg.Push(background_color=nsGeel), sg.Button('Verzenden', button_color=nsBlauw), sg.Push(background_color=nsGeel)]
]

maxChars = 140
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
    name = values['-NAME-']
    message = values['-MESSAGE-']
    x = name.capitalize()
    y = message.capitalize()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Verzenden':
        if len(name) == 0 or len(message) == 0:
            sg.popup("U moet beide velden invullen", button_color=nsGeel, background_color=nsBlauw, text_color="white", no_titlebar=True)
        else:
            cur.execute("INSERT INTO bericht(naam, datum, locatie, bericht) VALUES(%s, %s, %s, %s);", (x, date, location, y))
            conn.commit()
            window['-NAME-'].update('')
            window['-MESSAGE-'].update('')
        input_text = values['-MESSAGE-']
        input_text = input_text[:maxChars]

    currentTime = time.strftime('\n %H:%M')
    window['-CLOCK-'].update(currentTime)

cur.close()
conn.close()
window.close()
