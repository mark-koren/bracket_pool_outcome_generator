import os
import zipfile
from pathlib import Path
import streamlit as st
import pandas as pd
import shutil
import pickle
import numpy as np

from source.bracket_pdf_parser import load_or_generate_bracket_data, create_empty_score_csv_from_directory
from source.bracket_outcomes import load_or_generate_outcome_matrix
from source.bracket_pool_analyzer import load_or_generate_bracket_pool_scores, print_money_chances, \
    print_sweet_16_case_probabilities

from pages.utils import page_header, downloads_path, upload_folder, save_uploadedfile, markdown_file_downloader, \
    static_path, all_games_dict, optional_winner_selectbox, game_type_dict, team_id_dict, get_outcome_matrix, index_list_2021
from source.utils import generate_round_array


def individual_brackets(bracket_list, bracket_matrix, current_score_array, df_bracket_pool, score_array):
    page_header()

    if bracket_list is not None and bracket_matrix is not None and current_score_array is not None:
        st.header('4.0 Individual Brackets')

        outcome_matrix, likelihood_array = get_outcome_matrix(score_array)
        selected_outcome_matrix = outcome_matrix.copy()

        names = df_bracket_pool.sort_values('name').loc[:, 'name'].tolist()
        bracket_name = st.selectbox('Select a row to edit: ', names)
        print(bracket_name)
        df_bracket = df_bracket_pool[df_bracket_pool['name'] == bracket_name].copy()
        bracket_index = df_bracket['idx'].values[0]

        data_mode = st.selectbox('What do you want to do with the bracket pool data?',
                                 ['Inspect Data', 'Look at Scenarios'])
        if data_mode == 'Look at Scenarios':
            winner_dict = {}
            round_array = generate_round_array(16)
            for i in range(15):
                winner_dict[i] = None

            for i in range(0, 8):
                print(i)
                game_dict = all_games_dict[i]
                # winner = optional_winner_selectbox(game_name=game_dict['name'], team0=game_dict['team0'],
                #                                         team1=game_dict['team1'], i=i, index=2)
                option_list = [game_dict['team0'], game_dict['team1'], 'None']
                index = index_list_2021[i]
                if index == -1:
                    index = len(option_list) - 1
                winner = optional_winner_selectbox(game_name=game_dict['name'],
                                                   game_type=game_type_dict[round_array[i]],
                                                   option_list=option_list, i=-1, index=index)
                if winner == 'None':
                    winner = None
                winner_dict[i] = winner


            for i in range(8, 15):
                print(i)
                game_dict = all_games_dict[i]
                print(game_dict)
                team0 = winner_dict[game_dict['team0']]
                team1 = winner_dict[game_dict['team1']]
                print(team0)
                print(team1)
                print(game_dict['name'].format(team0=team0, team1=team1))
                print(team0 is not None)
                print(team1 is not None)
                if team0 is not None or team1 is not None:
                    option_list = []
                    if team0 is None:
                        team0 = 'Other'
                    else:
                        option_list.append(team0)
                    if team1 is None:
                        team1 = 'Other'
                    else:
                        option_list.append(team1)
                    option_list.append('None')
                    index = index_list_2021[i]
                    if index == -1:
                        index = len(option_list) - 1
                    winner = optional_winner_selectbox(game_name=game_dict['name'].format(team0=team0, team1=team1),
                                                       game_type=game_type_dict[round_array[i]],
                                                       option_list=option_list, i=-1, index=index)

                    if winner == 'None':
                        winner = None
                    winner_dict[i] = winner


            # score_array = np.array([4,8,16,32])
            for i in range(15):
                winner_key = winner_dict[i]
                if winner_key is not None:
                    winner_key = winner_key.lower()
                    winner_id = team_id_dict[winner_key]
                    winner_idx = winner_id * 4 + round_array[i]
                    winner_value = score_array[round_array[i]]

                    print(selected_outcome_matrix.shape)

                    selected_outcomes = selected_outcome_matrix[winner_idx, :] == winner_value
                    likelihood_array = likelihood_array[selected_outcomes]
                    selected_outcome_matrix = selected_outcome_matrix[:, selected_outcomes]

                    print(selected_outcome_matrix.shape)

        st.subheader('Who should I root for?')
        with st.spinner('Calculating Outcomes...'):
            total_outcomes = selected_outcome_matrix.shape[1]
            bracket_pool_scores = load_or_generate_bracket_pool_scores(static_path, bracket_matrix, selected_outcome_matrix,
                                                                       current_score_array, force_generation=False)

            # df_money_chances = print_money_chances(bracket_list, bracket_pool_scores)
            likelihood_array = likelihood_array / np.sum(likelihood_array)
            # df_money_chances = print_money_chances(bracket_list, bracket_pool_scores[bracket_index, :], likelihood_array)
            sweet_16_case_dict = print_sweet_16_case_probabilities(bracket_index, bracket_matrix, bracket_pool_scores, selected_outcome_matrix, likelihood_array)

            game = 0
            count_tracker = 0
            #
            # team0_dict['win_paths'] = team_0_win_count
            # team0_dict['win_paths_delta'] = team_0_win_count - base_total_paths
            # team0_dict['win_percent'] = team_0_win_count / total_outcomes * 100
            # team0_dict['win_percent_delta'] = team0_dict['win_percent'] - base_paths_percent
            # team0_dict['win_likelihood'] = np.sum(team_0_likeliood) * 100
            # team0_dict['win_likelihood_delta'] = team0_dict['win_likelihood'] - base_likelihood

            # st.write('<p style="color:green">THIS TEXT WILL BE RED</p>', unsafe_allow_html=True)6

            for key in sweet_16_case_dict.keys():
                if count_tracker == 0:
                    st.subheader('Game {game}: {game_name}'.format(
                        game=game,
                        game_name=all_games_dict[game]['name']
                    ))
                win_string = 'Win paths left if {team_name} wins: {win_paths} (Change: {win_paths_delta})'.format(
                        team_name=key,
                        win_paths=sweet_16_case_dict[key]['win_paths'],
                        win_paths_delta=sweet_16_case_dict[key]['win_paths_delta'],
                    )
                st.write(win_string)
                if sweet_16_case_dict[key]['win_percent_delta'] > 0:
                    color = 'green'
                elif sweet_16_case_dict[key]['win_percent_delta'] < 0:
                    color = 'red'
                else:
                    color = 'black'

                win_string = 'Win path percentages left if {team_name} wins: {win_percent:2f}% (Change: <font style="color:{color}">{win_percent_delta:2f}%</font>)'.format(
                    team_name=key,
                    win_percent=sweet_16_case_dict[key]['win_percent'],
                    win_percent_delta=sweet_16_case_dict[key]['win_percent_delta'],
                    color=color
                )
                # st.write(win_string)
                print(win_string)
                st.markdown(win_string, unsafe_allow_html=True)
                if sweet_16_case_dict[key]['win_likelihood_delta'] > 0:
                    color = 'green'
                elif sweet_16_case_dict[key]['win_likelihood_delta'] < 0:
                    color = 'red'
                else:
                    color = 'black'
                win_string = 'Win likelihood left if {team_name} wins: {win_likelihood:2f}% (Change: <font style="color:{color}">{win_likelihood_delta:2f}%</font>)'.format(
                    team_name=key,
                    win_likelihood=sweet_16_case_dict[key]['win_likelihood'],
                    win_likelihood_delta=sweet_16_case_dict[key]['win_likelihood_delta'],
                    color=color
                )
                print(win_string)
                st.write(win_string, unsafe_allow_html=True)
                game += count_tracker
                if count_tracker == 0:
                    count_tracker = 1
                else:
                    count_tracker = 0



