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

    st.subheader('Instructions:')
    st.write('''
    This tool is meant to show you how many ways you (and everyone else) in your bracket pool could still win.
    The process is straightforward.
    Step 1, which you are doing now, is to read the instructions.
    In step 2, you will enter the data on all of the brackets in your bracket pool.
    ''')

    st.subheader('Data Generation:')
    st.write('''
    When you finished reading these instructions, you can proceed to page 2, Generation using the dropdown menu in the sidebar.
    There are two ways to generate the bracket pool data.
    
    CBS or ESPN Pools:
    If your pool is run by  CBS Sports or ESPN, I wrote a script to automatically process pdfs of everyones bracket.
    Download a pdf copy of each bracket from your pool into a folder.
    Highlight all the brackets at once, right click, and choose 'compress' or 'send to zip' etc.
    DO NOT ZIP THE FOLDER ITSELF - this creates an extra layer of folder upon unzipping, which will break the auto-process script.
    You can then upload the zip on page 2.
    
    All Pools:
    You will have to enter each bracket individually.
    Select 'Add a Bracket' from the drop down menu.
    Enter in the correct data, including the current score.
    You will see a preview. If the preview is correct, click 'Add to Table'.
    
    
    For both pools, you will need to get the current score for each bracket as well. There are two ways to do this:
    
    CBS or ESPN Pools:
    Once all the brackets are generated, select 'Change Current Scores' from the dropdown menu.
    You will see a link to download an empty 'current_scores.csv'.
    Download this and open it on your computer.
    Enter in the correct scores for everyone and save it (as a .csv still!)
    Then, upload it to the 'updated current_scores.csv' file upload box.
    The scores should process automatically.
    
    All Pools:
    You can also use the data editor to change each bracket's score.
    Select 'Edit a Bracket' from the dropdown menu.
    Select the bracket by name, and then you can then change the score.
    Click 'Update Bracket' to save the changes.
    
    
    Inspect the data in the table viewer.
    If any of the data is incorrect, you can change it with the data editor.    
    Select 'Edit a Bracket' from the dropdown menu.
    Select the bracket by name, and then you can then change any values.
    Click 'Update Bracket' to save the changes.
    You can also delete rows, or clear all the data.
    
    Once the data is correct, click 'Generate Bracket Pool Data'
    This generates a 'bracket_pool_data.pkl' file.
    Click on the link to download it.
    Any time you want to generate outcomes for that bracket pool, upload that pkl file to the 'Upload bracket_pool_data.pkl' upload box on the sidebar.
    
    ''')

    st.subheader('Pool Outcome Viewer:')
    st.write('''
    When you have uploaded a bracket_pool_data.pkl file, you can proceed to page 3, Pool Overview using the dropdown menu in the sidebar.
    The dropdown menu defaults to 'Inspect Data'
    In this mode, you will see a table with every bracket, as well as their chances to tie for or finish alone in 1st, 2nd, or 3rd/
    The number of possible cases as well as the percentages are shown.
    
    If you are interested in specific scenarios, choose 'Look at Scenarios' from the dropdown menu.
    You will see a list of games.
    You can select the winner of a game, and the tool will recalculate the outcomes and percentages based on the games having the specified results.
    To access later games, you must select the winner from earlier rounds.
    For example, if you want to see your win chances when (oh sorry, if) Alabama makes the final four, first select Alabama as the winner of the Sweet 16 game vs UCLA.
    Then a box will pop up for the Elite 8 game. Since you have not chosen a winner of Florida St. vs Michigan, it will say Alabama vs Other.
    Select Alabama as the winner of that Elite 8 game.
    The table will refresh, showing you everyone's number of paths to winning if Alabama makes the final four.
    Note that each game you set reduces the number of realizable outcomes by a factor of two, so your total paths to victory may decrease even as your percentage of total paths increases.
    
    ''')

    st.subheader('Individual Bracket Viewer:')
    st.write('''
    To learn about an individual bracket, you can proceed to page 4, Individual Brackets using the dropdown menu in the sidebar.
    Select the name of the bracket you are interested in.
    The dropdown menu defaults to 'Inspect Data'
    In this mode, you will see the brackets number of paths (and percentages) to victory depending on who wins each of the sweet 16 games.
    This can give you an idea of who to root for, or if a game is a must-have.
    
     If you are interested in specific scenarios, choose 'Look at Scenarios' from the dropdown menu.
    You will see a list of games.
    This works the same way as in the 'Pool Overview' section.
    As you choose winners of different games, the outcomes for each of the sweet 16 games will update.
    ''')

    st.subheader('Final thoughts')
    st.write('''
    If you have any issues, feel free to reach out to me.
    I will do my best to help you get it working.
    If you enjoy playing around with this tool, you can donate to my ~~keg~~ uhhhh coffee fund with the Ko-Fi link above.
    I am in my last 3 months of grad school, lord knows I could use the.... caffeine.
    ''')