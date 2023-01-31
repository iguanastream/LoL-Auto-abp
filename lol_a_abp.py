import lol_gui
import pyautogui as pag
import time

def locate_click(path):
    """finds the location of a given image path and clicks it

    Args:
        path (str): path to the given image
    """
    pag.leftClick(pag.locateCenterOnScreen(path, confidence=0.6))
    
def accept():
    accept_buton = lol_gui.resource_path(lol_gui.img('utils', 'accept'))
    finding_match = lol_gui.resource_path(lol_gui.img('utils', 'finding'))
    
    lol_gui.window['process'].update('Accepting...')
    
    if pag.locateOnScreen(accept_buton, confidence=0.8) is not None:
        locate_click(accept_buton)
        lol_gui.window['process'].update('Accepted')
        time.sleep(15)
        return (pag.locateOnScreen(finding_match, confidence=0.8,) is None)
    time.sleep(2)
    return False

def ban(to_ban):
    champion_to_ban = lol_gui.resource_path(lol_gui.img('Champions', to_ban))
    info_ban = lol_gui.resource_path(lol_gui.img('utils', 'info_ban'))
    ban_button = lol_gui.resource_path(lol_gui.img('utils', 'ban'))
    search = lol_gui.resource_path(lol_gui.img('utils','search'))


    lol_gui.window['process'].update(f'Banning {to_ban}...')
    
    if pag.locateOnScreen(info_ban, confidence=0.8) is not None:
        locate_click(search)
        time.sleep(1)
        if ban != 'none':   
            pag.write(f'{to_ban}')
        time.sleep(1)
        if pag.locateOnScreen(champion_to_ban, confidence=0.8) is not None:
            locate_click(champion_to_ban)
            time.sleep(1)
            if pag.locateOnScreen(ban_button, confidence=0.8) is not None:
                locate_click(ban_button)
                lol_gui.window['process'].update(f'Banned {to_ban}')
                time.sleep(15)
                return True
    time.sleep(1)
    return False

def pick(to_pick):
    champion_to_pick = lol_gui.resource_path(lol_gui.img('Champions', to_pick))
    info_pick = lol_gui.resource_path(lol_gui.img('utils', 'info_pick'))
    pick_button = lol_gui.resource_path(lol_gui.img('utils', 'pick'))
    search = lol_gui.resource_path(lol_gui.img('utils','search'))

    lol_gui.window['process'].update(f'Picking {to_pick}...')
    
    if pag.locateOnScreen(info_pick, confidence=0.8) is not None:
        locate_click(search)
        time.sleep(1)
        if pag.locateOnScreen(champion_to_pick, confidence=0.8) is not None:
            locate_click(champion_to_pick)
            time.sleep(1)
            if pag.locateOnScreen(pick_button, confidence=0.8) is not None:
                locate_click(pick_button)
                lol_gui.window['process'].update(f'Picked {to_pick}')
                return True
    time.sleep(1)
    return False

def automatic(accepting, baning, picking, to_ban, to_pick):
    if accepting:
        accepted = False
        while not accepted:
            accepted = accept()
            
    if baning:
        baned = False
        while not baned:
            baned = ban(to_ban)
            
    if picking:
        picked = False
        while not picked:
            picked = pick(to_pick)
