import PySimpleGUI as sg
import psycopg2
import requests
import random
import time

date = time.strftime("%d/%m/%Y")
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

station = getStation()

def getWeather(location):
    try:
        apikey = '7be294282644886c765523cec21b15ad'
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location},nl&units=metric&appid={apikey}")
        responseData = response.json()
        return round(responseData['main']['temp'])
    except:
        return 'N/A '

def getWeatherTable(location):
    try:
        apikey = '7be294282644886c765523cec21b15ad'
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location},nl&units=metric&appid={apikey}")
        responseData = response.json()
        icon = responseData['weather'][0]['icon']
        desc = responseData['weather'][0]['description']
        temp = round(responseData['main']['temp'])
        feelsLike = round(responseData['main']['feels_like'])
        humid = round(responseData['main']['humidity'])
        tempMin = round(responseData['main']['temp_min'])
        tempMax = round(responseData['main']['temp_max'])
        wind = round(responseData['wind']['speed'])

        toprow = ['Omschrijving', 'Temperatuur', 'Voelt als', 'Min', 'Max', 'Vochtigheid', 'Wind']
        rows = [[' '], [' '], [' '], [' '],
                [desc, temp, feelsLike, humid, tempMin, tempMax, wind]]

        tableLayout = [[sg.Text(f"Weer in {station}", font=("Monsterrat", 25, "bold"), background_color=nsBlauw)],
                        [sg.Image(filename=f'weather/{icon}@2x.png', background_color=nsBlauw,),
                         sg.Table(values=rows, headings=toprow, justification='center', header_font=("Monsterrat", 14, "bold"),
                                  header_text_color="white", selected_row_colors=("white", nsBlauw), expand_x=True,
                                  background_color=nsBlauw, hide_vertical_scroll=True, border_width=0, header_border_width=0, header_background_color=nsBlauw)]]
        return tableLayout
    except:
        return 'N/A '

stationServices = []

def getStationServices():
    cur.execute("SELECT * FROM station_service WHERE station_city = %s", (station,))
    stationService = cur.fetchall()

    if stationService[0][2] == True:
        stationServices.append([sg.Image('ns/img_lift.png', size=(80, 80), subsample=2, background_color="white"), sg.Text('Lift', background_color="white", text_color="black")])
    if stationService[0][3] == True:
        stationServices.append([sg.Image('ns/img_ovfiets.png', size=(80, 80), subsample=2, background_color="white"), sg.Text('OV Fiets', background_color="white", text_color="black")])
    if stationService[0][4] == True:
        stationServices.append([sg.Image('ns/img_toilet.png', size=(80, 80), subsample=2, background_color="white"), sg.Text('Toilet', background_color="white", text_color="black")])
    if stationService[0][5] == True:
        stationServices.append([sg.Image('ns/img_pr.png', size=(80, 80), subsample=2, background_color="white"), sg.Text('P+R', background_color="white", text_color="black")])

getStationServices()

cur.execute("SELECT * FROM bericht JOIN beoordeling ON bericht.berichtId = beoordeling.berichtId WHERE beoordeling.beoordeling = True ORDER BY beoordeling.berichtId DESC LIMIT 5")

topLayout = [[sg.Image('ns.png', size=(100,100), subsample=(5), background_color=nsGeel),
     sg.Push(background_color=nsGeel),
     sg.Column(layout=[
         [sg.Text(f"\n {getWeather(station)}°C  {station}", size=(14, 3), background_color=nsBlauw,
              font=("Montserrat", 19), justification="c"),
          sg.VSeparator(),
          sg.Text(f'\n {date}', size=(9, 3), background_color=nsBlauw,
              font=("Montserrat", 19), justification="c"),
          sg.Text('', size=(6, 3), font=('Montserrat', 19), background_color=nsBlauw,
                 justification='c', key='-CLOCK-')],
    ], background_color=nsBlauw)]]

layoutBerichten = []

for bericht in cur.fetchall():
    topText = f"{bericht[1]} | {bericht[2]} | {bericht[3]}"
    layoutBerichten.append([
        sg.Column(layout=[
            [sg.Text(topText, background_color="white", text_color="grey")],
            [sg.Text(" ", size=(4, 0), background_color="white", text_color="black"),
             sg.Multiline(default_text=bericht[4], size=(50, 10), no_scrollbar=True, background_color="white",
                          border_width=0, disabled=True)
             ]
        ], background_color="white", size=(700, 90), key="-COLUMN-", pad=(0, 0))
    ])

colRight = [
    [sg.Text(f"Station {station} faciliteiten", background_color="white", text_color="black", font=("Montserrat", 20))],
    [sg.Column(stationServices, background_color="white")]
]

colBottom = [[
    sg.Column(getWeatherTable(station), justification="c", background_color=nsBlauw, expand_x=True)],
]

layout = [
    [topLayout],
    [sg.Column(layout=layoutBerichten, background_color=nsGeel, size=(700, 450)), sg.Column(layout=colRight, background_color="white", size=(700, 450), key="-COLUMN-")],
    [colBottom],
]

font = ("Montserrat", 13)

window = sg.Window(
    "Stationszuil",
    layout,
    background_color=nsGeel,
    font=font,
    no_titlebar=True
).Finalize()
window.Maximize()

while True:
    event, values = window.read(timeout=1000)
    if event == sg.WIN_CLOSED:
        break

    currentTime = time.strftime('\n %H:%M')
    window['-CLOCK-'].update(currentTime)

window.close()
cur.close()
conn.close()
