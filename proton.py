""" Open ProtonDB page or show info in Steam client at games shop page.

    https://github.com/thingsiplay/autokey_steamtools

    Python 3.6
    Autokey: 0.95
    
    Autokey is required: https://github.com/autokey/autokey/
    
    Only works in Steam client while games shop page is open. If script 
    is activated, it clicks with right mouse button to open menu and 
    copies url to clipboard. Then script extracts id and either open 
    ProtonDB page for game or displays ProtonDB information by looking
    up data from server.
    
    I recommend to set up a hotkey for quick access, in example 'F6'. 
    The ACTION_ variables defines if these actions will be executed.
    
    Copy the script into scripts folder of Autokey.  On my Ubuntu 
    machine its: 
    
        /home/tuncay/.config/autokey/data/
"""

import re
import time
import webbrowser
import urllib.request
import json


""" SETTINGS """

# Display message with summary from ProtonDB
# True: on, False: off
# True or False
ACTION_DIALOG = True

# Open ProtonDB link in a web browser.
# True: on, False: off
# True or False
ACTION_WEBBROWSER = True

# Wait seconds added between critical operations.
# Default: 0.1
# float
WAIT_DEFAULT = 0.1

""" END OF SETTINGS """


# Default sleep time in seconds between critical operations.
def wait(sleep=0.0):
    global WAIT_DEFAULT
    if not isinstance(sleep, float) or not isinstance(WAIT_DEFAULT, float):
        raise ValueError('Wait arguments must be float type.')
    time.sleep(sleep + WAIT_DEFAULT)


# Backup original clipboard data
clip_backup = clipboard.get_clipboard()
wait(0.1)
# Retrieve game url from menu "Copy Page URL"
mouse.click_relative_self(0, 0, 3)  # 3=right
wait()
keyboard.send_key('<down>')
wait()
keyboard.send_key('<down>')
wait()
keyboard.send_key('<down>')
wait()
keyboard.send_key('<down>')
wait()
keyboard.send_key('<enter>')
wait()
clip = None
clip = clipboard.get_clipboard()
wait(0.1)
# Proceed only if success.
if clip and clip.startswith('https://store.steampowered.com/app'):
    url_steam = str(clip)        
    match = re.search('(?<=/app/)(\d+)', url_steam)
    # Proceed only, if its a shop page for game.
    if match:
        # Create links
        id = match.group(1)
        url_proton = f'https://www.protondb.com/app/{id}'
        url_proton_json = f'https://www.protondb.com/api/v1/reports/summaries/{id}.json'
        # Extract title
        match = re.search('(?<=/app/)\d+/(.+)/$', url_steam)
        if match:
            game_title = match.group(1).replace('_', u'\u00A0')  # NB space
        # Extract summary and show results in a dialog
        if ACTION_DIALOG:
            clipboard.fill_clipboard(url_proton)
            wait(0.1)
            summary = ''
            try:
                with urllib.request.urlopen(url_proton_json) as f:
                    sum = json.load(f)
            except urllib.error.HTTPError:
                pass
            else:
                summary += game_title
                summary += '\n' + 64 * u'\u00A0'
                summary += '\n'
                summary += 'Rating / Tier:'
                summary += '\n'
                summary += str(sum['tier'])
                summary += '\n\n'
                summary += 'Confidence:'
                summary += '\n'
                summary += str(sum['confidence'])
                summary += '\n\n'
                summary += 'Score:'
                summary += '\n'
                summary += str(sum['score'])
                summary += '\n\n'
                summary += 'Reports:'
                summary += '\n'
                summary += str(sum['total'])
                summary += '\n\n'
            if summary:
                dialog.info_dialog(title='ProtonDB', message=summary)
            else:
                dialog.info_dialog(title='ProtonDB', message='No report.')
        # Open ProtonDB page in browser
        if ACTION_WEBBROWSER:
            # new: 1=new window, 2=new tab
            webbrowser.open(url_proton, new=2, autoraise=True)
# Restore original clipboard data
clipboard.fill_clipboard(clip_backup)
wait(0.1)
