import pdb
import numpy as np
from scipy import spatial

from io import StringIO
from string import digits

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import PDFPageAggregator

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

team_id_dict = {
    'gonzaga':0,
    'creighton':1,
    'usc':2,
    'oregon':3,
    'michigan':4,
    'florida st.':5,
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

def get_pdf_layout_analysis(file_path):
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
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    if lt_obj.x0 > 150 and lt_obj.x1 < 450 and lt_obj.y0 < 725:
                        # print(lt_obj)
                        # lt_objs.append(lt_obj)
                        # lt_string = lt_obj.get_text().strip().lower()
                        # if not any(substring in lt_string for substring in substring_list):
                        lt_string = lt_obj.get_text().strip().lower()
                        lt_string = lt_string.translate(lt_string.maketrans('','',digits))
                        print(lt_string)
                        if lt_string and not any(substring in lt_string for substring in substring_list):
                            lt_objs.append(lt_obj)
                            print(lt_obj)

        lt_obj_coords = np.zeros((len(lt_objs), 5))
        for obj_ix, lt_obj in enumerate(lt_objs):
            lt_obj_coords[obj_ix, 0] = lt_obj.x0
            lt_obj_coords[obj_ix, 1] = lt_obj.x1
            lt_obj_coords[obj_ix, 2] = lt_obj.y0
            lt_obj_coords[obj_ix, 3] = lt_obj.y1
            lt_obj_coords[obj_ix, 4] = obj_ix
        print(lt_obj_coords)
        sorted_array = lt_obj_coords[np.argsort(lt_obj_coords[:, 2])]
        print(sorted_array)
        
        tree = spatial.KDTree(lt_obj_coords[:,[0,2]])
        for i in range(15):
            print(lt_objs[tree.query(winner_locations_ESPN[i])[1]])
        pdb.set_trace()



def convert_pdf_to_string(file_path):

	output_string = StringIO()
	with open(file_path, 'rb') as in_file:
	    parser = PDFParser(in_file)
	    doc = PDFDocument(parser)
	    rsrcmgr = PDFResourceManager()
	    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	    interpreter = PDFPageInterpreter(rsrcmgr, device)
	    for page in PDFPage.create_pages(doc):
	        interpreter.process_page(page)

	return(output_string.getvalue())

                
def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()
    
    title = None
    pagenum = None
    
    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1

            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())
        
    return title, pagenum

if __name__ == '__main__':
    # print(convert_pdf_to_string('./mark_koren.pdf'))
    # get_pdf_layout_analysis('./mark_koren.pdf')

    # print(convert_pdf_to_string('./matt_jones.pdf'))
    # get_pdf_layout_analysis('./matt_jones.pdf')

    get_pdf_layout_analysis('../hot_sauce/ross_weber.pdf')
    get_pdf_layout_analysis('../hot_sauce/ross_weber_2.pdf')
    get_pdf_layout_analysis('../hot_sauce/ross_weber_3.pdf')