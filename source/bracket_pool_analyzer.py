import pdb
import numpy as np
from pathlib import Path
import pickle
import pandas as pd

from source.bracket_pdf_parser import load_or_generate_bracket_data
from source.bracket_outcomes import load_or_generate_outcome_matrix

team_name_dict = {
    0:'gonzaga',
    1:'creighton',
    2:'usc',
    3:'oregon',
    4:'michigan',
    5:'florida st.',
    6:'ucla',
    7:'alabama',
    8:'baylor',
    9:'villanova',
    10:'arkansas',
    11:'oral',
    12:'loyola chi.',
    13:'oregon st.',
    14:'syracuse',
    15:'houston',
}

def generate_bracket_pool_scores(bracket_matrix, outcome_matrix, current_score_array):
	return bracket_matrix.dot(outcome_matrix) + current_score_array

def save_bracket_pool_scores(bracket_dir_path, bracket_pool_scores):
    dirpath = Path(bracket_dir_path)
    assert (dirpath.is_dir())

    bracket_pool_scores_filename = 'bracket_pool_scores.pkl'
    bracket_pool_scores_path = dirpath / bracket_pool_scores_filename
    with bracket_pool_scores_path.open('wb') as file:
        pickle.dump(bracket_pool_scores, file)


def load_bracket_pool_scores(bracket_dir_path):
    dirpath = Path(bracket_dir_path)
    assert (dirpath.is_dir())

    bracket_pool_scores_filename = 'bracket_pool_scores.pkl'
    bracket_pool_scores_path = dirpath / bracket_pool_scores_filename
    assert bracket_pool_scores_path.is_file()

    with bracket_pool_scores_path.open('rb') as file:
        bracket_pool_scores = pickle.load(file)

    return bracket_pool_scores


def load_or_generate_bracket_pool_scores(bracket_dir_path, bracket_matrix, outcome_matrix, current_score_array, force_generation=False):
    try:
        assert not force_generation
        bracket_pool_scores = load_bracket_pool_scores(bracket_dir_path)
    except:
        print('Failed to load bracket pool score matrix -- generating and saving new bracket pool score matrix')
        bracket_pool_scores = generate_bracket_pool_scores(bracket_matrix, outcome_matrix, current_score_array)
        save_bracket_pool_scores(bracket_dir_path, bracket_pool_scores)
    finally:
        return bracket_pool_scores

def print_money_chances(bracket_list, bracket_pool_scores):
    # df_bracket_pool_scores = pd.DataFrame(data=bracket_pool_scores)
    df_bracket_names = pd.DataFrame([bracket_info['name'] for bracket_info in bracket_list], columns=['bracket_names'])
    # df_bracket_pool_scores = pd.concat([df_bracket_names,df_bracket_pool_scores],axis=1)
    # print(df_bracket_pool_scores.head())

    first_place_bracket_pool_scores = bracket_pool_scores.copy()
    first_place_bracket_pool_scores[np.where(np.not_equal(bracket_pool_scores,np.amax(bracket_pool_scores, axis=0)))] = 0
    first_place_bracket_pool_scores[np.where(np.not_equal(first_place_bracket_pool_scores, 0))] = 1
    
    first_place_tie_tracker = np.sum(first_place_bracket_pool_scores, axis=0)
    first_place_tied_counts = np.sum(first_place_bracket_pool_scores[:, first_place_tie_tracker > 1], axis=1).reshape(-1,1)
    first_place_no_ties_count = np.sum(first_place_bracket_pool_scores, axis=1).reshape(-1,1) - first_place_tied_counts

    second_place_bracket_pool_scores = bracket_pool_scores.copy()
    # Remove 1st place scores from each column
    second_place_bracket_pool_scores[np.where(np.equal(bracket_pool_scores, np.amax(bracket_pool_scores, axis=0)))] = 0
    second_place_bracket_pool_scores[np.where(np.not_equal(second_place_bracket_pool_scores,np.amax(second_place_bracket_pool_scores, axis=0)))] = 0
    second_place_bracket_pool_scores[np.where(np.not_equal(second_place_bracket_pool_scores, 0))] = 1
    # If two or more tied for first, no one gets second
    second_place_bracket_pool_scores[:, first_place_tie_tracker >= 2] = 0

    second_place_tie_tracker = np.sum(second_place_bracket_pool_scores, axis=0)
    second_place_tied_counts = np.sum(second_place_bracket_pool_scores[:, second_place_tie_tracker > 1], axis=1).reshape(-1,1)
    second_place_no_ties_count = np.sum(second_place_bracket_pool_scores, axis=1).reshape(-1,1) - second_place_tied_counts

    third_place_bracket_pool_scores = bracket_pool_scores.copy()
    # Remove 1st place scores from each column
    third_place_bracket_pool_scores[np.where(np.equal(bracket_pool_scores, np.amax(third_place_bracket_pool_scores, axis=0)))] = 0
    # Remove 2nd place scores from each column
    third_place_bracket_pool_scores[np.where(np.equal(bracket_pool_scores, np.amax(third_place_bracket_pool_scores, axis=0)))] = 0
    third_place_bracket_pool_scores[np.where(np.not_equal(third_place_bracket_pool_scores, np.amax(third_place_bracket_pool_scores, axis=0)))] = 0
    third_place_bracket_pool_scores[np.where(np.not_equal(third_place_bracket_pool_scores, 0))] = 1
    # If three or more tied for first, no one gets third
    third_place_bracket_pool_scores[:, first_place_tie_tracker >= 3] = 0
    # If two or more tied for second, no one gets third
    third_place_bracket_pool_scores[:, second_place_tie_tracker >= 2] = 0

    third_place_tie_tracker = np.sum(third_place_bracket_pool_scores, axis=0)
    third_place_tied_counts = np.sum(third_place_bracket_pool_scores[:, third_place_tie_tracker > 1], axis=1).reshape(-1,1)
    third_place_no_ties_count = np.sum(third_place_bracket_pool_scores, axis=1).reshape(-1,1) - third_place_tied_counts
    df_place_counts = pd.DataFrame(data=np.hstack([first_place_no_ties_count, first_place_tied_counts, second_place_no_ties_count, second_place_tied_counts, third_place_no_ties_count,third_place_tied_counts ]), columns=['first_alone', 'first_tied', 'second_alone', 'second_tied', 'third_alone', 'third_tied'])

    # pdb.set_trace()
    return pd.concat([df_bracket_names,df_place_counts],axis=1)

