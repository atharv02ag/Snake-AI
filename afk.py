import pyautogui as pag
import random
import time

#ran this script simultaneously because neat would not continue running if afk
#moves the cursor to a random location across the screen so the algorithm can run afk without stopping
while True:
    x = random.randint(600,700)
    y = random.randint(200,600)
    pag.moveTo(x,y,0.5)
    time.sleep(1)