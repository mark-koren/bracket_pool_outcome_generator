import os
import zipfile
from pathlib import Path
import streamlit as st
import pandas as pd
import shutil
import pickle

from source.bracket_pdf_parser import load_or_generate_bracket_data, create_empty_score_csv_from_directory, \
    generate_bracket_df_from_directory, create_empty_score_csv_from_df, get_score_dict_from_df_csv, generate_bracket_data_from_df
from source.bracket_outcomes import load_or_generate_outcome_matrix
from source.bracket_pool_analyzer import load_or_generate_bracket_pool_scores, print_money_chances


from pages.utils import page_header, downloads_path, upload_folder, save_uploadedfile, markdown_file_downloader, static_path, pick_winner_selectbox

game0_dict = {'name': 'Gonzaga vs Creighton',
              'team0': 'Gonzaga',
              'team1': 'Creighton'}

game1_dict = {'name': 'USC vs Oregon',
              'team0': 'USC',
              'team1': 'Oregon'}

game2_dict = {'name': 'Michigan vs Florida St.',
              'team0': 'Michigan',
              'team1': 'Florida St.'}

game3_dict = {'name': 'UCLA vs Alabama',
              'team0': 'UCLA',
              'team1': 'Alabama'}

game4_dict = {'name': 'Baylor vs Villanova',
              'team0': 'Baylor',
              'team1': 'Villanova'}

game5_dict = {'name': 'Arkansas vs ORAL',
              'team0': 'Arkansas',
              'team1': 'ORAL'}

game6_dict = {'name': 'Loyola Chi. vs Oregon St.',
              'team0': 'Loyola Chi.',
              'team1': 'Oregon St.'}

game7_dict = {'name': 'Syracuse vs Houston',
              'team0': 'Syracuse',
              'team1': 'Houston'}

game8_dict = {'name': '{team0} vs {team1}',
              'team0': 0,
              'team1': 1}

game9_dict = {'name': '{team0} vs {team1}',
              'team0': 2,
              'team1': 3}

game10_dict = {'name': '{team0} vs {team1}',
               'team0': 4,
               'team1': 5}

game11_dict = {'name': '{team0} vs {team1}',
               'team0': 6,
               'team1': 7}

game12_dict = {'name': '{team0} vs {team1}',
               'team0': 8,
               'team1': 9}

game13_dict = {'name': '{team0} vs {team1}',
               'team0': 10,
               'team1': 11}

game14_dict = {'name': '{team0} vs {team1}',
               'team0': 12,
               'team1': 13}



all_games_dict = {0 : game0_dict,
                  1 : game1_dict,
                  2 : game2_dict,
                  3 : game3_dict,
                  4 : game4_dict,
                  5 : game5_dict,
                  6 : game6_dict,
                  7 : game7_dict,
                  8 : game8_dict,
                  9 : game9_dict,
                  10: game10_dict,
                  11: game11_dict,
                  12: game12_dict,
                  13: game13_dict,
                  14: game14_dict,
                  }

team_name_conversion_dict = {'gonzaga': 'Gonzaga',
                             'creighton': 'Creighton',
                             'usc': 'USC',
                             'oregon': 'Oregon',
                             'michigan': 'Michigan',
                             'florida St.': 'Florida St.',
                             'ucla': 'UCLA',
                             'alabama': 'Alabama',
                             'baylor': 'Baylor',
                             'villanova': 'Villanova',
                             'arkansas': 'Arkansas',
                             'oral': 'ORAL',
                             'loyola chi.': 'Loyola Chi.',
                             'oregon st.': 'Oregon St.',
                             'syracuse': 'Syracuse',
                             'houston': 'Houston',}


# def file_downloader():
#     st.markdown("Download from [test](downloads/mydata.csv) blahg")
#     mydataframe = pd.DataFrame.from_dict({'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']})
#     mydataframe.to_csv(str(downloads_path() / "mydata.csv"), index=False)


