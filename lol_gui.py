import PySimpleGUI as sg
import os
import sys
import glob
import re
from random import randrange
import lol_a_abp as lol

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def img(path, image):
    """
    Args:
        path (str): name of the path in with the image is located
        image (str): name of the image

    Returns:
        str: absolute path of the file
    """
    return resource_path(os.path.join(f'{path}', f'{image}.png'))

def random_champ():
    return champions_dis[randrange(len(champions_dis))]

pick = 'random'
ban = 'none'

champions_sel = glob.glob(resource_path(img('Champions', '*')))
champions_dis = [
    re.search("[a-z]*\.png", champ, flags=re.I)[0].replace('.png', '')
    for champ in champions_sel
]
sg.theme('Dark')

layout = [
    [sg.Text('What champion do you want do ban? \nDefault is none.'), sg.Text('What champion do you want to pick? \nDefault is random.')],
    [sg.Listbox(champions_dis, size=(30,20), key='bans', enable_events=True), sg.Listbox(champions_dis, size=(30,20), key='picks', enable_events=True)],
    [sg.Input('', size=(30), key='ban', enable_events=True), sg.Input('', size=(30), key='pick', enable_events=True)],
    [sg.Image(img('Champions', ban), key='ban_img', enable_events=True), sg.Image(img('Champions', pick), key='pick_img', enable_events=True), 
        sg.Checkbox('Auto Accept', True, key = 'auto_accept'), sg.Checkbox('Auto Ban', True, key = 'auto_ban'), sg.Checkbox('Auto Pick', True, key = 'auto_pick')],
    [sg.Ok(), sg.Cancel(), sg.Button('Reset', key='Reset'), sg.Radio('Random in game', 1, True, key = 'in_game'), sg.Radio('Random in program', 1, False, key = 'in_app')],
    [sg.Text('Waiting...', key='process', enable_events=True)]
]

window = sg.Window('LoL Auto-ab&p', layout, icon=resource_path(os.path.join('utils', 'icon.ico')))

while True:
    event, values = window.read()
    if event in [sg.WIN_CLOSED, 'Cancel']:
        break
    
    if values['ban'] != '':
        window['bans'].update([x for x in champions_dis if values['ban'] in x.lower()])
        
    if values['pick'] != '':
        window['picks'].update([x for x in champions_dis if values['pick'] in x.lower()])
        
    if event == 'bans':
        ban = str(values['bans']).replace('\'', '').replace('[', '').replace(']', '')
        window['ban_img'].update(img('Champions', ban))
    if event == 'picks':
        pick = str(values['picks']).replace('\'', '').replace('[', '').replace(']', '')
        window['pick_img'].update(img('Champions', pick))
    
    if event == 'Ok':
        if values['in_game'] == True:
            window.perform_long_operation(lambda: lol.automatic(values['auto_accept'], values['auto_ban'], values['auto_pick'], ban, pick), 'process')
        else:
            window.perform_long_operation(lambda: lol.automatic(values['auto_accept'], values['auto_ban'], values['auto_pick'], ban, random_champ()), 'process')
    
    if event == 'Reset':
        window['process'].update('Waiting...')
        window['auto_accept'].update(True)
        window['auto_ban'].update(True)
        window['auto_pick'].update(True)
        window['in_game'].update(True)
        window['ban_img'].update(img('Champions', 'none'))
        window['pick_img'].update(img('Champions', 'random'))
        window['ban'].update('')
        window['pick'].update('')
        window['bans'].update(champions_dis)
        window['picks'].update(champions_dis)
        
        
window.close()