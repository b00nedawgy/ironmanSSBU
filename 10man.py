import PySimpleGUI as sg
import time
from lib_10man import char_lineup, gen_global, gen_matched_list, get_tier, tiers_color_dict
from PIL import Image
import os
import sys
from gui_lib import open_tierMaker, edit_tier

#theme
sg.theme('DarkAmber')

character_num = 0   #number of characters
matched_random = True
dlc_toggle = False

dic = gen_global("Players")
lst_names = list(dic.keys())

layout = [
    [sg.Text("Number of characters", size=(30, 1)), sg.InputText(default_text = "10")],
    [sg.Checkbox("Matched random", default=True)],
    [sg.Text("Player 1: ", size=(30, 1)), sg.Combo(lst_names,default_value = "Thomas",k="l1")],
    [sg.Text("Player 2: ", size=(30, 1)), sg.Combo(lst_names,default_value="Brendan",k="l2")],
    [sg.Column([[sg.Button("New Player", size = (15,1))]],
    element_justification = 'l', pad = 1),
    sg.Column([[sg.InputText()]], element_justification = 'r', pad = 1)],
    [sg.Column([[sg.Button("edit Player", size = (15,1))]],
    element_justification = 'l', pad = 1),
    sg.Column([[sg.Combo(lst_names, k="edit_l")]], element_justification = 'r', pad = 1)],
    [sg.Column([[sg.Button("Remove Player: ", size=(15,1))]],
    element_justification = 'l', pad = 1),
    sg.Column([[sg.Combo(lst_names, k="l3")]], element_justification = 'r', pad = 1)],
    [sg.Checkbox("toggle DLC", default=False, k="togDLC")],
    [sg.Button("Start")],
    [sg.Button("Close")]
]

margins = (10, 10)
player_one = "Brendan"        #defualt tier list
player_two = "Thomas"         #default tier list
tier_color = "grey"

window = sg.Window("10 Man Iron Man", layout, margins)

#gather information
while True:
    print(lst_names)
    event, values = window.read()
    print(values)
    if event == "Close" or event == sg.WIN_CLOSED:
        sys.exit("program exited")
    elif event == "Start":
        character_num = int(values[0])
        if values[1]:
            matched_random = True
            player_one = values["l1"]
            player_two = values["l2"]
        else:
            matched_random = False
        if character_num <= 0 or character_num > 10:    #player_num less than or equal to 0
            sys.exit("inputed values are invalid")
        if values["togDLC"] == True:
            dlc_toggle = True
        break
    elif event == "New Player":
        open_tierMaker(values[2])
        sys.exit("New Player Tier list made")
    elif event == "edit Player":
        edit_tier(values["edit_l"])
        sys.exit("Tier list edited")
    elif event == "Remove Player: ":
        os.remove("Players/"+values["l3"]+".txt")
        lst_names.remove(values["l3"])
        sys.exit("Player "+values["l3"]+" removed")
    window["l1"].update(values=lst_names)
    window["l2"].update(lst_names)
    window["l3"].update(lst_names)
window.close()

tier_layout = []

charList = []
seen = {}
saw = []

#inital characters, colors, and visibility of frames
name = []
color_list = []
charList = char_lineup(character_num, dlc_toggle)
visibility_config = []
for i in range(character_num):
    tier_color = tiers_color_dict[get_tier(player_one, charList[i], dic)]
    color_list.append(tier_color)
    seen["-IMG1-"+str(i)] = tier_color
    visibility_config.append(True)
name += charList

for i in range(len(color_list), 10):
    color_list.append("black")
    name.append("no_one")
    visibility_config.append(False)
color_list.append("!")
name.append("!")
visibility_config.append("!")

if matched_random:
    charList = gen_matched_list(player_one, player_two, dic, charList, dlc_toggle)
else:
    charList = char_lineup(character_num, dlc_toggle)

for i in range(character_num):
    tier_color = tiers_color_dict[get_tier(player_two, charList[i], dic)]
    color_list.append(tier_color)
    seen["-IMG2-"+str(i)] = tier_color
    visibility_config.append(True)
name += charList

for i in range(len(color_list), 21):
    color_list.append("black")
    name.append("no_one")
    visibility_config.append(False)