def unzip_pool_pdfs(uploaded_zip_file, force_generation):
    if uploaded_zip_file is not None:
        file_details = {"FileName": uploaded_zip_file.name, "FileType": uploaded_zip_file.type}
        print(file_details)
        print(uploaded_zip_file)

        zip_filepath = static_path().joinpath(uploaded_zip_file.name)
        if zip_filepath.exists() and force_generation:
            zip_filepath.unlink()
        print(zip_filepath)
        dir_filepath = zip_filepath.with_suffix('')
        if dir_filepath.exists() and force_generation:
            shutil.rmtree(dir_filepath)
        if not dir_filepath.exists():
            dir_filepath.mkdir()
        print(dir_filepath)

        pdfs_filepath = dir_filepath.joinpath('pdfs')
        if pdfs_filepath.exists():
            if force_generation:
                shutil.rmtree(dir_filepath)
                pdfs_filepath.mkdir()
            else:
                return pdfs_filepath, dir_filepath
        else:
            pdfs_filepath.mkdir()
        print(pdfs_filepath)

        save_uploadedfile(uploaded_zip_file, zip_filepath)
        zip_ref = zipfile.ZipFile(zip_filepath, 'r')
        zip_ref.extractall(pdfs_filepath)
        zip_ref.close()

        # zip_filepath.unlink()
        return pdfs_filepath, dir_filepath
    return None, None


def create_data_folder(uploaded_bracket_list, uploaded_bracket_matrix, uploaded_current_score_array, dir_filepath,
                       force_generation=False):
    if uploaded_bracket_list is not None and uploaded_bracket_matrix is not None and uploaded_current_score_array is not None:
        if dir_filepath.exists():
            if force_generation:
                shutil.rmtree(dir_filepath)
                dir_filepath.mkdir()
        else:
            dir_filepath.mkdir()
        print(dir_filepath)

        bracket_list_filepath = dir_filepath.joinpath(uploaded_bracket_list.name)
        if bracket_list_filepath.exists() and force_generation:
            bracket_list_filepath.unlink()
        if not bracket_list_filepath.exists():
            save_uploadedfile(uploaded_bracket_list, bracket_list_filepath)

        bracket_matrix_filepath = dir_filepath.joinpath(uploaded_bracket_matrix.name)
        if bracket_matrix_filepath.exists() and force_generation:
            bracket_matrix_filepath.unlink()
        if not bracket_matrix_filepath.exists():
            save_uploadedfile(uploaded_bracket_matrix, bracket_matrix_filepath)

        current_score_array_filepath = dir_filepath.joinpath(uploaded_current_score_array.name)
        if current_score_array_filepath.exists() and force_generation:
            current_score_array_filepath.unlink()
        if not current_score_array_filepath.exists():
            save_uploadedfile(uploaded_current_score_array, current_score_array_filepath)

        return bracket_list_filepath, bracket_matrix_filepath, current_score_array_filepath
    return None, None, None


def get_score_csv(uploaded_csv_file, pdfs_filepath, force_generation=False):
    if uploaded_csv_file is not None:
        file_details = {"FileName": uploaded_csv_file.name, "FileType": uploaded_csv_file.type}
        print(file_details)
        print(uploaded_csv_file)

        csv_filepath = pdfs_filepath.joinpath(uploaded_csv_file.name)
        print(csv_filepath)
        if csv_filepath.exists():
            if force_generation:
                csv_filepath.unlink()
            else:
                return csv_filepath

        save_uploadedfile(uploaded_csv_file, csv_filepath)

        return csv_filepath



