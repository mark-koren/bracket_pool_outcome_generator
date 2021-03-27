import os
import zipfile
from pathlib import Path
import streamlit as st
import pandas as pd
import shutil
import pickle

from pages.introduction import introduction
from pages.generate import generate
from pages.pool_overview import pool_overview
from pages.individual_brackets import individual_brackets

from pages.utils import static_path, downloads_path, upload_folder

possible_files_names = [
    'bracket_list.pkl',
    'bracket_matrix.pkl',
    'bracket_pool_data.pkl',
    'current_score_array.pkl',
    'current_scores.csv',
    'df_bracket_pool.pkl',
    'outcome_matrix_16.pkl',
    'empty_current_scores.csv',
]

@st.cache
def unpack_bracket_pool_data(uploaded_bracket_pool_data, force_generation=False):
    bracket_pool_data_dict = pickle.load(uploaded_bracket_pool_data)

    bracket_list = bracket_pool_data_dict['bracket_list']
    bracket_matrix = bracket_pool_data_dict['bracket_matrix']
    current_score_array = bracket_pool_data_dict['current_score_array']
    df_bracket_pool = bracket_pool_data_dict['df_bracket_pool']

    return bracket_list, bracket_matrix, current_score_array, df_bracket_pool

bracket_pool_data_loaded = False
bracket_list = None
bracket_matrix = None
current_score_array = None
df_bracket_pool = None

page = st.sidebar.selectbox('Step:', ('1. Introduction', '2. Generate', '3. Pool Overview', '4. Individual Brackets'))
uploaded_bracket_pool_data = st.sidebar.file_uploader('Upload bracket_pool_data.pkl:')
if uploaded_bracket_pool_data is not None:
    bracket_list, bracket_matrix, current_score_array, df_bracket_pool = unpack_bracket_pool_data(
        uploaded_bracket_pool_data)

if st.sidebar.button('CLEAR ALL DATA (WARNING - CAN NOT BE UNDONE!)'):
    for filename in possible_files_names:
        temp_path = static_path() / filename
        print(temp_path)
        if temp_path.is_file():
            temp_path.unlink()
        temp_path = downloads_path() / filename
        print(temp_path)
        if temp_path.is_file():
            temp_path.unlink()

if page == '1. Introduction':
    introduction()
elif page == '2. Generate':
    generate()
elif page == '3. Pool Overview':
    pool_overview(bracket_list, bracket_matrix, current_score_array, df_bracket_pool)
elif page == '4. Individual Brackets':
    individual_brackets(bracket_list, bracket_matrix, current_score_array, df_bracket_pool)