#refresh characters
def refresh_characters():
    #player1
    charList = char_lineup(character_num, dlc_toggle)
    for i in range(len(charList)):
        tier_color = tiers_color_dict[get_tier(player_one, charList[i], dic)]
        imOut = "chars/" + charList[i] + ".png"
        window2["-IMG1-" + str(i)].update(image_filename = imOut)
        window2["-IMG1-" + str(i)].update(button_color = tier_color)
        window2["-IMG1-" + str(i)].ParentRowFrame.config(background = "grey")
        window2["f-IMG1-" + str(i)].update(visible = True)
        window2["f-IMG1-"+str(i)].Widget.config(background = "gold")
        seen["-IMG1-"+str(i)] = tier_color
    #player2
    if matched_random:
        charList = gen_matched_list(player_one, player_two, dic, charList, dlc_toggle)
    else:
        charList = char_lineup(character_num, dlc_toggle)

    for i in range(len(charList)):
        tier_color = tiers_color_dict[get_tier(player_two, charList[i], dic)]
        imOut = "chars/" + charList[i] + ".png"
        window2["-IMG2-" + str(i)].update(image_filename = imOut),
        window2["-IMG2-" + str(i)].update(button_color = tier_color)
        window2["-IMG2-" + str(i)].ParentRowFrame.config(background = "grey")
        window2["f-IMG2-" + str(i)].update(visible = True)
        window2["f-IMG2-"+str(i)].Widget.config(background = "gold")
        seen["-IMG2-"+str(i)] = tier_color

#setup layout for window 2
col1_s = [
    [sg.Frame('', [[sg.Button(key="-IMG1-"+str(i),
    image_filename = "chars/"+name[i]+".png",
    button_color = color_list[i])]],
    background_color = "gold", visible = visibility_config[i],
    key="f-IMG1-"+str(i)),

    sg.Frame('', [[sg.Button(key="-IMG1-"+str(i+1),
    image_filename = "chars/"+name[i+1]+".png",
    button_color = color_list[i + 1])]],
    background_color = "gold", visible = visibility_config[i+1],
    key="f-IMG1-"+str(i+1))] for i in range(0,10,2)
]

col2_s = [
    [sg.Frame('', [[sg.Button(key="-IMG2-"+str(i),
    image_filename = "chars/"+name[name.index("!")+1+i]+".png",
    button_color = color_list[color_list.index("!")+1+i])]],
    background_color = "gold", visible = visibility_config[visibility_config.index("!")+1+i],
    key="f-IMG2-"+str(i)),

    sg.Frame('', [[sg.Button(key="-IMG2-"+str(i+1),
    image_filename = "chars/"+name[name.index("!")+1+i+1]+".png",
    button_color = color_list[color_list.index("!")+1+i+1])]],
    background_color = "gold", visible = visibility_config[visibility_config.index("!")+1+i+1],
    key="f-IMG2-"+str(i+1))] for i in range(0,10,2)
]

col1=[
    [sg.Text('Player 1', background_color='black', font = ["Ariel", 30])],
    [sg.Column(col1_s, element_justification='c')]
]

col2=[
    [sg.Text('Player 2', background_color="black", font = ["Ariel", 30])],
    [sg.Column(col2_s, element_justification='c')]
]

layout2 = [
    [sg.Column(col1, element_justification='l'),
    sg.VSeparator(p=(30,0)),
    sg.Column(col2, element_justification='r')],
    [sg.Button("Close"), sg.Button("Retry")]
]

#window of characters
window2 = sg.Window("The Ironman", layout2, margins, location = (400,0), element_justification = 'c', element_padding = 1)

#list of usable buttons
but_ton = []
for i in range(1,3,1):
    for j in range(10):
        but_ton.append("-IMG"+str(i)+"-"+str(j))

#window2 event loop
while True:
    event, values = window2.read()
    print(event)
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    elif event == "Retry":
        saw.clear()
        refresh_characters()
        window2.refresh()
    elif event in but_ton:
        print("event found in but_ton")
        if event in saw:
            tier_color = seen[event]
            window2[event].update(button_color = tier_color)
            window2["f"+event].Widget.config(background = "gold")
            saw.remove(event)
            print(saw)
        else:
            window2[event].update(button_color = "grey")
            window2["f"+event].Widget.config(background = "grey")
            window2[event].ParentRowFrame.config(background = "grey")
            saw.append(event)
            print(saw)
window2.close()
