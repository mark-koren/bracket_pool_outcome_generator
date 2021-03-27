import numpy as np
import pdb
import itertools
from tqdm import tqdm
from pathlib import Path
import pickle

# from bracket_pdf_parser import *
from source.utils import generate_round_array, generate_pointer_arrays

# def generate_bracket_from_dict(num_teams):
# 	max_games_per_team = np.log2(num_teams)
# 	bracket = np.zeros((num_teams, max_games_per_team))
# 	return

def generate_bracket_truth_table(num_teams):
	single_game_outcome = [0,1]
	total_games = num_teams - 1
	# max_games_per_team = int(np.log2(num_teams))
	return np.array(list(itertools.product(single_game_outcome, repeat=total_games))).astype(int)

def bracket_truth_table_generator(num_teams):
	single_game_outcome = [0,1]
	total_games = num_teams - 1
	# max_games_per_team = int(np.log2(num_teams))
	return itertools.product(single_game_outcome, repeat=total_games)

def generate_outcome_matrix(num_teams, score_array=None):
	# num_teams = 16
	round_array = generate_round_array(num_teams)
	game_pointer_array, round_pointer_array = generate_pointer_arrays(num_teams)
	if score_array is None:
		score_array = np.array([4,8,16,32])

	max_games_per_team = int(np.log2(num_teams))
	total_games = num_teams - 1

	# Create everything using generators
	row_list = []
	for truthtable_row in tqdm(bracket_truth_table_generator(num_teams), total=2**total_games):
		outcome_row = generate_outcome_row(num_teams, total_games, max_games_per_team, truthtable_row, round_array,
										   round_pointer_array, game_pointer_array, score_array)
		row_list.append(outcome_row.reshape((-1,1)))

	outcome_matrix = np.hstack(row_list)
	# This  was the preallocation method
	# bracket_truth_table = generate_bracket_truth_table(num_teams)
	#
	# outcome_matrix = np.zeros((bracket_truth_table.shape[0], num_teams * max_games_per_team))
	#
	# # random_row = np.random.choice(np.arange(bracket_truth_table.shape[0]))
	# for row in tqdm(range(bracket_truth_table.shape[0])):
	# 	game_outcome_array = bracket_truth_table[row,:]
	#
	# 	outcome_row = generate_outcome_row(num_teams, total_games, max_games_per_team, game_outcome_array, round_array, round_pointer_array, game_pointer_array, score_array)
	# 	outcome_matrix[row, :] = outcome_row.reshape((1,-1))
	# print(game_outcome_array)
	# print(outcome_row)
	return outcome_matrix

def save_outcome_matrix(dir_path, outcome_matrix, num_teams=16):
	dirpath = Path(dir_path)
	assert (dirpath.is_dir())
	outcome_matrix_filename = 'outcome_matrix_' + str(num_teams) + '.pkl'
	outcome_matrix_path = dirpath / outcome_matrix_filename
	with outcome_matrix_path.open('wb') as file:
		pickle.dump(outcome_matrix, file)

def load_outcome_matrix(dir_path, num_teams=16):
	dirpath = Path(dir_path)
	assert (dirpath.is_dir())
	outcome_matrix_filename = 'outcome_matrix_' + str(num_teams) + '.pkl'
	outcome_matrix_path = dirpath / outcome_matrix_filename
	assert outcome_matrix_path.is_file()
	with outcome_matrix_path.open('rb') as file:
		outcome_matrix = pickle.load(file)

	return outcome_matrix

def load_or_generate_outcome_matrix(dir_path, num_teams=16, score_array=None, force_generation=False):
	try:
		assert not force_generation
		outcome_matrix = load_outcome_matrix(dir_path, num_teams)
	except:
		print('Failed to load outcome matrix -- generating and saving a new outcome matrix')
		outcome_matrix = generate_outcome_matrix(num_teams, score_array)
		save_outcome_matrix(dir_path, outcome_matrix, num_teams=16)
	finally:
		return outcome_matrix

def generate_outcome_row(num_teams, total_games, max_games_per_team, game_outcome_array, round_array, round_pointer_array, game_pointer_array, score_array):
	winner_tracker = np.arange(num_teams).astype(int)
	team_score_row = np.zeros((num_teams, max_games_per_team)).astype(int)

	for i in range(total_games):
		# pdb.set_trace()
		round_pointer = round_pointer_array[i]
		game_pointer = game_pointer_array[i]
		winner_tracker_index = game_outcome_array[i] + 2 * (i - game_pointer) + round_pointer
		team_index = winner_tracker[winner_tracker_index]
		winner_tracker[i] = team_index
		team_score_row[team_index, round_array[i]] = score_array[round_array[i]]
		# print(i)
		# pdb.set_trace()

	return team_score_row





if __name__ == '__main__':
	num_teams = 16
	pdb.set_trace()
	truth_table = generate_bracket_truth_table(num_teams)
	outcome_matrix = load_or_generate_outcome_matrix('../', num_teams, force_generation=False)
	pdb.set_trace()
	print('done')
	# load_outcome_matrix('./', num_teams=16)
	# generate_outcome_matrix(num_teams=16)
	# round_array = generate_round_array(num_teams)
	# # round_pointer_array = generate_round_pointer_array(num_teams)
	# # game_pointer_array = generate_game_pointer_array(num_teams)
	# game_pointer_array, round_pointer_array = generate_pointer_arrays(num_teams)
	# score_array = np.array([4,8,16,32])

	# # print(round_array)
	# # print(round_pointer_array)
	# # print(game_pointer_array)
	

	# max_games_per_team = int(np.log2(num_teams))
	# # total_games = num_teams - 1
	# # winner_tracker = np.arange(num_teams)
	# total_games = num_teams - 1

	# bracket_truth_table = generate_bracket_truth_table(num_teams)

	# random_row = np.random.choice(np.arange(bracket_truth_table.shape[0]))
	# game_outcome_array = bracket_truth_table[random_row,:]

	# # game_outcome_array = np.array([0, 0, 0, 0, 1, 0, 1])

	# outcome_row = generate_outcome_row(num_teams, total_games, max_games_per_team, game_outcome_array, round_array, round_pointer_array, game_pointer_array, score_array)
	# print(game_outcome_array)
	# print(outcome_row)
	# from brackets import *
	#
	# outcome_matrix = generate_outcome_matrix(num_teams)
	# # print(outcome_matrix)
	#
	# # mark_koren_scores = np.array(mark_koren['bracket']).dot(outcome_matrix) + mark_koren['score']
	# mark_koren_scores = outcome_matrix.dot(np.array(mark_koren['bracket'])) + mark_koren['score']
	# matt_jones_scores = outcome_matrix.dot(np.array(matt_jones['bracket'])) + matt_jones['score']
	# # matt_jones_scores = np.array(matt_jones['bracket']).dot(outcome_matrix) + matt_jones['score']
	#
	# koren_win_cases = np.sum((mark_koren_scores > matt_jones_scores).astype(int))
	#
	# print(koren_win_cases / mark_koren_scores.shape[0])

	# print(np.array(mark_koren_4).dot(outcome_matrix))
	# print(np.array(dom_hawkins_4).dot(outcome_matrix))
	# print(np.array(matt_jones_4).dot(outcome_matrix))

	# mark_koren_dict = get_bracket_dict('./mark_koren.pdf')
	# print(mark_koren_dict)
	# mark_koren_array = get_bracket_array(mark_koren_dict)
	# print(mark_koren_array)