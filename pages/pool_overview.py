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
from source.bracket_pool_analyzer import load_or_generate_bracket_pool_scores, print_money_chances


from pages.utils import page_header, downloads_path, upload_folder, save_uploadedfile, markdown_file_downloader, \
    static_path, pick_winner_selectbox, all_games_dict, optional_winner_selectbox, game_type_dict, team_id_dict, \
    get_outcome_matrix
from source.utils import generate_round_array



def pool_overview(bracket_list, bracket_matrix, current_score_array, df_bracket_pool, score_array):
    page_header()

    if bracket_list is not None and bracket_matrix is not None and current_score_array is not None:
        st.header('3.0 Bracket Pool Results')

        outcome_matrix = get_outcome_matrix(score_array)
        # print(outcome_matrix)
        selected_outcome_matrix = outcome_matrix.copy()
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
                winner = optional_winner_selectbox(game_name=game_dict['name'],
                                                   game_type=game_type_dict[round_array[i]],
                                                   option_list=[game_dict['team0'], game_dict['team1'], 'None'], i=-1, index=2)
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
                    winner = optional_winner_selectbox(game_name=game_dict['name'].format(team0=team0, team1=team1),
                                                       game_type=game_type_dict[round_array[i]],
                                                       option_list=option_list, i=-1, index=len(option_list)-1)

                    if winner == 'None':
                        winner = None
                    winner_dict[i] = winner


            score_array = np.array([4,8,16,32])
            for i in range(15):
                winner_key = winner_dict[i]
                if winner_key is not None:
                    winner_key = winner_key.lower()
                    winner_id = team_id_dict[winner_key]
                    winner_idx = winner_id * 4 + round_array[i]
                    winner_value = score_array[round_array[i]]

                    print(selected_outcome_matrix.shape)

                    selected_outcome_matrix = selected_outcome_matrix[:, selected_outcome_matrix[winner_idx, :] == winner_value]
                    print(selected_outcome_matrix.shape)


        with st.spinner('Calculating Outcomes...'):
            bracket_pool_scores = load_or_generate_bracket_pool_scores(static_path, bracket_matrix, selected_outcome_matrix,
                                                                       current_score_array, force_generation=False)

            df_money_chances = print_money_chances(bracket_list, bracket_pool_scores)
        #columns=['first_alone', 'first_tied', 'second_alone', 'second_tied', 'third_alone', 'third_tied']
        total_cases = selected_outcome_matrix.shape[1]
        if total_cases > 0:
            df_money_chances_with_percents = df_money_chances.copy()
            df_money_chances_with_percents['first_alone_percent'] = df_money_chances.first_alone / total_cases * 100
            df_money_chances_with_percents['first_tied_percent'] = df_money_chances.first_tied / total_cases * 100
            df_money_chances_with_percents['second_alone_percent'] = df_money_chances.second_alone / total_cases * 100
            df_money_chances_with_percents['second_tied_percent'] = df_money_chances.second_tied / total_cases * 100
            df_money_chances_with_percents['third_alone_percent'] = df_money_chances.third_alone / total_cases * 100
            df_money_chances_with_percents['third_tied_percent'] = df_money_chances.third_tied / total_cases * 100

            df_money_chances_with_percents = df_money_chances_with_percents[['bracket_names',
                                                                            'first_alone', 'first_alone_percent',
                                                                            'first_tied', 'first_tied_percent',
                                                                            'second_alone', 'second_alone_percent',
                                                                            'second_tied', 'second_tied_percent',
                                                                            'third_alone', 'third_alone_percent',
                                                                            'third_tied', 'third_tied_percent', ]]

            st.dataframe(df_money_chances_with_percents)
        else:
            st.warning('It is impossible to achieve this combination of selected winners (How did you even do this??)')

