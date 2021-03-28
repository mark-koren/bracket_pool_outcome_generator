import numpy as np
import pdb
import itertools
from tqdm import tqdm

team_ratings_538 = {0: 96.71,
					1: 88.85,
					2: 89.82,
					3: 87.39,
					4: 89.52,
					5: 88.93,
					6: 86.95,
					7: 90.57,
					8: 94.78,
					9: 87.75,
					10: 88.38,
					11: 76.43,
					12: 88.6,
					13: 86.15,
					14: 86.02,
					15: 91.94,}

def win_likelihood_538(winner_rating, loser_rating):
	return 1 / (1 + 10 ** (-(winner_rating - loser_rating) * 30.464 / 400))

def generate_round_pointer_array(num_teams):
	total_games = num_teams - 1
	round_pointer_array = np.zeros(total_games)
	n = num_teams // 2
	end_idx = num_teams // 2

	for i in range(2,int(np.log2(num_teams))):
		start_idx = end_idx
		end_idx = start_idx + n//2
		round_pointer_array[start_idx:end_idx+1] = start_idx
		n = n//2

	return round_pointer_array.astype(int)

def generate_game_pointer_array(num_teams):
	total_games = num_teams - 1
	round_pointer_array = np.zeros(total_games)
	n = num_teams // 2
	end_idx = num_teams // 2
	for i in range(1,int(np.log2(num_teams))):
		start_idx = end_idx
		end_idx = start_idx + n//2
		round_pointer_array[start_idx:end_idx+1] = start_idx
		n = n//2

	return round_pointer_array.astype(int)

def generate_pointer_arrays(num_teams):
	total_games = num_teams - 1
	round_pointer_array = np.zeros(total_games)
	game_pointer_array = np.zeros(total_games)
	n = num_teams // 2
	end_idx = num_teams // 2
	old_start_idx = 0
	for i in range(1,int(np.log2(num_teams))):
		start_idx = end_idx
		end_idx = start_idx + n//2
		game_pointer_array[start_idx:end_idx+1] = start_idx
		round_pointer_array[start_idx:end_idx+1] = old_start_idx
		old_start_idx = start_idx
		n = n//2

	return game_pointer_array.astype(int), round_pointer_array.astype(int)

def generate_round_array(num_teams):
	total_games = num_teams - 1
	round_pointer_array = np.zeros(total_games)
	n = num_teams // 2
	end_idx = num_teams // 2
	for i in range(1,int(np.log2(num_teams))):
		start_idx = end_idx
		end_idx = start_idx + n//2
		round_pointer_array[start_idx:end_idx+1] = i
		n = n//2

	return round_pointer_array.astype(int)