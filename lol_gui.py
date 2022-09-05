import PySimpleGUI as sg
import os
import sys
import glob
import pyautogui as pag
import time
import re

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def img(image):
    return resource_path(os.path.join('Champions', f'{image}.png'))

def locate_click(image):
    pag.leftClick(pag.locateCenterOnScreen(image, confidence=0.7))

reset = False
accepted = False
searched = False
searched_1 = False
selected = False
banned = False
picked = False
locked = False
done = False

def automatic(ban, pick):
    global reset
    global accepted
    global searched
    global searched_1
    global selected
    global banned
    global picked
    global locked
    global done

    reset = False
    # accepted = False
    searched = False
    searched_1 = False
    selected = False
    # banned = False
    # picked = False
    locked = False
    done = False
    while done == False and reset == False:
        
        while accepted == False and reset == False:
            window['process'].update('Accepting...')
            if pag.locateOnScreen(resource_path(os.path.join('utils', 'accept.png')), confidence=0.8) != None:
                locate_click(resource_path(os.path.join('utils', 'accept.png')))
                accepted = True
                window['process'].update('Accepted')
                time.sleep(30)
            time.sleep(2)
            
        while searched == False and reset == False:
            window['process'].update('Searching...')
            if pag.locateOnScreen(resource_path(os.path.join('utils', 'info.png')), confidence=0.8) != None:
                locate_click(resource_path(os.path.join('utils', 'search.png')))
                if ban != 'none':
                    pag.write(f'{ban}')
                searched = True
                time.sleep(2)
                
        while selected == False and reset == False:
            window['process'].update('Selecting...')
            if pag.locateOnScreen(img(ban), confidence=0.6) != None:
                locate_click(img(ban))
                selected = True
                time.sleep(1)
                
        while banned == False and reset == False:
            window['process'].update('Banning...')
            if pag.locateOnScreen(resource_path(os.path.join('utils', 'ban.png')), confidence=0.8) != None:
                locate_click(resource_path(os.path.join('utils', 'ban.png')))
                banned = True
                window['process'].update("Banned")
                time.sleep(3)
                
        while searched_1 == False and reset == False:
            window['process'].update('Searching...')
            if pag.locateOnScreen(resource_path(os.path.join('utils', 'info_1.png')), confidence=0.8) != None:
                locate_click(resource_path(os.path.join('utils', 'search.png')))
                if pick != 'random':
                    pag.write(f'{pick}')
                searched_1 = True
                time.sleep(2)
                
        while picked == False and reset == False:
            window['process'].update('Picking...')
            if pag.locateOnScreen(img(pick), confidence=0.8) != None:
                locate_click(img(pick))
                picked = True
                
        while locked == False and reset == False:
            window['process'].update('Locking...')
            if pag.locateOnScreen(resource_path(os.path.join('utils', 'lock.png')), confidence=0.8) != None:
                locate_click(resource_path(os.path.join('utils', 'lock.png')))
                locked = True
                done = True
                window['process'].update('Done')


pick = 'random'
ban = 'none'
champions_sel = glob.glob(resource_path(os.path.join('Champions', '*.png')))
champions_dis = []
for champ in champions_sel:
    champions_dis.append(re.search("[a-z]*\.png", champ, flags = re.I)[0].replace('.png', ''))

sg.theme('Dark')

layout = [
    [sg.Text('What champion do you want do ban? \nDefault is none.'), sg.Text('What champion do you want to pick? \nDefault is random.')],
    [sg.Listbox(champions_dis, size=(30,20), key='bans', enable_events=True), sg.Listbox(champions_dis, size=(30,20), key='picks', enable_events=True)],
    [sg.Input('', size=(30), key='ban', enable_events=True), sg.Input('', size=(30), key='pick', enable_events=True)],
    [sg.Image(img(ban), key='ban_img', enable_events=True), sg.Image(img(pick), key='pick_img', enable_events=True), 
        sg.Checkbox('Auto Accept', True, key = 'auto_accept'), sg.Checkbox('Auto Ban', True, key = 'auto_ban'), sg.Checkbox('Auto Pick', True, key = 'auto_pick')],
    [sg.Ok(), sg.Cancel(), sg.Button('Reset', key='Reset')],
    [sg.Text('Waiting...', key='process', enable_events=True)]
]

window = sg.Window('LoL Auto-ab&p', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    
    if values['ban'] != '':
        window['bans'].update([x for x in champions_dis if values['ban'] in x.lower()])
    else:
        window['bans'].update(champions_dis)
    if values['pick'] != '':
        window['picks'].update([x for x in champions_dis if values['pick'] in x.lower()])
    else:
        window['picks'].update(champions_dis)
        
    if event == 'bans':
        ban = str(values['bans']).replace('\'', '').replace('[', '').replace(']', '')
        window['ban_img'].update(img(ban))
    elif event == 'picks':
        pick = str(values['picks']).replace('\'', '').replace('[', '').replace(']', '')
        window['pick_img'].update(img(pick))
        
    if event == 'Ok':
        if values['auto_accept'] == False:
            accepted = True
        if values['auto_ban'] == False:
            banned = True
        if values['auto_pick'] == False:
            picked = True
        window.perform_long_operation(lambda: automatic(ban, pick), 'process')
        
    if event == 'Reset':
        reset = True
        window['process'].update('Waiting...')
        window['ban_img'].update(img('none'))
        window['pick_img'].update(img('random'))
        window['auto_accept'].update(True)
        window['auto_ban'].update(True)
        window['auto_pick'].update(True)
        accepted = False
        banned = False
        picked = False
        
        

window.close()
