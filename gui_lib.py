import PySimpleGUI as sg
import time
from lib_10man import list_of_characters, list_to_tier, tiers_color_dict, tierlist_to_array, checkinlst, get_pos_nums, check_visibility, grabn#, inc
from PIL import Image
from itertools import count
import os
import sys

#naming convention for keys of the buttons
def imgkey(extension):
    return "img"+str(extension)

#fixing edgecase for naming convention. removes instances of zeros for x
def zeroException(x, y):
    if int(x) == 0:
        return y
    else:
        return x + y

#window for editing player tier lists
def edit_tier(name):
    itr_tier_color = list(tiers_color_dict.values())
    tr_lst = tierlist_to_array(name)
    print(tr_lst)
    n = 0
    col = [
        [sg.Button(key=imgkey(str(j)+str(i)),
        button_color = itr_tier_color[j],
        image_filename = checkinlst("charsl/", tr_lst, j, i, ".png"),
        visible = check_visibility(tr_lst, j, i)) for i in range(len(tr_lst[j]))]
        for j in range(len(tr_lst))
    ]

    layout = [
            [sg.Text("edit "+name+"'s tier list", font = ["Ariel", 11])],
            [sg.Column(col, pad = 0)],
            [sg.Button(key="submit")]
    ]
    margins = (1,1)
    window = sg.Window("edit tier list",  layout, margins, element_justification = 'c')

    def swap_img(key1, key2):
        #k1 and k2 are lists: [i, j]
        k1, k2 = get_pos_nums(grabn(key1)), get_pos_nums(grabn(key2))
        k1i, k1j, k2i, k2j = int(k1[0]), int(k1[1]), int(k2[0]), int(k2[1])
        print("k1i:"+str(k1i)+" k1j:"+str(k1j)+" k2i:"+str(k2i)+" k2j:"+str(k2j))
        window[key1].update(image_filename = checkinlst("charsl/", tr_lst, k2i, k2j, ".png"))
        window[key2].update(image_filename = checkinlst("charsl/", tr_lst, k1i, k1j, ".png"))
        print("k1 : "+str(k1)+"\nk2 : "+str(k2))
        tr_lst[k1i][k1j], tr_lst[k2i][k2j] = tr_lst[k2i][k2j], tr_lst[k1i][k1j]

    but_tons = []
    for j in range(len(tr_lst)):
        for i in range(len(tr_lst[j])):
            but_tons.append(imgkey(str(j)+str(i)))
    print(but_tons)
    seen = []
    while True:
        event, values = window.read()
        print(event)
        if event == sg.WIN_CLOSED:
            break
        elif event in but_tons:
            print(event + " seen")
            seen.append(event)
            if len(seen) == 2:
                swap_img(seen[0], seen[1])
                seen = []
        elif event == "submit":
            with open("Players/"+name+".txt", 'w') as f:
                for lst in tr_lst:
                    f.write(list_to_tier(lst))
            break
    window.close()

def open_tierMaker(name):
    col = [
    [sg.Button(key="img"+str(i*10+0), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+0]+".png"),
    sg.Button(key="img"+str(i*10+1), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+1]+".png"),
    sg.Button(key="img"+str(i*10+2), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+2]+".png"),
    sg.Button(key="img"+str(i*10+3), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+3]+".png"),
    sg.Button(key="img"+str(i*10+4), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+4]+".png"),
    sg.Button(key="img"+str(i*10+5), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+5]+".png"),
    sg.Button(key="img"+str(i*10+6), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+6]+".png"),
    sg.Button(key="img"+str(i*10+7), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+7]+".png"),
    sg.Button(key="img"+str(i*10+8), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+8]+".png"),
    sg.Button(key="img"+str(i*10+9), button_color = "gold",
    image_filename = "charsl/"+list_of_characters[i*10+9]+".png")]
    for i in range(0,8)
    ]
    layout = [
        [sg.Text("S tiers:", key = "txt_tier", font = ["Ariel", 11]),
        sg.Text("0", key = "charin_tier", font = ["Ariel", 11])],
        [sg.Text("Aim for 14 characters each tier", font = ["Ariel", 11])],
        [sg.Text("86 characters", key = "txt_num_char", font = ["Ariel", 11])],

        [sg.Column(col, key = "col", pad = 0)],
        [sg.Button(key="img80", button_color = "gold",
        image_filename = "charsl/"+list_of_characters[80]+".png"),
        sg.Button(key="img81", button_color = "gold",
        image_filename = "charsl/"+list_of_characters[81]+".png"),
        sg.Button(key="img82", button_color = "gold",
        image_filename = "charsl/"+list_of_characters[82]+".png"),
        sg.Button(key="img83", button_color = "gold",
        image_filename = "charsl/"+list_of_characters[83]+".png"),
        sg.Button(key="img84", button_color = "gold",
        image_filename = "charsl/"+list_of_characters[84]+".png"),
        sg.Button(key="img85", button_color = "gold",
        image_filename = "charsl/"+list_of_characters[85]+".png")],

        [sg.Button("Submit")],
        [sg.Button("Close")]
    ]

    margins = (1,1)
    window = sg.Window("test window", layout, margins, element_justification = 'c')
    new_file = open("Players/" + name + ".txt", "w")
    saw = []
    lst_saw = []
    but_tons = []
    tiers = ['S','A','B','C','D','F']
    line = 0
    num_chars = 86
    karen_tier = 0
    over15 = 0
    over16 = 0
    for i in range(86):
        but_tons.append("img"+str(i))
    while True:
        event, values = window.read()
        if event == "Close" or event == sg.WIN_CLOSED:
            new_file.close()
            os.remove("Players/"+name+".txt")
            break
        elif event in but_tons:
            if event in saw:
                window[event].update(button_color = "gold")
                num_chars += 1
                karen_tier -= 1
                saw.remove(event)
            else:
                window[event].update(button_color = "grey")
                num_chars -= 1
                karen_tier += 1
                saw.append(event)
        elif ((over15 == 1 and len(saw) > 15) or over15 == 2 or over16 == 1) and event == "Submit" and len(saw) > 14:
            print("too many characters")
        elif event == "Submit" and len(saw) >= 14:
            #write the current tier to new_file
            if len(saw) > 16:
                print("too many characters")
                continue
            elif len(saw) == 15:
                over15 += 1
            elif len(saw) == 16:
                over16 += 1
            print("over15:"+str(over15))
            print("over16:"+str(over16))

            for s in saw:
                window[s].update(disabled = True)
                lst_saw.append(list_of_characters[int(s[3:])])
            string = list_to_tier(lst_saw)
            new_file.write(string)
            if line == 5:
                #find a way to make tier after all the saw and tiers are made
                new_file.close()
                break
            line += 1
            window["txt_tier"].update(tiers[line]+" tiers")
            karen_tier = 0
            saw.clear()
            lst_saw.clear()
        window["txt_num_char"].update(str(num_chars)+" characters:")
        window["charin_tier"].update(str(karen_tier))

    window.close()
