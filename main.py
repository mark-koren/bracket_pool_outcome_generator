import os
import zipfile
from pathlib import Path
import streamlit as st
import pandas as pd
import shutil
import pickle

from source.bracket_pdf_parser import load_or_generate_bracket_data, create_empty_score_csv_from_directory
from source.bracket_outcomes import load_or_generate_outcome_matrix
from source.bracket_pool_analyzer import load_or_generate_bracket_pool_scores, print_money_chances

UPLOAD_FOLDER = Path.cwd().joinpath('data')

# HACK This only works when we've installed streamlit with pipenv, so the
# permissions during install are the same as the running process
STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / 'static'
# We create a downloads directory within the streamlit static asset directory
# and we write output files to it
DOWNLOADS_PATH = (STREAMLIT_STATIC_PATH / "downloads")
if not DOWNLOADS_PATH.is_dir():
    DOWNLOADS_PATH.mkdir()

def save_uploadedfile(uploadedfile, save_destination):
    with save_destination.open('wb') as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{filename} to {save_destination}".format(filename=uploadedfile.name, save_destination=save_destination))

def markdown_file_downloader(text, link_text, download_path):
    markdown_string = text.format(link_text=link_text, download_path=download_path)
    print(markdown_string)
    st.markdown(markdown_string)


def file_downloader():
    st.markdown("Download from [test](downloads/mydata.csv) blahg")
    mydataframe = pd.DataFrame.from_dict({'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']})
    mydataframe.to_csv(str(DOWNLOADS_PATH / "mydata.csv"), index=False)

def unzip_pool_pdfs(uploaded_zip_file, force_generation):
    if uploaded_zip_file is not None:
        file_details = {"FileName": uploaded_zip_file.name, "FileType": uploaded_zip_file.type}
        print(file_details)
        print(uploaded_zip_file)

        zip_filepath = UPLOAD_FOLDER.joinpath(uploaded_zip_file.name)
        if zip_filepath.exists() and force_generation:
            zip_filepath.unlink()
        print(zip_filepath)
        dir_filepath = zip_filepath.with_suffix('')
        if dir_filepath.exists() and force_generation:
            shutil.rmtree(dir_filepath)
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

        save_uploadedfile(uploaded_zip_file,zip_filepath)
        zip_ref = zipfile.ZipFile(zip_filepath, 'r')
        zip_ref.extractall(pdfs_filepath)
        zip_ref.close()

        # zip_filepath.unlink()
        return pdfs_filepath, dir_filepath
    return None, None

def create_data_folder(uploaded_bracket_list, uploaded_bracket_matrix, uploaded_current_score_array, dir_filepath, force_generation=False):
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
def get_outcome_matrix():
    outcome_matrix = load_or_generate_outcome_matrix(STREAMLIT_STATIC_PATH, num_teams=16, force_generation=False)
    return outcome_matrix

st.title('So you\'re saying there\'s a chance!?!')
st.header('Bracket pool outcome generator')
st.subheader('By: Mark Koren')
# st.markdown('[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L4L242M4H)')


st.header('1. Generate Bracket Pool Data')
st.text('Already generated the data? Go to step 2.')


st.subheader('1.1 Upload Bracket Pool PDFs')
st.text('Select the organization that hosts your bracket pool.')
pool_type = st.radio('Bracket Pool Type:', ('CBS', 'ESPN', 'OTHER'))

generated_pdf_dir = False
pdfs_filepath = None
dir_filepath = None
force_generation = False
if pool_type == 'CBS' or pool_type == 'ESPN':

    st.write('If you are part of a CBS Sports or ESPN bracket pool, I can generate everything automatically. Upload a zip folder containing a pdf of every persons bracket:')
    force_generation_radio = st.radio('Force Generation?:', ('Yes', 'No'), index=1)
    if force_generation_radio == 'Yes':
        force_generation = True
    uploaded_pdfs = st.file_uploader('Upload zipped folder of bracket pdfs:')
    pdfs_filepath, dir_filepath = unzip_pool_pdfs(uploaded_pdfs, force_generation)
    if pdfs_filepath is not None:
        try:
            csv_file = create_empty_score_csv_from_directory(pdfs_filepath)
            print(csv_file)
            # downloadable_csv_file = DOWNLOADS_PATH / csv_file.name
            # if not downloadable_csv_file.is_file():
            #     csv_file.rename()

            csv_file.replace(DOWNLOADS_PATH / csv_file.name)
            print(csv_file)
            # download_file = Path(DOWNLOADS_PATH).joinpath(csv_file.name)
            # if download_file.exists():
            #     download_file.unlink()
            # print(download_file)
            # download_file.symlink_to(csv_file)
            # print(download_file)
            download_path = 'downloads/' + csv_file.name
            download_text = 'Download the empty [{link_text}]({download_path}).'
            markdown_file_downloader(text=download_text, link_text='current_scores.csv', download_path=download_path)
            # st.markdown("Download the [downloads/mydata.csv](downloads/mydata.csv) blahg")
            generated_pdf_dir = True
        except:
            st.error('Sorry, something went wrong and I couldn\'t generate the empty score csv. Maybe double check your input and try again?')
            st.stop()

