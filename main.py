from PokemonRedAgent import PokemonAgent

base_q_file = None

ash = PokemonAgent(base_q_values=base_q_file)
ash.train(10)