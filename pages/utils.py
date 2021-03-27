import streamlit as st
from pathlib import Path

from source.bracket_outcomes import load_or_generate_outcome_matrix

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


team_id_dict = {
    'gonzaga':0,
    'creighton':1,
    'usc':2,
    'oregon':3,
    'michigan':4,
    'florida st.':5,
    'florida state':5,
    'ucla':6,
    'alabama':7,
    'baylor':8,
    'villanova':9,
    'arkansas':10,
    'oral':11,
    'loyola chi.':12,
    'oregon st.':13,
    'syracuse':14,
    'houston':15,
}

game_type_dict = {
    0: 'Sweet 16',
    1: 'Elite 8',
    2: 'Final 4',
    3: 'National Championship Game',
}

@st.cache
def get_outcome_matrix(score_array):
    outcome_matrix = load_or_generate_outcome_matrix(static_path(), num_teams=16, score_array=score_array, force_generation=True)
    # print(outcome_matrix)
    return outcome_matrix

def page_header():
    st.title('So you\'re saying there\'s a chance!?!')
    st.header('Bracket pool outcome generator')
    st.subheader('By: Mark Koren')
    st.markdown('[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L4L242M4H)')

def save_uploadedfile(uploadedfile, save_destination):
    with save_destination.open('wb') as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{filename} to {save_destination}".format(filename=uploadedfile.name,
                                                                           save_destination=save_destination))

def markdown_file_downloader(text, link_text, download_path):
    markdown_string = text.format(link_text=link_text, download_path=download_path)
    print(markdown_string)
    st.markdown(markdown_string)

def upload_folder():
    UPLOAD_FOLDER = Path.cwd().joinpath('data')
    if not UPLOAD_FOLDER.is_dir():
        UPLOAD_FOLDER.mkdir()
    return UPLOAD_FOLDER

# HACK This only works when we've installed streamlit with pipenv, so the
# permissions during install are the same as the running process
def static_path():
    STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / 'static'
    if not STREAMLIT_STATIC_PATH.is_dir():
        STREAMLIT_STATIC_PATH.mkdir()
    return STREAMLIT_STATIC_PATH
# We create a downloads directory within the streamlit static asset directory
# and we write output files to it
def downloads_path():
    DOWNLOADS_PATH = (static_path() / "downloads")
    if not DOWNLOADS_PATH.is_dir():
        DOWNLOADS_PATH.mkdir()
    return DOWNLOADS_PATH

def pick_winner_selectbox(game_name, team0, team1, i=-1, index=0):
    selectbox_text = 'Please select the winner of ' + game_name + ':'
    other = 'Other'
    if i > -1:
        other = 'Other-' + str(i)
    game_winner = st.selectbox(selectbox_text, [team0, team1, other], index=index)
    print(game_winner)
    return game_winner

def optional_winner_selectbox(game_name, game_type, option_list, i=-1, index=0):
    selectbox_text = 'Please select the winner of ' + game_name + ' (' + game_type + '):'
    game_winner = st.selectbox(selectbox_text, option_list, index=index, key='optional_winner_selectbox' + str(i))
    print(game_winner)
    return game_winner