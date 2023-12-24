from colorama import Fore
from pyboy import pyboy, WindowEvent


class PokemonAgent:
    def __init__(self):
        self.num_pokemon = None
        self.num_attacks = None
        self.overworld_actions = None
        self.battle_actions = None
        self.current_actions = None  # Trenutno korišteni set akcija


## FOR THE FUTURE: There may be a need for a seperate set of actions based on the type of scenary

    def set_overworld_actions(self):
        # Postavi set akcija za overworld
        self.overworld_actions = {"MoveUP": [WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP], 
                                  "MoveDOWN": [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN], 
                                  "MoveLEFT": [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT], 
                                  "MoveRIGHT": [WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT],
                                  "PressA": [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A],
                                  "PressB": [WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B]}
        self.current_actions = self.overworld_actions

    def set_battle_actions(self):
        # Postavi set akcija za borbu
        #actions = []
        #actions = {"Attack": [],
        #           "Switch": [],
        #           "PressA": [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A],
        #          "PressB": [WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B]}
        #for attack in range(1, self.num_attacks + 1):
        #    actions["Attack"].append(f'A{attack}')
        #for switch in range(1, self.num_pokemon):
        #    actions["Switch"].append(f'S{switch}')        
        self.battle_actions = {"MoveUP": [WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP], 
                                  "MoveDOWN": [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN], 
                                  "MoveLEFT": [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT], 
                                  "MoveRIGHT": [WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT],
                                  "PressA": [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A],
                                  "PressB": [WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B]}
        self.current_actions = self.battle_actions

    def get_actions(self):
        # Vrati trenutno korišteni set akcija
        return list(self.current_actions)
    
    def set_num_pokemon(self, num_pokemon):
        self.num_pokemon = num_pokemon
    
    def set_num_attacks(self, num_attacks):
        self.num_attacks = num_attacks
        
    def step(self, pb, action):
        pb.send_input(action)

        
    def train(self):
        ...