class PokemonAgent:
    def __init__(self):
        self.num_pokemon = None
        self.num_attacks = None
        self.overworld_actions = None
        self.battle_actions = None
        self.current_actions = None  # Trenutno korišteni set akcija

    def set_overworld_actions(self):
        # Postavi set akcija za overworld
        self.overworld_actions = ["MoveForward", "MoveBackward", "MoveLeft", "MoveRight"]
        self.current_actions = self.overworld_actions

    def set_battle_actions(self):
        # Postavi set akcija za borbu
        actions = []
        for attack in range(1, self.num_attacks + 1):
            actions.append(f'A{attack}')
        for switch in range(1, self.num_pokemon):
            actions.append(f'S{switch}')
        self.battle_actions = actions
        self.current_actions = self.battle_actions

    def get_actions(self):
        # Vrati trenutno korišteni set akcija
        return self.current_actions
    
    def set_num_pokemon(self, num_pokemon):
        self.num_pokemon = num_pokemon
    
    def set_num_attacks(self, num_attacks):
        self.num_attacks = num_attacks