@st.cache
def get_base_bracket_pool_df():
    df = pd.DataFrame(columns=['idx','name','current_score',0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
    # df = df.set_index('name')
    return df

def get_bracket_pool_df(df_location):
    if not df_location.is_file():
        print('Could not load: ', df_location, ' Generating base bracket')
        df = get_base_bracket_pool_df()
        df.to_pickle(df_location)
    else:
        df = pd.read_pickle(df_location)
        # if df.shape[0] > 0:
        #     df = df.set_index('name')
    return df

@st.cache
def get_index():
    return 0

def generate():
    df_bracket_pool_path = static_path() / 'df_bracket_pool.pkl'
    df_bracket_pool = get_bracket_pool_df(df_bracket_pool_path)
    page_header()

    st.header('1. Generate Bracket Pool Data')
    st.text('Already generated the data? Go to step 2.')

    st.subheader('1.1 Upload Bracket Pool PDFs')
    st.text('Select the organization that hosts your bracket pool.')
    pool_type = st.radio('Bracket Pool Type:', ('CBS', 'ESPN', 'OTHER'))

    generated_pdf_dir = False
    pdfs_filepath = None
    dir_filepath = None
    force_generation = False
    bracket_list = None
    bracket_matrix = None
    current_score_array = None
    if pool_type == 'CBS' or pool_type == 'ESPN':

        st.write(
            'If you are part of a CBS Sports or ESPN bracket pool, I can generate everything automatically. Upload a zip folder containing a pdf of every persons bracket:')
        force_generation_radio = st.radio('Force Generation?:', ('Yes', 'No'), index=1)
        if force_generation_radio == 'Yes':
            force_generation = True
        uploaded_pdfs = st.file_uploader('Upload zipped folder of bracket pdfs:')
        pdfs_filepath, dir_filepath = unzip_pool_pdfs(uploaded_pdfs, force_generation)
        if pdfs_filepath is not None:
            if df_bracket_pool.shape[0] > 0:
                generated_pdf_dir = True
            if st.button('Generate Bracket Pool from PDFs'):
                with st.spinner('Generating Bracket Pool from PDFs...'):
                    generation_progress = st.progress(0.0)
                    try:
                        df_bracket_pool = generate_bracket_df_from_directory(pdfs_filepath, pool_type=pool_type, progress_bar=generation_progress.progress)
                        print(df_bracket_pool.head())
                        df_bracket_pool.to_pickle(df_bracket_pool_path)
                        generated_pdf_dir = True
                    except:
                        st.error(
                            'Sorry, something went wrong and I couldn\'t generate the empty score csv. Maybe double check your input and try again?')
                        st.stop()

    else:
        generated_pdf_dir = True

    if generated_pdf_dir:
        default_winners = [0]*15
        data_mode = st.selectbox('What do you want to do with the bracket pool data?', ['Inspect Data', 'Add a Bracket', 'Edit a Bracket', 'Change Current Scores'])
        bracket_dict = {}
        if data_mode == 'Change Current Scores':
            st.write('There are two ways to do this. You can use the \'Edit a Bracket\' option to modify each score one by one. Or you can generate and download a csv file of scores below. Edit the file (make sure it still saves as a csv!), upload it, and then click update.')
            # if st.button('Generate Empty current_scores.csv'):
            df_empty_scores = create_empty_score_csv_from_df(df_bracket_pool)
            df_empty_scores_path = downloads_path() / 'empty_current_scores.csv'
            if df_empty_scores_path.is_file():
                df_empty_scores_path.unlink()
            df_empty_scores.to_csv(df_empty_scores_path)

            download_text = 'Download empty [{link_text}]({download_path}).'
            download_path = 'downloads/' + df_empty_scores_path.name
            markdown_file_downloader(text=download_text, link_text='current_scores.csv', download_path=download_path)

            uploaded_current_scores = st.file_uploader('Upload updated current_scores.csv:')
            if uploaded_current_scores is not None:
                current_scores_dict = get_score_dict_from_df_csv(uploaded_current_scores)
                for key in current_scores_dict.keys():
                    print(key)
                    if key in df_bracket_pool.name.values:
                        df_bracket_pool.loc[df_bracket_pool.name == key, 'current_score'] = current_scores_dict[key]
                # current_scores = pd.read_csv(uploaded_current_scores)
                # print(df_current_scores.columns)
                # for index, row in df_current_scores.iterrows():
                #     print(index, row)
                #     if row.name in df_bracket_pool.name.values:
                #         print(row.name)
                #         df_bracket_pool[df_bracket_pool.name == row.name].current_score = row.current_score

            df_bracket_pool.to_pickle(df_bracket_pool_path)


        if data_mode == 'Edit a Bracket':
            names = df_bracket_pool.sort_values('name').loc[:, 'name'].tolist()
            edit_row_name = st.selectbox('Select a row to edit: ', names)
            df_edit_row = df_bracket_pool[df_bracket_pool.name == edit_row_name].copy()
            default_bracket_name = df_edit_row.name.values[0]
            default_bracket_score = df_edit_row.current_score.values[0]
            for i in range(15):
                game_winner = df_edit_row[i].values[0]
                if game_winner in team_name_conversion_dict:
                    game_winner = team_name_conversion_dict[game_winner]
                else:
                    game_winner = 'Other-' + str(i)
                game_dict = all_games_dict[i]
                if i < 8:
                    team0 = game_dict['team0']
                    team1 = game_dict['team1']
                else:
                    team0 = bracket_dict[game_dict['team0']]
                    team1 = bracket_dict[game_dict['team1']]
                if team0 == game_winner:
                    default_winners[i] = 0
                elif team1 == game_winner:
                    default_winners[i] = 1
                else:
                    default_winners[i] = 2
                bracket_dict[i] = game_winner

        if data_mode == 'Add a Bracket':
            # st.text('Sorry, I only support CBS and ESPN for now, but I am working to expand on this ASAP!')
            st.text('Enter the info for each bracket:')
            default_bracket_name = 'bracket_1'
            default_bracket_score = 0

            for i in range(15):
                bracket_dict[i] = None


        if data_mode == 'Add a Bracket' or data_mode == 'Edit a Bracket':
            bracket_name = st.text_input('Bracket Name (No spaces, no duplicate names):', value=default_bracket_name)
            current_score = st.number_input('Current bracket score:', value=default_bracket_score)
            print(bracket_name, current_score)
            bracket_dict['name'] = bracket_name
            bracket_dict['current_score'] = current_score

            game_dict = all_games_dict[0]
            # selectbox_text = 'Please select the winner of ' + game_dict['name'] + ':'
            # game_winner = st.selectbox(selectbox_text, [game_dict['team0'], game_dict['team1'], 'Other-' + str(0)])
            game_winner = pick_winner_selectbox(game_name=game_dict['name'], team0=game_dict['team0'], team1=game_dict['team1'], i=0, index=default_winners[0])
            bracket_dict[0] = game_winner

            for i in range(1, 8):
                if bracket_dict[i-1] is not None:
                    print(i)
                    game_dict = all_games_dict[i]
                    bracket_dict[i] = pick_winner_selectbox(game_name=game_dict['name'], team0=game_dict['team0'], team1=game_dict['team1'], i=i, index=default_winners[i])

            for i in range(8, 15):
                if bracket_dict[i-1] is not None:
                    print(i)
                    game_dict = all_games_dict[i]
                    print(game_dict)
                    team0 = bracket_dict[game_dict['team0']]
                    team1 = bracket_dict[game_dict['team1']]
                    print(team0)
                    print(team1)
                    print(game_dict['name'].format(team0=team0, team1=team1))
                    if team0 is not None and team1 is not None:
                        bracket_dict[i] = pick_winner_selectbox(game_name=game_dict['name'].format(team0=team0, team1=team1), team0=team0,
                                              team1=team1, i=i, index=default_winners[i])

            print(bracket_dict)

            idx = df_bracket_pool.shape[0]
            bracket_dict['idx'] = idx
            # Turn into lists of 1 for dataframe conversion
            for key in bracket_dict.keys():
                bracket_dict[key] = [bracket_dict[key]]
            # df_bracket = pd.DataFrame(data=bracket_dict, index=index)
            df_bracket = pd.DataFrame(data=bracket_dict)
            st.text('Current Bracket:')
            st.dataframe(df_bracket)
            st.text('Look Correct?:')

        if data_mode == 'Add a Bracket':
            add_to_table = st.button('Add to table')
            if add_to_table:
                if bracket_dict['name'][0] in df_bracket_pool.name.values:
                    st.warning('Can\t add bracket: bracket name already exists in the bracket pool!')
                else:
                    df_bracket_pool = df_bracket_pool.append(df_bracket)
                    print(df_bracket_pool.head())
                    df_bracket_pool.to_pickle(df_bracket_pool_path)

        if data_mode == 'Edit a Bracket':
            update_table = st.button('Update Bracket')
            if update_table:
                print(df_edit_row)
                print(df_bracket)
                # df_bracket = pd.DataFrame(data=bracket_dict)
                df_bracket_pool[df_bracket_pool.name == edit_row_name] = df_bracket
                df_bracket_pool.to_pickle(df_bracket_pool_path)
            # print(df_bracket_pool.head())


        st_df_bracket_pool = st.dataframe(df_bracket_pool)
        if df_bracket_pool.shape[0] > 0:
            st.text('Make a mistake? (WARNING: These can not be undone:')
            print(df_bracket_pool.loc[:,'name'].tolist())
            delete_row_name = st.selectbox('Select a row to delete: ', df_bracket_pool.loc[:,'name'].tolist())
            if st.button('Delete Row'):
                print(delete_row_name)
                df_bracket_pool = df_bracket_pool[df_bracket_pool.name != delete_row_name]
                df_bracket_pool.to_pickle(df_bracket_pool_path)
                st_df_bracket_pool.dataframe(df_bracket_pool)
                # df_bracket_pool.drop(delete_row)
                # df_bracket_pool.to_pickle(df_bracket_pool_path)

            if st.button('Clear All'):
                df_bracket_pool_path.unlink()
                df_bracket_pool = get_bracket_pool_df(df_bracket_pool_path)
                st_df_bracket_pool.dataframe(df_bracket_pool)

            st.subheader('Generate Bracket Pool Data')
            st.text('Everything look correct? Generate the data, download it, and upload it into the slider bar')

            if st.button('Generate Bracket Pool Data!'):
                bracket_list, bracket_matrix, current_score_array = generate_bracket_data_from_df(df_bracket_pool)
                bracket_pool_data_dict = {'bracket_list': bracket_list,
                                          'bracket_matrix': bracket_matrix,
                                          'current_score_array': current_score_array,
                                          'df_bracket_pool': df_bracket_pool}

                bracket_pool_data_dict_path = downloads_path() / 'bracket_pool_data.pkl'
                with bracket_pool_data_dict_path.open('wb') as f:
                    pickle.dump(bracket_pool_data_dict, f)
                download_text = 'Download [{link_text}]({download_path}).'
                download_path = 'downloads/' + bracket_pool_data_dict_path.name
                markdown_file_downloader(text=download_text, link_text='bracket_pool_data.pkl',
                                         download_path=download_path)











    # csv_filepath = None
    # if generated_pdf_dir and pdfs_filepath is not None and dir_filepath is not None:
    #     st.subheader('1.2 Upload Current Score csv')
    #     st.text('Upload a csv that designates the current score for each bracket.')
    #     uploaded_score_csv = st.file_uploader('Upload current_scores.csv:')
    #     csv_filepath = get_score_csv(uploaded_score_csv, pdfs_filepath, force_generation=force_generation)
    #     if csv_filepath is not None:
    #         # TODO: Add progress bar
    #         try:
    #             bracket_list, bracket_matrix, current_score_array = load_or_generate_bracket_data(pdfs_filepath,
    #                                                                                               pool_type=pool_type,
    #                                                                                               force_generation=force_generation)
    #
    #             print(bracket_list)
    #
    #             bracket_list_path = pdfs_filepath.joinpath('bracket_list.pkl')
    #             download_bracket_list_path = downloads_path() / bracket_list_path.name
    #             shutil.copy(str(bracket_list_path), str(download_bracket_list_path))
    #
    #             download_path = 'downloads/' + bracket_list_path.name
    #             download_text = 'Download the [{link_text}]({download_path}).'
    #             markdown_file_downloader(text=download_text, link_text='bracket list', download_path=download_path)
    #
    #             bracket_matrix_path = pdfs_filepath.joinpath('bracket_matrix.pkl')
    #             download_bracket_matrix_path = downloads_path() / bracket_matrix_path.name
    #             shutil.copy(str(bracket_matrix_path), str(download_bracket_matrix_path))
    #
    #             download_path = 'downloads/' + bracket_matrix_path.name
    #             download_text = 'Download the [{link_text}]({download_path}).'
    #             markdown_file_downloader(text=download_text, link_text='bracket matrix', download_path=download_path)
    #
    #             current_score_array_path = pdfs_filepath.joinpath('current_score_array.pkl')
    #             download_current_score_array_path = downloads_path() / current_score_array_path.name
    #             shutil.copy(str(current_score_array_path), str(download_current_score_array_path))
    #
    #             download_path = 'downloads/' + current_score_array_path.name
    #             download_text = 'Download the [{link_text}]({download_path}).'
    #             markdown_file_downloader(text=download_text, link_text='current score array', download_path=download_path)
    #
    #             # shutil.rmtree(pdfs_filepath)
    #         except:
    #             st.error(
    #                 'Sorry, something went wrong and I couldn\'t generate the empty score csv. Maybe double check your input and try again?')
    #             st.stop()




    # st.header('2.0 Upload Bracket Pool Data')
    # st.text('If you have already generated your bracket pool data, upload it now: ')
    #
    # uploaded_bracket_list = st.file_uploader('Upload bracket_list.pkl:')
    # uploaded_bracket_matrix = st.file_uploader('Upload bracket_matrix.pkl:')
    # uploaded_current_score_array = st.file_uploader('Upload current_score_array.pkl:')
    #
    # bracket_list_filepath, bracket_matrix_filepath, current_score_array_filepath = create_data_folder(uploaded_bracket_list,
    #                                                                                                   uploaded_bracket_matrix,
    #                                                                                                   uploaded_current_score_array,
    #                                                                                                   dir_filepath,
    #                                                                                                   force_generation=False)
    # if bracket_list_filepath is not None:
    #     with bracket_list_filepath.open('rb') as f:
    #         bracket_list = pickle.load(f)
    #
    #     with bracket_matrix_filepath.open('rb') as f:
    #         bracket_matrix = pickle.load(f)
    #
    #     with current_score_array_filepath.open('rb') as f:
    #         current_score_array = pickle.load(f)
    #
