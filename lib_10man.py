import random
import os

#list of ssbu characters
list_of_characters = ['Mario', 'Donkey Kong', 'Link', 'Samus', 'Dark Samus', 'Yoshi', 'Kirby', 'Fox', 'Pikachu', 'Luigi', 'Ness', 'Captain Falcon', 'Jigglypuff', 'Peach', 'Daisy', 'Bowser', 'Ice Climbers', 'Sheik', 'Zelda', 'Dr. Mario', 'Pichu', 'Falco', 'Marth', 'Lucina', 'Young Link', 'Ganondorf', 'Mewtwo', 'Roy', 'Chrom', 'Mr. Game & Watch', 'Meta Knight', 'Pit', 'Dark Pit', 'Zero Suit Samus', 'Wario', 'Snake', 'Ike', 'Pokemon Trainer', 'Diddy Kong', 'Lucas', 'Sonic', 'King Dedede', 'Olimar', 'Lucario', 'R.O.B.', 'Toon Link', 'Wolf', 'Villager', 'Mega Man', 'Wii Fit Trainer', 'Rosalina & Luma', 'Little Mac', 'Greninja', 'Mii Brawler', 'Mii Swordfighter', 'Mii Gunner', 'Palutena', 'Pac-man', 'Robin', 'Shulk', 'Bowser Jr.', 'Duck Hunt', 'Ryu', 'Ken', 'Cloud', 'Corrin', 'Bayonetta', 'Inkling', 'Ridley', 'Simon', 'Richter', 'King K. Rool', 'Isabelle', 'Incineroar', 'Piranha Plant', 'Joker', 'Hero', 'Banjo & Kazooie', 'Terry', 'Byleth', 'Min Min', 'Steve', 'Sephiroth', 'Pyra-Mythra', 'Kazuya', 'Sora']

#dlc characters
dlc_characters = ['Piranha Plant', 'Joker', 'Hero', 'Banjo & Kazooie', 'Terry', 'Byleth', 'Min Min', 'Steve', 'Sephiroth', 'Pyra-Mythra', 'Kazuya', 'Sora']

#dictionary of tiers : colors
tiers_color_dict = {'S':"red", 'A':"orange", 'B':"green", 'C':"blue", 'D':"purple", 'F':"pink"}

#returns list of characters for a player
def char_lineup(num_characters, dlc_toggle):
    lineup = []
    random.seed()
    loc = list_of_characters.copy()
    if dlc_toggle:
        loc = [elem for elem in loc if elem not in dlc_characters]
    for i in range(num_characters):
        chosen_character = random.randrange(0, len(loc))
        name = loc[chosen_character]
        loc.remove(name)
        lineup.append(name)
    return lineup

def gen_personal(filename):
    tierDict = {}
    tiers = ['S', 'A', 'B', 'C', 'D', 'F']
    counter = 0

    f = open("Players/" + filename, "r")
    for x in f:
        tierDict[tiers[counter]] = x.strip().split('_')
        counter = counter + 1
    return tierDict 

def gen_global(directory):
    dictOut = {}
    for f in os.listdir(directory):
        dictOut[f.split('.')[0]] = gen_personal(f)
    return dictOut

def get_tier(player, character, dic):
    for x in dic[player]:
        for y in dic[player][x]:
            if character == y:
                return x
    print("\nPlayer: " + player + " Character: " + character)
    return None

def get_rand_char_from_tier(player, tier, dic):
    return dic[player][tier][random.randrange(0, len(dic[player][tier]), 1)]

def gen_matched_list(player1, player2, dic, p1List, dlc_toggle):
    p2List = []
    for x in p1List:
        char = get_rand_char_from_tier(player2, get_tier(player1, x, dic), dic)
        while char in p2List:
            char = get_rand_char_from_tier(player2, get_tier(player1, x, dic), dic)
        if dlc_toggle:
            while char in dlc_characters:
                char = get_rand_char_from_tier(player2, get_tier(player1, x, dic), dic)
        p2List.append(char)
    return p2List

def print_dict(dictionary):
    print(dictionary)

def list_to_tier(lst):
    string = ""
    for s in lst:
        string += s + "_"
    string = string[0:-1]
    string += "\n"
    return string

#creates 2d array of given tier list
def tierlist_to_array(name):
    lst = []
    with open("Players/"+name+".txt", 'r') as f:
        while True:
            read = f.readline()
            if not read:
                break
            tier = read.split("_")
            tier[-1] = tier[-1][0:-1]
            lst.append(tier)
    return lst

#checks if array coordinate exists
#prerequisite: lst needs to be a list of list of strings
def checkinlst(str1, lst, x, y, str2):
    if x < len(lst) and y < len(lst[x]):
        return str1 + lst[x][y] + str2
    else:
        print("RETURNED NONE")
        return None

#ex: num = 86 -> pos_nums = [6, 8]
def get_pos_nums(num):
    pos_nums = []
    print(num)
    string = str(num)
    pos_nums.append(string[0])
    pos_nums.append(string[1:])
    print(pos_nums)
    return pos_nums

#if coordinate not in range of array, button visibility is false, else true
def check_visibility(lst, x, y):
    if x < len(lst) and y < len(lst[x]):
        return True
    else:
        return False

#grab number from naming convention "img##"
def grabn(string):
    i = len(string) - 1
    while string[i:].isdigit():
        i -= 1
    print(string[i+1:])
    return string[i+1:]

