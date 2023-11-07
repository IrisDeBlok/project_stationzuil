import psycopg2
import time
import PySimpleGUI as sg
import random
import requests

date = time.strftime("%Y/%m/%d") #datum van vandaag
today = time.strftime("%d/%m/%Y")

#kleuren
nsGeel = "#FFC917"
nsBlauw = "#003082"

#db connectie
DB_HOST = "13.93.31.162"
DB_NAME = "stationszuil"
DB_USER = "postgres"
DB_PASS = "Hallo123"

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

def approvingMessage(name, email):
    cur.execute("SELECT * FROM bericht WHERE NOT EXISTS (SELECT beoordeling.berichtid FROM beoordeling WHERE bericht.berichtid = beoordeling.berichtid)")
    berichten = cur.fetchall() #alle berichten uit de berichtentabel worden hier opgehaald die niet overeenkomen met een id in de beoordeling tabel

    if not berichten: #dit wordt laten zien als er geen berichten meer zijn die nagekeken hoeven worden
        sg.popup(f"Geen nieuwe berichten!\n", button_color=nsGeel, background_color=nsBlauw, no_titlebar=True)
    else:
        for bericht in berichten: #laat alle berichten 1 voor 1 terug komen
            berichtId = bericht[0] #pakt het id
            cur.execute("SELECT * from moderator WHERE naam = %s AND email = %s", (name, email))
            activeModerators = cur.fetchall() #haalt alle moderators op waar de naam en email overeenkomen met de ingevoerde waarde
            for activeModerator in activeModerators: #laat alle moderators 1 voor 1 terug komen
                moderatorId = activeModerator[0] #pakt het id
                beoordeling = sg.popup_yes_no(f'\n\n\n\tBericht: {bericht[4]}\n\tWilt u dit bericht goedkeuren?\t\n\n\n',
                                              button_color=nsGeel, background_color=nsBlauw, text_color="white", no_titlebar=True) #laat het bericht zien die moet worden goedgekeurd
                if beoordeling == "Yes":
                    cur.execute(
                        "INSERT INTO beoordeling (berichtid, moderatorid, datum, beoordeling) VALUES(%s, %s, %s, %s);",
                        (berichtId, moderatorId, date, True)) #query
                    conn.commit() #voert query uit
                elif beoordeling == "No":
                    cur.execute(
                        "INSERT INTO beoordeling (berichtid, moderatorid, datum, beoordeling) VALUES(%s, %s, %s, %s);",
                        (berichtId, moderatorId, date, False)) #query
                    conn.commit() #voert query uit

topLayout = [    [sg.Image('ns/ns.png', size=(100,100), subsample=(5), background_color=nsGeel), #ns logo
     sg.Push(background_color=nsGeel), #duwt dit element naar de andere kant van het scherm
     sg.Column(layout=[
         [sg.Text(f"\n {getWeather(location)}°C   {location}", size=(16, 3), background_color=nsBlauw,
              font=("Montserrat", 22), justification="c"), #het weer en locatie
          sg.VSeparator(), #verticale streep
          sg.Text(f'\n {today}', size=(10, 3), background_color=nsBlauw,
              font=("Montserrat", 22), justification="c"), #datum van vandaag
          sg.Text('', size=(7, 3), font=('Montserrat', 22), background_color=nsBlauw,
                 justification='c', key='-CLOCK-')], #actuele tijd
    ], background_color=nsBlauw, key="_COLUMN_")]]

layout = [
    [topLayout],
    [sg.T('Uw naam:', expand_x=True, justification='center', background_color=nsBlauw)], #naam input label
    [sg.Input('', enable_events=True, key='-NAME-', expand_x=True, justification='center')], #naam input
    [sg.T('Uw e-mail:', expand_x=True, justification='center', background_color=nsBlauw)], #email input label
    [sg.Input('', enable_events=True, key='-EMAIL-', size=(5, 5), expand_x=True, justification='center')], #email input
    [sg.Push(background_color=nsGeel), sg.Button('Inloggen', button_color=nsBlauw), sg.Push(background_color=nsGeel)] #duwt dit element naar het midden
]

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
    if event == sg.WIN_CLOSED:
        break #window sluit als die gestopt wordt
    if event == 'Inloggen':
        name = values['-NAME-']  #haalt die de waarde van het element met de key NAME op
        email = values['-EMAIL-']  #haalt die de waarde van het element met de key MESSAGE op
        approvingMessage(name, email) #stuurt de variable naar de functie

    currentTime = time.strftime('\n %H:%M') #actuele tijd
    window['-CLOCK-'].update(currentTime) #update de actuele tijd iedere seconde(door de timeout op line 100)

cur.close() #cursor closed van de db
conn.close() #connection closed van de db
window.close() #window closed van de GUI
