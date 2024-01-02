from PokemonRedAgent import PokemonAgent
from MemoryManip import *

from colorama import Fore
import sys

if(len(sys.argv)<4):
    print("Skripta traži 3 parametra; naziv datoteke, broj boje i bool za raw")
else:
    args = sys.argv[1:]

    title = str(args[0])
    col = int(args[1])
    r = False if args[2] == "False" else True
    print(r)
    #file = None
    file = title

    colors = [Fore.CYAN, Fore.RED, Fore.MAGENTA, Fore.GREEN, Fore.YELLOW, Fore.WHITE]

    ash = PokemonAgent(discount_factor= 0.95, base_q_values = file, col=colors[col], raw = r)
    print(ash.learning_rate)
    ash.train(1)