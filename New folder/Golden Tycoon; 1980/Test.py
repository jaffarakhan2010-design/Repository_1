from random import randint
from datetime import datetime
a = 1
h = datetime.now().hour
m = datetime.now().minute
p = "am"
if h > 12:
    h -= 12
    p = "pm"

debt_list = [100, 200, 300]
interest_list = [3,52,2]
text_list = ["H","E", "L", "L", "O"]

print(f"{h}:{m} {p}")

print(2 ** 6)

num = 0
nameo = ''
k = ''

for i in text_list:
    nameo += text_list[num]
    print(nameo)
    num += 1

if k:
    print("True")
else: print("False")


#for i in range(20):
#    print(randint(1,100))

print(len(debt_list))

equity_own = 100
equity_num = 30
equity_list = []
list_math = [145, 70, 82]

equity_own -= equity_num
equity_list.append(equity_num)
Tru = True
equity_num = 0

print(len(equity_list) - 1)

my_list = [10, 20, 30, 40, 50]
print(f"Original list: {my_list}")

my_list.append(False)
# Change the value at index 2 (which is 30) to 99
my_list[2] -= 99
print(f"Modified list: {my_list}")

ogage = int(input())
line = 0
for i in (my_list):
    print(14.7 + 13.8 + 14.1 + 15.8 + 25.2 + 42 + 74 + 80.5 + 74.9 + 49 + 28.9 + 14.9 )
print("------------------------------------------------------------------------------------------------")
while Tru:
    print(ogage, line)
    ogage = (ogage / 2) + 7
    line += 1
    if ogage == 14.0:
        Tru = False
        print(ogage, line)