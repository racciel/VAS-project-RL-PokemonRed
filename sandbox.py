from sandbox2 import PokemonAgent
from MemoryManip import *

from colorama import Fore
import sys

args = sys.argv[1:]

title = str(args[0])
col = int(args[1])

#file = None
file = title

colors = [Fore.BLUE, Fore.RED, Fore.MAGENTA, Fore.GREEN, Fore.YELLOW, Fore.WHITE]

ash = PokemonAgent(base_q_values = file, col=colors[col], raw = True)
ash.train(10)