from pyboy import PyBoy, WindowEvent
from MemoryManip import *
import pickle
import numpy as np
from colorama import Fore
import psutil

class PokemonAgent:
    def __init__(self, 
                 learning_rate=0.5, 
                 discount_factor=0.9, 
                 exploration_rate=1.0, 
                 exploration_decay=0.995, 
                 decay_factor = 0.995, 
                 base_q_values = None, 
                 col = Fore.GREEN,
                 raw = True,
                 max_steps = 0):
        self.current_state = None
        self.num_pokemon = None
        self.num_attacks = None
        self.col = col
        self.raw = raw
        self.max_steps = max_steps
        
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
        self.decay_factor = decay_factor
        self.base_q_values = base_q_values
        self.previous_health = None
        
        if base_q_values is not None and self.raw == False:
            self.load_model(base_q_values)
            self.learning_rate=0.01
        else:
            self.q_values = {}
            self.raw = False
            
    def get_reward(self, pb):
        #seen_poke_count = sum(seen_pokes(pb))
        #pokemon_change = max(,0)
        money_change = max(get_money(pb) - self.old_money, 0)
        items_change = max(total_items(pb) - self.old_items_count, 0)
        party_lvl_change = max(party_lvl(pb) - self.old_party_lvl, 0)
        badges_change = max(get_badges(pb) - self.old_badges, 0)
        died_change = max(get_died(pb) - self.old_died, 0)
        if get_mode(pb) == 0:
            expl_change = max(self.update_map(pb), 0)
        else:
            expl_change = 0
        self.old_party_lvl = party_lvl(pb)
        self.old_items_count = total_items(pb)
        self.old_money = get_money(pb)
        self.old_badges = get_badges(pb)
        self.old_died = get_died(pb)
        self.num_pokemon = num_pokemons(pb)
        
        healing_modifier = 0.005/self.num_pokemon if died_change > 0 else 0
        
        expl_mod = explore_mod(pb)
        
        if party_lvl_change > 1:
            party_modif = 0.0002 * 2/self.num_pokemon
        else:
            party_modif = 0.005 * 10/party_lvl(pb)
        
        party_modif*=expl_mod
        
        state_scores = {
            'level': party_lvl_change * party_modif, # It works!
            #'heal': self.healing(pb) * healing_modifier, # It works!
            #'items': items_change * 0.005, # It works!
            #'dead': died_change * -0.001, # It works!
            'money': money_change * 0.003, # It works!
            'explore': expl_mod * expl_change * 0.05, # It works!
            'badge': badges_change * 0.5 # It works!
            # new place reward
            # no reward for another pokemon 
        }
        
        return state_scores
    
    def healing(self, pb):
        current_health = hp_read(pb)
        #print(f"Current Health: {current_health}")
        #print(f"Previous Health: {self.previous_health}")
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
        if get_mode(pb):
            return get_battle_state(pb)
        else:
            p, x, y = get_x_y(pb)
            #return (p, x, y, self.num_pokemon, get_money(pb), party_lvl(pb), percentage_party_hp(pb), total_items(pb), get_badges(pb))
            #return (p, x, y, party_lvl(pb), get_badges(pb))
            return (p, x, y, get_badges(pb))

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
    
    def save_model(self, file_path, score):
        try:
            with open(file_path, 'rb') as file:
                old = pickle.load(file)
            file.close()
        except FileNotFoundError:
            old = [{}, 0]
            with open(file_path, 'wb') as file:
                pickle.dump(old, file)
            file.close()
            return

        if old[1] < score:
            final = ([self.q_values], score)
            with open(file_path, 'wb') as file:
                pickle.dump(final, file)
            file.close()

    def load_model(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                final = pickle.load(file)
                #print(final[0])
                if len(final) > 1:
                    self.q_values = final[0][0]
                    #print("Tu smo")
                else:
                    self.q_values = {}
            file.close()
        except FileNotFoundError:
            self.q_values = {}
            self.save_model(file_path, 0)
        except Exception as e:
            print(f"Error loading model from {file_path}: {e}")
        #print(f"LOADED: {self.q_values}")
            
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
        for e in range(n_ep):
            with PyBoy('./PokemonRed.gb') as pyb:
                with open("./PokemonRedSaveState.state", "rb") as file_like_object:
                    pyb.load_state(file_like_object)
                rend = False
                
                print(f"Open files before: {psutil.Process().open_files()}")
                file_like_object.close()
                print(f"Open files after: {psutil.Process().open_files()}")


                
                pyb.set_emulation_speed(0)
                #pyb.set_emulation_speed(15)
                
                total_reward = 0
                state = self.get_state(pyb)
                self.old_money = get_money(pyb)
                self.old_party_lvl = party_lvl(pyb)
                self.old_items_count = total_items(pyb)
                self.old_died = get_died(pyb)
                self.old_badges = get_badges(pyb)
                self.old_explored = []
                
                #self.explored = get_location_from_state(pyb)
                pyb._rendering(rend)
                base_tick_speed = 30
                rest = base_tick_speed
                btns = [1,1]   ## NULA GASI EMULATOR!!!! ZAPAMTI! 
                timer = 100
                c = timer
                
                n_moves = 0
                
                while not pyb.tick():
                    
                    # USED ONCE TO SAVESTATE
                    #if(pyb.get_input() == [WindowEvent.PRESS_BUTTON_SELECT]):
                    #    file_like_object = open("./PokemonRedSaveState.state", "wb")
                    #    pyb.save_state(file_like_object)
                    
                    # Saving the values is now an option
                    if(WindowEvent.PRESS_BUTTON_SELECT in pyb.get_input()):
                        if rend:
                            rend = False
                        else:
                            rend = True
                        pyb._rendering(rend)
                        #self.save_model("./PokemonRedQValuesTEST.pickle", total_reward)
                        #pyb.stop()
                    
                    num_pokemon = num_pokemons(pyb)
                    num_attacks = num_moves(pyb)
                    self.set_num_pokemon(num_pokemon)
                    self.set_num_attacks(num_attacks)
                    mode = get_mode(pyb) # overworld = 0, in battle = anything else
                    #print(percentage_party_hp(pyb))
                    #print(f"Input(s): {pyb.get_input()}")
                    
                    if mode > 0:
                        self.set_battle_actions()
                        #print("Moguće akcije u borbi:", self.get_actions())
                    else:
                        self.set_overworld_actions()
                        #print("Moguće akcije u overworldu:", self.get_actions()) 
                    
                    #print(self.q_values)
                    
                    #print(get_x_y(pyb))
                    
                    rest-=1
                    if rest == 0:
                        n_moves += 1
                        action = self.choose_action(state)
                        btns = self.current_actions[action]
                        self.step(pyb, btns[0])
                        next_state = self.get_state(pyb)
                        #print(get_x_y(pyb))
                        #print(f"{self.get_explored()}")
                        reward = self.get_reward(pyb)
                        self.update_q_values(state, action, reward, next_state)
                        print(self. col + f"Episode {e + 1}, Total Reward: {total_reward:0,.4f}, Learning rate: {self.learning_rate}")
                        #print(type(self.q_values))
                        
                        total_reward += sum(r for _, r in reward.items())
                        state = next_state
                        
                        rest = base_tick_speed
                        
                        #c-=1
                                                
                        if c==0:
                            c = timer
                            self.learning_rate *= self.decay_factor
                        
                    elif rest == base_tick_speed/2.5:
                        self.step(pyb, btns[1])
                        ...
                    if goal(pyb) or (self.max_steps > 0 and n_moves>self.max_steps):
                        score = total_reward/np.log(n_moves)
                        self.save_model(self.base_q_values, score = score)
                        pyb.stop()
                self.learning_rate *= self.decay_factor
                #print(self.learning_rate)
        #self.save_model(generation)