from datetime import datetime
import random

date = datetime.today()
today = date.strftime("%d-%m-%Y %H:%M")

locationList = [
                'Arnhem',
                'Almere',
                'Amersfoort',
                'Almelo',
                'Alkmaar',
                'Apeldoorn',
                'Assen',
                'Amsterdam',
                'Boxtel',
                'Breda',
                'Dordrecht',
                'Delft',
                'Deventer',
                'Enschede',
                'Gouda',
                'Groningen',
                'Den Haag',
                'Hengelo',
                'Haarlem',
                'Helmond',
                'Hoorn',
                'Heerlen',
                'Den Bosch',
                'Hilversum',
                'Leiden',
                'Lelystad',
                'Leeuwarden',
                'Maastricht',
                'Nijmegen',
                'Oss',
                'Roermond',
                'Roosendaal',
                'Sittard',
                'Tilburg',
                'Utrecht',
                'Venlo',
                'Vlissingen',
                'Zaandam',
                'Zwolle',
                'Zutphen'
                ]
location = random.choice(locationList)
name = input('Enter your name: ')
message = input('Message: ')

if len(name) == 0:
    print('Hello anoniem')
else:
    print('Hello ' + name)

print('Date:', today)
print('Location:', location)

if len(message) == 0:
    print('message needs to be filled')
elif len(message) > 140:
    print('message is too long. Keep it under 140 characters')
else:
    print('Message:', message)