else:
    st.text('Sorry, I only support CBS and ESPN for now, but I am working to expand on this ASAP!')

csv_filepath = None
if generated_pdf_dir and pdfs_filepath is not None and dir_filepath is not None:
    st.subheader('1.2 Upload Current Score csv')
    st.text('Upload a csv that designates the current score for each bracket.')
    uploaded_score_csv = st.file_uploader('Upload current_scores.csv:')
    csv_filepath = get_score_csv(uploaded_score_csv, pdfs_filepath, force_generation=force_generation)
    if csv_filepath is not None:
        # TODO: Add progress bar
        try:
            bracket_list, bracket_matrix, current_score_array = load_or_generate_bracket_data(pdfs_filepath, pool_type=pool_type, force_generation=force_generation)
            print(bracket_list)

            bracket_list_path = pdfs_filepath.joinpath('bracket_list.pkl')
            download_bracket_list_path = DOWNLOADS_PATH  / bracket_list_path.name
            shutil.copy(str(bracket_list_path), str(download_bracket_list_path))

            download_path = 'downloads/' + bracket_list_path.name
            download_text = 'Download the [{link_text}]({download_path}).'
            markdown_file_downloader(text=download_text, link_text='bracket list', download_path=download_path)

            bracket_matrix_path = pdfs_filepath.joinpath('bracket_matrix.pkl')
            download_bracket_matrix_path = DOWNLOADS_PATH / bracket_matrix_path.name
            shutil.copy(str(bracket_matrix_path), str(download_bracket_matrix_path))

            download_path = 'downloads/' + bracket_matrix_path.name
            download_text = 'Download the [{link_text}]({download_path}).'
            markdown_file_downloader(text=download_text, link_text='bracket matrix', download_path=download_path)

            current_score_array_path = pdfs_filepath.joinpath('current_score_array.pkl')
            download_current_score_array_path = DOWNLOADS_PATH / current_score_array_path.name
            shutil.copy(str(current_score_array_path), str(download_current_score_array_path))

            download_path = 'downloads/' + current_score_array_path.name
            download_text = 'Download the [{link_text}]({download_path}).'
            markdown_file_downloader(text=download_text, link_text='current score array', download_path=download_path)

            # shutil.rmtree(pdfs_filepath)
        except:
            st.error('Sorry, something went wrong and I couldn\'t generate the empty score csv. Maybe double check your input and try again?')
            st.stop()


st.header('2.0 Upload Bracket Pool Data')
st.text('If you have already generated your bracket pool data, upload it now: ')

uploaded_bracket_list = st.file_uploader('Upload bracket_list.pkl:')
uploaded_bracket_matrix = st.file_uploader('Upload bracket_matrix.pkl:')
uploaded_current_score_array = st.file_uploader('Upload current_score_array.pkl:')

bracket_list_filepath, bracket_matrix_filepath, current_score_array_filepath = create_data_folder(uploaded_bracket_list, uploaded_bracket_matrix, uploaded_current_score_array, dir_filepath, force_generation=False)
if bracket_list_filepath is not None:
    with bracket_list_filepath.open('rb') as f:
        bracket_list = pickle.load(f)

    with bracket_matrix_filepath.open('rb') as f:
        bracket_matrix = pickle.load(f)

    with current_score_array_filepath.open('rb') as f:
        current_score_array = pickle.load(f)

if bracket_list is not None and bracket_matrix is not None and current_score_array is not None:
    st.header('3.0 Bracket Pool Results')

    outcome_matrix = get_outcome_matrix()
    bracket_pool_scores = load_or_generate_bracket_pool_scores(dir_filepath, bracket_matrix, outcome_matrix,
                                                               current_score_array, force_generation=False)
    df_money_chances = print_money_chances(bracket_list, bracket_pool_scores)
    st.dataframe(df_money_chances)