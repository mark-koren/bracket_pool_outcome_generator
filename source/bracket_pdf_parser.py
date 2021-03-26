import pdb
import numpy as np
from scipy import spatial
from pathlib import Path
import csv
import pickle
from string import digits

from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import PDFPageAggregator

from source.utils import generate_round_array

winner_locations_CBS = {
    0 :[212, 428],
    1 :[212, 309],
    2 :[212, 193],
    3 :[212, 74 ],
    4 :[580, 428],
    5 :[580, 309],
    6 :[580, 193],
    7 :[580, 74 ],
    8 :[276, 371],
    9 :[276, 132],
    10:[516, 371],
    11:[516, 132],
    12:[238, 238],
    13:[556, 238],
    14:[374, 225],
}

winner_locations_ESPN = {
    0 :[197, 648],
    1 :[197, 531],
    2 :[197, 399],
    3 :[197, 282],
    4 :[420, 648],
    5 :[420, 531],
    6 :[420, 399],
    7 :[420, 282],
    8 :[249, 590],
    9 :[249, 341],
    10:[368, 590],
    11:[368, 341],
    12:[207, 459],
    13:[409, 459],
    14:[282, 482],
}

x0_or_x1 = {
    'x0':[0,1,2,3,8,9,12,14],
    'x1':[4,5,6,7,10,11,13],
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

substring_list = ['national','championship','indianapolis','april','west','east','midwest','south','predicted','winning','score','losing','presented']
def append_lt_obj_CBS(lt_obj):
    if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
        if lt_obj.x0 > 200 and lt_obj.x1 < 600 and lt_obj.y0 < 480:
            lt_string = lt_obj.get_text().strip().lower()
            if not any(substring in lt_string for substring in substring_list):
                return True

    return False

def append_lt_obj_ESPN(lt_obj):
    if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
        if lt_obj.x0 > 150 and lt_obj.x1 < 450 and lt_obj.y0 < 725:
            lt_string = lt_obj.get_text().strip().lower()
            lt_string = lt_string.translate(lt_string.maketrans('', '', digits))
            if lt_string and not any(substring in lt_string for substring in substring_list):
                return True

    return False

def get_winner_i_CBS(i, lt_objs, tree_dict):
    winner = lt_objs[tree_dict[i].query(winner_locations_CBS[i])[1]]
    winner_text = winner.get_text().strip().lower()
    return winner_text

def get_winner_i_ESPN(i, lt_objs, tree_dict):
    # pdb.set_trace()
    winner = lt_objs[tree_dict[i].query(winner_locations_ESPN[i])[1]]
    winner_text = winner.get_text().strip().lower()
    winner_text = winner_text.translate(winner_text.maketrans('', '', digits))
    winner_text = winner_text.replace('…','')
    winner_text = winner_text.replace('your', '')
    winner_text = winner_text.replace('pick', '')
    return winner_text.strip()

def get_bracket_dict(file_path, pool_type='CBS'):
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        # Set parameters for analysis.
        laparams = LAParams()
        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = device.get_result()
            lt_objs = []
            for lt_obj in layout:
                if pool_type=='CBS' and append_lt_obj_CBS(lt_obj):
                    lt_objs.append(lt_obj)
                elif pool_type=='ESPN' and append_lt_obj_ESPN(lt_obj):
                    print(lt_obj)
                    lt_objs.append(lt_obj)

        lt_obj_coords = np.zeros((len(lt_objs), 5))
        for obj_ix, lt_obj in enumerate(lt_objs):
            lt_obj_coords[obj_ix, 0] = lt_obj.x0
            lt_obj_coords[obj_ix, 1] = lt_obj.x1
            lt_obj_coords[obj_ix, 2] = lt_obj.y0
            lt_obj_coords[obj_ix, 3] = lt_obj.y1
            lt_obj_coords[obj_ix, 4] = obj_ix
        # print(lt_obj_coords)
        # sorted_array = lt_obj_coords[np.argsort(lt_obj_coords[:, 2])]
        # print(sorted_array)
        
        x0_tree = spatial.KDTree(lt_obj_coords[:,[0,2]])
        x1_tree = spatial.KDTree(lt_obj_coords[:,[1,2]])
        tree_dict = {}
        for idx in x0_or_x1['x0']:
            tree_dict[idx] = x0_tree

        for idx in x0_or_x1['x1']:
            tree_dict[idx] = x1_tree

        winner_dict = {}
        for i in range(15):
            if pool_type == 'CBS':
                winner_dict[i] = get_winner_i_CBS(i, lt_objs, tree_dict)
            elif pool_type == 'ESPN':
                winner_dict[i] = get_winner_i_ESPN(i, lt_objs, tree_dict)

        return winner_dict

def get_bracket_array(bracket_dict):
    bracket_array = np.zeros((16,4))
    round_array = generate_round_array(16)
    for i in range(15):
        # pdb.set_trace()
        winning_team = bracket_dict[i]
        if winning_team in team_id_dict:
            winning_team_idx = team_id_dict[winning_team]
            bracket_array[winning_team_idx, round_array[i]] = 1

    # return bracket_array.astype(int)
    return bracket_array.reshape((1,-1)).astype(int)

def generate_bracket_data_from_directory(dir_path):
        dirpath = Path(dir_path)
        assert (dirpath.is_dir())

        bracket_matrix = np.array([], dtype=np.int64).reshape(0,64)
        current_score_array = np.array([], dtype=np.int64).reshape(0,1)
        score_dict = get_score_dict_from_directory(dir_path)
        bracket_list = []

        pdf_files = dirpath.glob('*.pdf')
        for bracket_idx, pdf_file in enumerate(pdf_files):
            try:
                bracket_dict = get_bracket_dict(pdf_file)
                bracket_name = pdf_file.stem
                if bracket_name == 'sue_koren':
                    bracket_dict[14] = 'gonzaga'
                bracket_array = get_bracket_array(bracket_dict)

                bracket_info = {'name': bracket_name,
                                'idx': bracket_idx,
                                'current_score': score_dict[bracket_name],
                                'bracket_array':  bracket_array}
                bracket_list.append(bracket_info
                                    )
                bracket_matrix = np.vstack([bracket_matrix, bracket_array])
                current_score_array = np.vstack([current_score_array, np.array(score_dict[bracket_name])])


            except:
                print('Failed to create bracket for ', pdf_file.name)
                pdb.set_trace()
                continue

        return bracket_list, bracket_matrix, current_score_array

def create_empty_score_csv_from_directory(dir_path):
    dirpath = Path(dir_path)
    assert (dirpath.is_dir())
    csv_file = dirpath / 'current_scores.csv'
    with csv_file.open("w", encoding="utf-8") as file:
        csvWriter = csv.writer(file)
        pdf_files = dirpath.glob('*.pdf')
        for bracket_idx, pdf_file in enumerate(pdf_files):
            bracket_name = pdf_file.stem
            placeholder_row = [bracket_name, 0]
            csvWriter.writerow(placeholder_row)

    return csv_file

def get_score_dict_from_csv(csv_file):
    score_dict = {}
    with csv_file.open("r", encoding="utf-8") as file:
        csvReader = csv.reader(file)

        for row in csvReader:
            score_dict[row[0]] = int(row[1])

    return score_dict

def get_score_dict_from_directory(dir_path):
    dirpath = Path(dir_path)
    assert (dirpath.is_dir())
    csv_file = dirpath / 'current_scores.csv'
    return get_score_dict_from_csv(csv_file)

def save_bracket_data(bracket_dir_path, bracket_list, bracket_matrix, current_score_array):
    dirpath = Path(bracket_dir_path)
    assert (dirpath.is_dir())

    bracket_list_filename = 'bracket_list.pkl'
    bracket_list_path = dirpath / bracket_list_filename
    with bracket_list_path.open('wb') as file:
        pickle.dump(bracket_list, file)

    bracket_matrix_filename = 'bracket_matrix.pkl'
    bracket_matrix_path = dirpath / bracket_matrix_filename
    with bracket_matrix_path.open('wb') as file:
        pickle.dump(bracket_matrix, file)

    current_score_array_filename = 'current_score_array.pkl'
    current_score_array_path = dirpath / current_score_array_filename
    with current_score_array_path.open('wb') as file:
        pickle.dump(current_score_array, file)

def load_bracket_data(bracket_dir_path):
    dirpath = Path(bracket_dir_path)
    print(dirpath)
    print(dirpath.is_dir())
    assert (dirpath.is_dir())

    bracket_list_filename = 'bracket_list.pkl'
    bracket_list_path = dirpath / bracket_list_filename
    print(bracket_list_path)
    print(bracket_list_path.is_file())
    assert bracket_list_path.is_file()

    with bracket_list_path.open('rb') as file:
        bracket_list = pickle.load(file)

    bracket_matrix_filename = 'bracket_matrix.pkl'
    bracket_matrix_path = dirpath / bracket_matrix_filename
    print(bracket_matrix_path)
    print(bracket_matrix_path.is_file())
    assert bracket_matrix_path.is_file()

    with bracket_matrix_path.open('rb') as file:
        bracket_matrix = pickle.load(file)

    current_score_array_filename = 'current_score_array.pkl'
    current_score_array_path = dirpath / current_score_array_filename
    print(current_score_array_path)
    print(current_score_array_path.is_file())
    assert current_score_array_path.is_file()

    with current_score_array_path.open('rb') as file:
        current_score_array = pickle.load(file)

    return bracket_list, bracket_matrix, current_score_array

def load_or_generate_bracket_data(bracket_dir_path, force_generation=False):
    try:
        print(force_generation)
        assert not force_generation
        bracket_list, bracket_matrix, current_score_array = load_bracket_data(bracket_dir_path)
    except:
        print('Failed to load bracket pool data -- generating and saving new bracket pool data')
        bracket_list, bracket_matrix, current_score_array = generate_bracket_data_from_directory(bracket_dir_path)
        save_bracket_data(bracket_dir_path, bracket_list, bracket_matrix, current_score_array)
    finally:
        return bracket_list, bracket_matrix, current_score_array



if __name__ == '__main__':
    # print(convert_pdf_to_string('./mark_koren.pdf'))
    # mark_koren_dict = get_bracket_dict('./mark_koren.pdf')
    # print(mark_koren_dict)
    # mark_koren_array = get_bracket_array(mark_koren_dict)
    # print(mark_koren_array)
    #
    # # print(convert_pdf_to_string('./matt_jones.pdf'))
    # matt_jones_dict = get_bracket_dict('./matt_jones.pdf')
    # print(matt_jones_dict)
    # matt_jones_array = get_bracket_array(matt_jones_dict)
    # print(matt_jones_array)

    # create_empty_score_csv_from_directory('./aj_ellis_co')
    # # bracket_list, bracket_matrix = get_brackets_from_directory('./aj_ellis_co')
    # bracket_list, bracket_matrix, current_score_array = load_or_generate_bracket_data('./aj_ellis_co', force_generation=True)
    # print(bracket_list)
    # print(bracket_matrix)
    # print(current_score_array)

    print(get_bracket_dict('../hot_sauce/ross_weber.pdf', pool_type='ESPN'))
    print(get_bracket_dict('../hot_sauce/ross_weber_2.pdf', pool_type='ESPN'))
    print(get_bracket_dict('../hot_sauce/ross_weber_3.pdf', pool_type='ESPN'))