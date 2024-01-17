from PokemonRedAgent import PokemonAgent
from MemoryManip import *

from colorama import Fore
import sys

if(len(sys.argv)<5):
    print("Skripta traži 4 parametra; naziv datoteke, broj boje i bool za raw")
else:
    args = sys.argv[1:]

    title = str(args[0])
    col = int(args[1])
    r = False if args[2] == "False" else True
    #file = None
    file = title

    ms = int(args[3])

    i = 10

    ms_l = []

    for i in range(ms):
        ms_l.append(10**i)

    ms_l = ms_l[::-1]
    ms_l = ms_l[0:3]
    ms_l = ms_l[::-1]

    colors = [Fore.CYAN, Fore.RED, Fore.MAGENTA, Fore.GREEN, Fore.YELLOW, Fore.WHITE]

    for m in ms_l:
        ash = PokemonAgent(discount_factor= 0.95, base_q_values = file, col=colors[col], raw = r, max_steps=m)
        print(ash.learning_rate)
        ash.train(100)