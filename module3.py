import PySimpleGUI as sg
import psycopg2
import requests
import random
import time

date = time.strftime("%Y/%m/%d") #datum van vandaag

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

def getWeatherTable(location):
    #hier heb ik een try except gebruikt voor als er geen wifi of verbind is met de api. als er geen verbind is dan geeft die N/A terug
    try:
        apikey = '7be294282644886c765523cec21b15ad' #api key
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location},nl&units=metric&appid={apikey}") #hier haalt die de gegevens op. de variable location geeft de random gekozen locatie mee
        responseData = response.json()
        icon = responseData['weather'][0]['icon'] #haalt het icon op
        desc = responseData['weather'][0]['description'] #haalt de omschrijving op
        temp = round(responseData['main']['temp']) #haalt de temperatuur op
        feelsLike = round(responseData['main']['feels_like']) #haalt de gevoelstemperatuur
        humid = round(responseData['main']['humidity']) #haalt de luchtvochtigheid
        tempMin = round(responseData['main']['temp_min']) #haalt de minimale temp op
        tempMax = round(responseData['main']['temp_max']) #haalt de maximale temp op
        wind = round(responseData['wind']['speed']) #haalt die windsnelheid op

        toprow = ['Omschrijving', 'Temperatuur', 'Gevoelstemperatuur', 'Min', 'Max', 'Luchtvochtigheid', 'Wind'] #bovenregel van de tabel
        rows = [[' '], [' '], [' '], [' '],
                [desc, temp, feelsLike, humid, tempMin, tempMax, wind]] #zet hier alle waarde neer

        tableLayout = [[sg.Text(f"Weer in {location}", font=("Monsterrat", 25, "bold"), background_color=nsBlauw)], #laat zien welke stad het is
                        [sg.Image(filename=f'weather/{icon}@2x.png', background_color=nsBlauw,), #plaatje
                         sg.Table(values=rows, headings=toprow, justification='center', header_font=("Monsterrat", 14, "bold"), #de tabel
                                  header_text_color="white", selected_row_colors=("white", nsBlauw), expand_x=True,
                                  background_color=nsBlauw, hide_vertical_scroll=True, border_width=0, header_border_width=0, header_background_color=nsBlauw)]]
        return tableLayout
    except:
        return 'N/A ' #als er geen verbinding is geeft die dit terug

stationServices = [] #stopt hier alle stationservices in

def getStationServices():
    cur.execute("SELECT * FROM station_service WHERE station_city = %s", (location,))
    stationService = cur.fetchall() #haalt alle services op waar het station overeenkomt met de random gekozen locatie

    if stationService[0][2] == True:
        stationServices.append([sg.Image('ns/img_lift.png', size=(80, 80), subsample=2, background_color="white"),
                                sg.Text('Lift', background_color="white", text_color="black")]) #lift
    if stationService[0][3] == True:
        stationServices.append([sg.Image('ns/img_ovfiets.png', size=(80, 80), subsample=2, background_color="white"),
                                sg.Text('OV Fiets', background_color="white", text_color="black")]) #OV Fiets
    if stationService[0][4] == True:
        stationServices.append([sg.Image('ns/img_toilet.png', size=(80, 80), subsample=2, background_color="white"),
                                sg.Text('Toilet', background_color="white", text_color="black")]) #toilet
    if stationService[0][5] == True:
        stationServices.append([sg.Image('ns/img_pr.png', size=(80, 80), subsample=2, background_color="white"),
                                sg.Text('P+R', background_color="white", text_color="black")]) #P+R

getStationServices()

cur.execute("SELECT * FROM bericht JOIN beoordeling ON bericht.berichtId = beoordeling.berichtId WHERE beoordeling.beoordeling = True ORDER BY beoordeling.berichtId DESC LIMIT 5") #haalt de laatste 5 berichten op in db

topLayout = [[sg.Image('ns/ns.png', size=(100,100), subsample=(5), background_color=nsGeel), #ns logo
     sg.Push(background_color=nsGeel), #duwt dit element naar de andere kant van het scherm
     sg.Column(layout=[
         [sg.Text(f"\n {getWeather(location)}°C   {location}", size=(16, 3), background_color=nsBlauw,
              font=("Montserrat", 22), justification="c"), #het weer en locatie
          sg.VSeparator(), #verticale streep
          sg.Text(f'\n {date}', size=(10, 3), background_color=nsBlauw,
              font=("Montserrat", 22), justification="c"), #datum van vandaag
          sg.Text('', size=(7, 3), font=('Montserrat', 22), background_color=nsBlauw,
                 justification='c', key='-CLOCK-')], #actuele tijd
    ], background_color=nsBlauw, key="_COLUMN_")]]

layoutBerichten = [] #doet de laatste 5 berichten in met de layoutBerichten

for bericht in cur.fetchall(): #laat de berichten 1 voor 1 langs komen
    topText = f"{bericht[1]} | {bericht[2]} | {bericht[3]}" #top regel met naam, datm en tijd, en locatie
    layoutBerichten.append([ #doet die in de list
        sg.Column(layout=[
            [sg.Text(topText, background_color="white", text_color="grey")],
            [sg.Text(" ", size=(4, 0), background_color="white", text_color="black"),
             sg.Multiline(default_text=bericht[4], size=(50, 10), no_scrollbar=True, background_color="white",
                          border_width=0, disabled=True)] #hier wordt het bericht neergezet
        ], background_color="white", size=(700, 90), pad=(0, 0))
    ])

colRight = [
    [sg.Text(f"Station {location} faciliteiten", background_color="white", text_color="black", font=("Montserrat", 20))],
    [sg.Column(stationServices, background_color="white")] #station services
]

colBottom = [[
    sg.Column(getWeatherTable(location), justification="c", background_color=nsBlauw, expand_x=True)], #tabel met weer info
]

layout = [
    [topLayout],
    [sg.Column(layout=layoutBerichten, background_color=nsGeel, size=(700, 450)),
     sg.Column(layout=colRight, background_color="white", size=(700, 450))], #hier wordt de berichten column en het service tabel naast elkaar gezet
    [colBottom],
]

font = ("Montserrat", 13) #font style en size

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

        currentTime = time.strftime('\n %H:%M')  # actuele tijd
        window['-CLOCK-'].update(currentTime)  # update de actuele tijd iedere seconde(door de timeout op line 100)

cur.close()  # cursor closed van de db
conn.close()  # connection closed van de db
window.close()  # window closed van de GUI
