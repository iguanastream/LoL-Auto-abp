import PySimpleGUI as sg
import os
import glob


def img(image):
    return os.path.join('Champions', f'{image}.png')


pick = 'random'
ban = 'none'
champions_sel = glob.glob(os.path.join('Champions', '*.png'))
champions_dis = []
for champ in champions_sel:
    champions_dis.append(champ.replace('Champions\\', '').replace('.png', ''))

sg.theme('Dark')

layout = [
    [sg.Text('What champion do you want do ban? \nDefault is none.'), sg.Text('What champion do you want to pick? \nDefault is random.')],
    [sg.Listbox(champions_dis, size=(30,20), key='bans', enable_events=True), sg.Listbox(champions_dis, size=(30,20), key='picks', enable_events=True)],
    [sg.Input('', size=(30), key='ban', enable_events=True), sg.Input('', size=(30), key='pick', enable_events=True)],
    [sg.Image(img(ban), key='ban_img', enable_events=True), sg.Image(img(pick), key='pick_img', enable_events=True)],
    [sg.Ok(), sg.Cancel()]
]

window = sg.Window('Lol Auto-pan', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
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
        pass

window.close()

