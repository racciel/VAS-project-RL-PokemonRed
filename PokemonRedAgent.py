import random
from pyboy import PyBoy, WindowEvent
from MemoryManip import *
import pickle
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

class PokemonAgent:
    def __init__(self, base_q_values = None):
        self.current_state = None
        self.num_pokemon = None
        self.num_attacks = None
        self.died = 0
        self.general_actions = {"MoveUP": [WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP], 
                                "MoveDOWN": [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN], 
                                "MoveLEFT": [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT], 
                                "MoveRIGHT": [WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT],
                                "SelectAction": [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A],
                                "CancelAction": [WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B]}
                
        self.overworld_actions = self.general_actions
        self.battle_actions = self.general_actions
        
        self.current_actions = None  # Trenutno korišteni set akcija

        self.explore_weight = 1
        
        if base_q_values is not None:
            self.q_values = base_q_values.get_q_values().copy()
        else:
            self.q_values = {("Overworld", action): 0.0 for action in self.general_actions}
            
    def get_game_state_reward(self, pb):
        seen_poke_count = sum(seen_pokes(pb))
        money_change = max(get_money(pb) - self.old_money, 0)
        items_change = max(total_items(pb) - self.old_items_count, 0)
        self.old_items_count = total_items(pb)
        self.old_money = get_money(pb)
        state_scores = { 
            'level': self.party_lvl(pb), 
            'heal': self.total_healing_rew,
            'items': items_change * 1.5,
            'dead': -0.1*self.died,
            'money': money_change * 3,
            'seen_poke':  seen_poke_count * 40,
            'explore': self.get_knn_reward()
        }
        
        return state_scores
    
    def get_knn_reward(self):
        pre_rew = self.explore_weight * 0.005
        post_rew = self.explore_weight * 0.01
        cur_size = self.knn_index.get_current_count() if self.use_screen_explore else len(self.seen_coords)
        base = (self.base_explore if self.levels_satisfied else cur_size) * pre_rew
        post = (cur_size if self.levels_satisfied else 0) * post_rew
        return base + post
    
    def save_model(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.q_values, file)

    def load_model(self, file_path):
        with open(file_path, 'rb') as file:
            self.q_values = pickle.load(file)
            
    def set_overworld_actions(self):
        self.current_actions = self.overworld_actions

    def set_battle_actions(self):
        self.current_actions = self.battle_actions

    def get_actions(self):
        return list(self.current_actions)
    
    def set_num_pokemon(self, num_pokemon):
        self.num_pokemon = num_pokemon
    
    def set_num_attacks(self, num_attacks):
        self.num_attacks = num_attacks
        
    def step(self, pb, action):
        pb.send_input(action)
     
    def train(self, n_ep):
        generation = []
        for _ in range(n_ep):
            with PyBoy('./PokemonRed.gb') as pyb:
                self.old_money = get_money(pyb)
                base_tick_speed = 20
                rest = base_tick_speed
                btns = [1,1]   ## NULA GASI EMULATOR!!!! ZAPAMTI! 
                while not pyb.tick():
                    num_pokemon = pyb.get_memory_value(0xD163)
                    num_attacks = num_moves(pyb)
                    self.set_num_pokemon(num_pokemon)
                    self.set_num_attacks(num_attacks)
                    mode = pyb.get_memory_value(0xD057) # overworld = 0, in battle = anything else
                    print(f"Suma levela pokemona u party-ju: {party_lvl(pyb)}")
                    
                    print(f"Broj pokemona: {self.num_pokemon}")
                    print(f"Broj napada: {self.num_attacks}")
                    print(f"Input(s): {pyb.get_input()}")
                    
                    if mode > 0:
                        self.set_battle_actions()
                        print("Moguće akcije u borbi:", self.get_actions())
                    else:
                        self.set_overworld_actions()
                        print("Moguće akcije u overworldu:", self.get_actions()) 
                        
                    print("Odabrani meni:", menu_option(pyb))
                    print("Moc odabranog napada:", selected_move_power(pyb))

                    rest-=1
                    if rest == 0:
                        max_q_value = max(self.q_values.values())
                        best_actions = [action for action, q_value in self.q_values.items() if q_value == max_q_value]
                        chosen_action = random.choice(best_actions)  # Nasumično odaberi između jednako dobrih akcija
                        btns = self.current_actions[chosen_action[1]]
                        
                        self.step(pyb, btns[0])
                        rest = base_tick_speed
                    elif rest == base_tick_speed/2:
                        self.step(pyb, btns[1])
                    if goal(pyb):
                        # Tu ću zapisati najbolju q tablicu za ovu generaciju pa ću je koristiti poslije kao početnu
                        pyb.stop()
        self.save_model(generation)