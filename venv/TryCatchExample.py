
from pathlib import Path

data_folder = Path("C:/Users/lukas.kapust/Desktop/java test/possession/testen/LevelFolder")

file_to_open = data_folder / "testDatei.txt"
y = 5
eval(input())
try:
   # y = 2
    # print(x)
    data = open(file_to_open)
    #data.write("dwadawdaw")
   # y = 7
except:
    print("Error")
finally:
    print("finally")
    print(y)

