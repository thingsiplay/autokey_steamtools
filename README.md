# autokey_steamtools
Scripts for Autokey

steamtools script: https://github.com/thingsiplay/autokey_steamtools
Autokey is required: https://github.com/autokey/autokey/
    
Copy the script into scripts folder of Autokey.  On my Ubuntu machine its: 
    
        /home/tuncay/.config/autokey/data/

## Script: proton.py

Only works in Steam client while games shop page is open. If script is activated, it clicks with right mouse button to open menu and copies url to clipboard. Then script extracts id and either open ProtonDB page for game or displays ProtonDB information by looking up data from server.

The default hotkey is 'F6', but can be changed in Autokey itself. If you do not want to show up the dialog or open the link in browser, then edit the scripts variables.

Set ACTION_DIALOG=False to disable show dialog or ACTION_WEBBROWSER=False to disable open browser.
