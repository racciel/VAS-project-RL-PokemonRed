import random
from pyboy import PyBoy, WindowEvent
from MemoryManip import *
import pickle
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import io

class PokemonAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995, base_q_values = None):
        self.current_state = None
        self.num_pokemon = None
        self.num_attacks = None
        
        self.general_actions = {"MoveUP": [WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP], 
                                "MoveDOWN": [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN], 
                                "MoveLEFT": [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT], 
                                "MoveRIGHT": [WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT],
                                "SelectAction": [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A],
                                "CancelAction": [WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B]}
        
        self.overworld_actions = self.general_actions
        self.battle_actions = self.general_actions
        
        self.current_actions = None  # Trenutno korišteni set akcija
        
        self.learning_rate = learning_rate  # stopa učenja
        self.discount_factor = discount_factor  # faktor diskontiranja
        self.exploration_rate = exploration_rate  # stopa istraživanja
        self.exploration_decay = exploration_decay  # faktor smanjenja istraživanja
        
        self.previous_health = None
        
        if base_q_values is not None:
            self.q_values = base_q_values.copy()
        else:
            self.q_values = {}
            
    def get_reward(self, pb):
        #seen_poke_count = sum(seen_pokes(pb))
        money_change = max(get_money(pb) - self.old_money, 0)
        items_change = max(total_items(pb) - self.old_items_count, 0)
        party_lvl_change = max(party_lvl(pb) - self.old_party_lvl, 0)
        badges_change = max(get_badges(pb) - self.old_badges, 0)
        died_change = max(get_died(pb) - self.old_died, 0)
        expl_change = max(self.update_map(pb), 0) ## TODO
        self.old_party_lvl = party_lvl(pb)
        self.old_items_count = total_items(pb)
        self.old_money = get_money(pb)
        self.old_badges = get_badges(pb)
        self.old_died = get_died(pb)
        
        state_scores = {
            'level': party_lvl_change * 0.3, # It works!
            'heal': self.healing(pb)* 0.15, # testing
            'items': items_change * 0.15, # It works!
            'dead': -0.01*died_change, # WIP
            'money': money_change * 0.03, # It works!
            'explore': expl_change*0.02, # It works!
            'badge': badges_change * 0.5 # It works!
        }
        
        return state_scores
    
    def healing(self, pb):
        current_health = hp_read(pb)
        print(f"Current Health: {current_health}")
        print(f"Previous Health: {self.previous_health}")
        if self.previous_health is not None:
            relevant_health = [current for i, current in enumerate(current_health) if i in range(self.num_pokemon)]
            relevant_previous_health = [previous for i, previous in enumerate(self.previous_health) if i in range(self.num_pokemon)]
            

            healing_occurred = any(current > previous for current, previous in zip(relevant_health, relevant_previous_health))
            if healing_occurred:
                self.previous_health = current_health
                return healing_occurred
            
        self.previous_health = current_health
        return 0.0
    
    def get_explored(self):
        return self.q_values
    
    def get_state(self, pb):
        p, x, y = get_x_y(pb)
        return (p, x, y, self.num_pokemon, get_money(pb), party_lvl(pb), total_items(pb), get_badges(pb))

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.get_actions())
        else:
            best_action = max(self.get_actions(), key=lambda action: self.q_values.get((state, action), 0))
        return best_action
    
    def update_map(self, pb):
        current = get_x_y(pb)
        if current in self.old_explored:
            return 0
        else:
            self.old_explored.append(current)
            return 1
    
    def update_q_values(self, state, action, reward, next_state):
        if state not in self.q_values:
            self.q_values[state] = {}

        current_q = self.q_values[state].get(action, 0)
        max_future_q = max(self.q_values.get(next_state, {}).get(a, 0) for a in self.get_actions())

        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (
                float(sum(reward[k] for k, _ in reward.items())) + self.discount_factor * max_future_q)
        self.q_values[state][action] = new_q
    
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
        for e in range(n_ep):
            with PyBoy('./PokemonRed.gb') as pyb:
                
                file_like_object = open("./PokemonRedSaveState.state", "rb")
                #print(file_like_object)
                pyb.load_state(file_like_object)
                
                total_reward = 0
                state = self.get_state(pyb)
                self.old_money = get_money(pyb)
                self.old_party_lvl = party_lvl(pyb)
                self.old_items_count = total_items(pyb)
                self.old_died = get_died(pyb)
                self.old_badges = get_badges(pyb)
                self.old_explored = []
                
                #self.explored = get_location_from_state(pyb)
                
                base_tick_speed = 20
                rest = base_tick_speed
                btns = [1,1]   ## NULA GASI EMULATOR!!!! ZAPAMTI! 
                
                while not pyb.tick():
                    
                    # USED ONCE TO SAVESTATE
                    #if(pyb.get_input() == [WindowEvent.PRESS_BUTTON_SELECT]):
                    #    file_like_object = open("./PokemonRedSaveState.state", "wb")
                    #    pyb.save_state(file_like_object)
                    
                    num_pokemon = pyb.get_memory_value(0xD163)
                    num_attacks = num_moves(pyb)
                    self.set_num_pokemon(num_pokemon)
                    self.set_num_attacks(num_attacks)
                    mode = pyb.get_memory_value(0xD057) # overworld = 0, in battle = anything else
                    #print(f"Suma levela pokemona u party-ju: {party_lvl(pyb)}")
                    
                    #print(f"Broj pokemona: {self.num_pokemon}")
                    #print(f"Broj napada: {self.num_attacks}")
                    print(f"Input(s): {pyb.get_input()}")
                    
                    if mode > 0:
                        self.set_battle_actions()
                        #print("Moguće akcije u borbi:", self.get_actions())
                    else:
                        self.set_overworld_actions()
                        #print("Moguće akcije u overworldu:", self.get_actions()) 
                        
                    print(f"Episode {e + 1}, Total Reward: {total_reward}")
                    #print(f"Sta god da je ovo: {get_x_y(pyb)}")
                    #print(self.q_values)
                    
                    
                    rest-=1
                    if rest == 0:
                        action = self.choose_action(state)
                        btns = self.current_actions[action]
                        #self.step(pyb, btns[0])
                        
                        next_state = self.get_state(pyb)
                        
                        #print(f"{self.get_explored()}")
                        reward = self.get_reward(pyb)
                        self.update_q_values(state, action, reward, next_state)
                        
                        total_reward += sum(r for _, r in reward.items())
                        state = next_state
                        
                        rest = base_tick_speed
                    elif rest == base_tick_speed/2:
                        #self.step(pyb, btns[1])
                        ...
                    if goal(pyb):
                        # Tu ću zapisati najbolju q tablicu za ovu generaciju pa ću je koristiti poslije kao početnu
                        pyb.stop()
        self.save_model(generation)