import PySimpleGUI as sg
import os
import sys
import glob
import pyautogui as pag
import time
import re
from random import randrange

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def img(image, path):
    """Creates a shorter code for easier readability

    Args:
        image (str): name of the image
        path (str): name of the path in with the image is located

    Returns:
        str: absolute path of the file
    """
    return resource_path(os.path.join(f'{path}', f'{image}.png'))

def locate_click(path):
    """finds the location of a given image path

    Args:
        path (str): path to the given image
    """
    pag.leftClick(pag.locateCenterOnScreen(path, confidence=0.6))
def random_champ():
    return champions_dis[randrange(len(champions_dis))]

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
    """A magick function in with all of the automation happens

    Args:
        ban (str): name of the champion to ban
        pick (str): name of the champion to pick
    """
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
    searched = False
    searched_1 = False
    selected = False
    locked = False
    done = False
    
    while done == False and reset == False:
        
        while accepted == False and reset == False:
            window['process'].update('Accepting...')
            if pag.locateOnScreen(resource_path(img('accept', 'utils')), confidence=0.8) != None:
                locate_click(resource_path(img('accept', 'utils')))
                accepted = True
                window['process'].update('Accepted')
                time.sleep(30)
            time.sleep(2)
            
        while searched == False and reset == False:
            window['process'].update('Searching...')
            if pag.locateOnScreen(resource_path(img('info', 'utils')), confidence=0.8) != None:
                locate_click(resource_path(img('search', 'utils')))
                if ban != 'none':   
                    pag.write(f'{ban}')
                    searched = True
                elif ban == 'none':
                    searched = True
                time.sleep(1)
                
        while selected == False and reset == False:
            window['process'].update('Selecting...')
            if pag.locateOnScreen(img(ban, 'Champions'), confidence=0.6) != None:
                time.sleep(1)
                locate_click(img(ban, 'Champions'))
                selected = True
            time.sleep(1)
                
        while banned == False and reset == False:
            window['process'].update('Banning...')
            if pag.locateOnScreen(resource_path(img('ban', 'utils')), confidence=0.8) != None:
                locate_click(resource_path(img('ban', 'utils')))
                banned = True
                window['process'].update("Banned")
                time.sleep(3)
                
        while searched_1 == False and reset == False:
            window['process'].update('Searching...')
            if pag.locateOnScreen(resource_path(img('info_1', 'utils')), confidence=0.8) != None:
                locate_click(resource_path(img('search', 'utils')))
                if pick != 'random':
                    pag.write(f'{pick}')
                    searched_1 = True
                elif pick == 'random':
                    searched_1 = True
                time.sleep(1)
                
        while picked == False and reset == False:
            window['process'].update('Picking...')
            if pag.locateOnScreen(img(pick, 'Champions'), confidence=0.8) != None:
                locate_click(img(pick, 'Champions'))
                picked = True
                
        while locked == False and reset == False:
            window['process'].update('Locking...')
            if pag.locateOnScreen(resource_path(img('lock', 'utils')), confidence=0.8) != None:
                locate_click(resource_path(img('lock', 'utils')))
                locked = True
                done = True
                window['process'].update('Done')

# Default values for ban and pick
pick = 'random'
ban = 'none'

champions_sel = glob.glob(resource_path(img('*', 'Champions')))
champions_dis = []
for champ in champions_sel: # Replaces log name of the absolute path of the images to names of champions
    champions_dis.append(re.search("[a-z]*\.png", champ, flags = re.I)[0].replace('.png', ''))

sg.theme('Dark')

layout = [
    [sg.Text('What champion do you want do ban? \nDefault is none.'), sg.Text('What champion do you want to pick? \nDefault is random.')],
    [sg.Listbox(champions_dis, size=(30,20), key='bans', enable_events=True), sg.Listbox(champions_dis, size=(30,20), key='picks', enable_events=True)],
    [sg.Input('', size=(30), key='ban', enable_events=True), sg.Input('', size=(30), key='pick', enable_events=True)],
    [sg.Image(img(ban, 'Champions'), key='ban_img', enable_events=True), sg.Image(img(pick, 'Champions'), key='pick_img', enable_events=True), 
        sg.Checkbox('Auto Accept', True, key = 'auto_accept'), sg.Checkbox('Auto Ban', True, key = 'auto_ban'), sg.Checkbox('Auto Pick', True, key = 'auto_pick')],
    [sg.Ok(), sg.Cancel(), sg.Button('Reset', key='Reset'), sg.Radio('Random in game', 1, True, key = 'in_game'), sg.Radio('Random in program', 1, False, key = 'in_app')],
    [sg.Text('Waiting...', key='process', enable_events=True)]
]

window = sg.Window('LoL Auto-ab&p', layout, icon=resource_path(os.path.join('utils', 'icon.ico')))

while True: # Checking what button was prest
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
        window['ban_img'].update(img(ban, 'Champions'))
    elif event == 'picks':
        pick = str(values['picks']).replace('\'', '').replace('[', '').replace(']', '')
        window['pick_img'].update(img(pick, 'Champions'))
        
    if event == 'Ok':
        if values['auto_accept'] == False:
            accepted = True
        if values['auto_ban'] == False:
            banned = True
            searched = True
            selected = True
        if values['auto_pick'] == False:
            picked = True
            searched_1 = True
            locked = True
        if values['in_game'] == True:
            window.perform_long_operation(lambda: automatic(ban, pick), 'process')
        if values['in_app'] == True:
            window.perform_long_operation(lambda: automatic(ban, random_champ()), 'process')
        
    if event == 'Reset':
        reset = True
        window['process'].update('Waiting...')
        window['ban_img'].update(img('none', 'Champions'))
        window['pick_img'].update(img('random', 'Champions'))
        window['auto_accept'].update(True)
        window['auto_ban'].update(True)
        window['auto_pick'].update(True)
        window['ban'].update('')
        window['pick'].update('')
        accepted = False
        banned = False
        searched = False
        selected = False
        picked = False
        searched_1 = False
        locked = False
        
        

window.close()
