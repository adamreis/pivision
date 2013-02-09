import os

def update_gui(text):
    os.system(' sed -i "$ d" gui.html')
    os.system('echo ' + text + '>> gui.html')
