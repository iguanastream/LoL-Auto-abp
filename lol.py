import pyautogui as pag
import keyboard as kb
import time
import cv2
import os


def locate_click(image):
    pag.leftClick(pag.locateCenterOnScreen(image, confidence=0.7))


accepted = False
searched = False
selected = False #758,387
banned = False
picked = False
locked = False
done = False
champ = 'Udyr'

while done == False:
    
    while locked == False:
        # print('locking')
        if pag.locateOnScreen('lock.png', confidence=0.8) != None:
            locate_click('lock.png')
            locked = True
            done = True
            print('Done')
        while picked == False:
            # print('picking')
            if pag.locateOnScreen('random.png', confidence=0.8) != None:
                locate_click('random.png')
                picked = True
            while banned == False:
                # print('banning')
                if pag.locateOnScreen('ban.png', confidence=0.8) != None:
                    locate_click('ban.png')
                    banned = True
                    print("Banned")
                while selected == False:
                    # print('selecting')
                    if pag.locateOnScreen(os.path.join('Champions', f'{champ}.png'), confidence=0.7) != None:
                        locate_click(os.path.join('Champions', f'{champ}.png'))
                        selected = True
                        time.sleep(1)
                    while searched == False:
                        # print('searchig')
                        if pag.locateOnScreen('info.png', confidence=0.8) != None:
                            locate_click('search.png')
                            pag.write(f'{champ}')
                            searched = True
                            time.sleep(2)
                        while accepted == False:
                            # print('accepting')
                            if pag.locateOnScreen('accept.png', confidence=0.8) != None:
                                locate_click('accept.png')
                                accepted = True
                                print('Accepted')
                                time.sleep(30)
                            time.sleep(2)
                            
