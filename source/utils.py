import numpy as np
import pdb
import itertools
from tqdm import tqdm

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