def print_money_paths_for_index(bracket_index, bracket_matrix, bracket_pool_scores, outcome_matrix):
    max_value_per_case = np.amax(bracket_pool_scores, axis=0)
    paths = outcome_matrix[:, bracket_pool_scores[bracket_index, :] == max_value_per_case]
    no_zaga = paths[:,paths[3,:] != 32]
    pdb.set_trace()

def print_sweet_16_case_probabilities(bracket_index, bracket_matrix, bracket_pool_scores, outcome_matrix):
    max_value_per_case = np.amax(bracket_pool_scores, axis=0)
    paths = outcome_matrix[:, bracket_pool_scores[bracket_index, :] == max_value_per_case]
    for i in range(0,16,2):
        # pdb.set_trace()
        team_0_wins = paths[:,paths[i * 4,:] == 4]
        if team_0_wins.size:
            team_0_win_count = team_0_wins.shape[1]
        else:
            team_0_win_count = 0
        print('Win paths left if {team_name} wins: {win_count} ({win_percent:.2f}%)'.format(
            team_name=team_name_dict[i],
            win_count=team_0_win_count,
            win_percent=team_0_win_count/32768*100,
        ))

        team_1_wins = paths[:,paths[(i + 1) * 4,:] == 4]
        if team_1_wins.size:
            team_1_win_count = team_1_wins.shape[1]
        else:
            team_1_win_count = 0
        print('Win paths left if {team_name} wins: {win_count} ({win_percent:.2f}%)'.format(
            team_name=team_name_dict[(i + 1)],
            win_count=team_1_win_count,
            win_percent=team_1_win_count/32768*100,
        ))

if __name__ == '__main__':
    num_teams = 16
    data_dir_path = '../'
    bracket_dir_path = '../aj_ellis_co'
    outcome_matrix = load_or_generate_outcome_matrix(data_dir_path, num_teams)
    bracket_list, bracket_matrix, current_score_array = load_or_generate_bracket_data(bracket_dir_path, force_generation=False)
    # print(bracket_list)
    # print(bracket_matrix)
    # print(current_score_array)
    bracket_pool_scores = load_or_generate_bracket_pool_scores(bracket_dir_path, bracket_matrix, outcome_matrix,
                                                               current_score_array, force_generation=False)
    # pdb.set_trace()
    for bracket_info in bracket_list:
        if bracket_info['name'] == 'mark_koren':
            bracket_index = bracket_info['idx']
    # print_money_paths_for_index(bracket_index, bracket_matrix, bracket_pool_scores, outcome_matrix)
    print_sweet_16_case_probabilities(bracket_index, bracket_matrix, bracket_pool_scores, outcome_matrix)
    # df_money_chances = print_money_chances(bracket_list, bracket_pool_scores)
    # df_money_chances.to_csv(Path(bracket_dir_path + '/money_chances.csv'))
    # bracket_list, bracket_matrix = get_brackets_from_directory('./aj_ellis_co')
    # print(bracket_list)
    # print(bracket_matrix)


