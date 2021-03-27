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


from pages.utils import page_header, downloads_path, upload_folder, save_uploadedfile, markdown_file_downloader, static_path

def introduction():
    page_header()