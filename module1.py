import random
import requests
import psycopg2
import time
import PySimpleGUI as sg

#datum en tijd
date = time.strftime("%Y/%m/%d %H:%M")
today = time.strftime("%d/%m/%Y")

#kleuren
nsGeel = "#FFC917"
nsBlauw = "#003082"

#db connectie
DB_HOST = "localhost"
DB_NAME = "stationzuil"
DB_USER = "postgres"
DB_PASS = "Koeskoes123123!"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

#random station
def getStation():
    with open('stations.txt', 'r') as stationFile: #opent het bestand
        return random.choice(stationFile.read().splitlines()) #leest het gehele bestand door en split alle lijnen in losse worden

location = getStation() #het random station variable

#api call voor het weer
def getWeather(location):
    #hier heb ik een try except gebruikt voor als er geen wifi of verbind is met de api. als er geen verbind is dan geeft die N/A terug
    try:
        apikey = '7be294282644886c765523cec21b15ad' #api key
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location},nl&units=metric&appid={apikey}") #hier haalt die de gegevens op. de variable location geeft de random gekozen locatie mee
        responseData = response.json()
        return round(responseData['main']['temp']) #haalt de temperatuur op
    except:
        return 'N/A' #als er geen verbinding is geeft die dit terug

#GUI layout
layout = [
    [sg.Image('ns/ns.png', size=(100,100), subsample=(5), background_color=nsGeel), #ns logo
     sg.Push(background_color=nsGeel), #duwt dit element naar de andere kant van het scherm
     sg.Column(layout=[
         [sg.Text(f"\n {getWeather(location)}°C   {location}", size=(16, 3), background_color=nsBlauw,
              font=("Montserrat", 22), justification="c"), #het weer en locatie
          sg.VSeparator(), #verticale streep
          sg.Text(f'\n {today}', size=(10, 3), background_color=nsBlauw,
              font=("Montserrat", 22), justification="c"), #datum van vandaag
          sg.Text('', size=(7, 3), font=('Montserrat', 22), background_color=nsBlauw,
                 justification='c', key='-CLOCK-')], #actuele tijd
    ], background_color=nsBlauw, key="_COLUMN_")],
    [sg.T('Uw naam:', key='-OUT-', expand_x=True, justification='center', background_color=nsBlauw)], #naam input label
    [sg.Input('', enable_events=True, key='-NAME-', expand_x=True, justification='center')], #naam input
    [sg.T('Uw bericht:', key='-OUT-', expand_x=True, justification='center', background_color=nsBlauw)], #bericht input label
    [sg.Multiline('', enable_events=True, key='-MESSAGE-', size=(5, 5), no_scrollbar=True, expand_x=True, justification='c')], #bericht input
    [sg.T("*Dit bericht wordt nagekeken door een moderator en mag bestaan uit maximaal 140 karakters", expand_x=True, justification="c",
          background_color=nsGeel, text_color="black", font=("Montserrat", 10))], #tekst wat aangeeft wat er met het bericht gebeurt
    [sg.Push(background_color=nsGeel), sg.Button('Verzenden', button_color=nsBlauw), sg.Push(background_color=nsGeel)] #duwt dit element naar het midden
]

maxChars = 140 #maximale karakters
font = ("Montserrat", 18) #font style en size

window = sg.Window(
    "Stationszuil",
    layout,
    background_color=nsGeel,
    font=font,
    no_titlebar=True
).Finalize() #maakt het scherm van de GUI elementen
window.Maximize() #full screen

while True:
    event, values = window.read(timeout=1000)  #Update iedere 1000 milliseconden
    name = values['-NAME-'] #haalt die de waarde van het element met de key NAME op
    message = values['-MESSAGE-'] #haalt die de waarde van het element met de key MESSAGE op
    x = name.capitalize() #maakt die van het eerste letter een hoofdletter
    y = message.capitalize() #maakt die van het eerste letter een hoofdletter
    if event == sg.WIN_CLOSED:
        break #window sluit als die gestopt wordt
    if event == 'Verzenden': #op de knop verzenden wordt geklikt
        if len(name) == 0: #naam heeft geen lengte
            cur.execute("INSERT INTO bericht(naam, datum, locatie, bericht) VALUES(%s, %s, %s, %s);",
                        ('Anoniem', date, location, y)) #query
            conn.commit() #voer de query uit
            window['-NAME-'].update('') #veld wordt geleegd
            window['-MESSAGE-'].update('') #veld wordt geleegd
        elif len(message) == 0: #bericht geen lengte
            sg.popup("U moet het bericht veld invullen", button_color=nsGeel, background_color=nsBlauw, text_color="white", no_titlebar=True) #laat de persoon weten dat ze het bericht moeten invullen
        else:
            cur.execute("INSERT INTO bericht(naam, datum, locatie, bericht) VALUES(%s, %s, %s, %s);", (x, date, location, y)) #query
            conn.commit() #voer de query uit
            window['-NAME-'].update('') #veld wordt geleegd
            window['-MESSAGE-'].update('') #veld wordt geleegd
        input_text = values['-MESSAGE-']
        input_text = input_text[:maxChars] #message veld mag niet langer zijn dan de variable maxChars
        #als het bericht langer is dan maxChars, dan worden alleen 140 karakters opgestuurd naar de db

    currentTime = time.strftime('\n %H:%M') #actuele tijd
    window['-CLOCK-'].update(currentTime) #update de actuele tijd iedere seconde(door de timeout op line 77)

cur.close() #cursor closed van de db
conn.close() #connection closed van de db
window.close() #window closed van de GUI
