# input()

# print('Enter Your Name')
# print(input())

x = input('Enter your name:')
mijnlijst = ['Uw bericht', x]

for word in mijnlijst:
    print(input(word))

if len(x) == 0:
    print('Hallo, anoniem')
else:
    print('Hello, ' + x)