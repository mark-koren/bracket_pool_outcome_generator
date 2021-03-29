# bracket_pool_outcome_generator
Bracket pool outcome generator

# NEW! THE APP IS LIVE AT share.streamlit.io

You no longer need to install anything! You can use the app at:
https://share.streamlit.io/mark-koren/bracket_pool_outcome_generator/main/main.py

# Installation Instructions (NO LONGER NECESSARY)
If you still want to install and launch locally:
## Windows:

1. Install [Python 3](https://www.python.org/downloads/), then open up [command line](https://www.computerhope.com/issues/chusedos.htm).

2. Download the git repository. There are two ways to do this:
    1. Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Then clone the repository:
    `git clone https://github.com/mark-koren/bracket_pool_outcome_generator.git`
    2. Download the zip folder (green Code button in upper right). Naviagte to the folder containing the zip folder and unzip.
    `cd Downloads/`
    `cd bracket_pool_outcome_generator-main/`

3. Naviagte to the folder you just downloaded the repository to.
`cd bracket_pool_outcome_generator-main/`

4. Install the python required python dependencies.
`py -m pip install -r requirements.txt`

5. Launch the app
`py -m streamlit run main.py`

6. The app should open in your internet browser automatically. If it does not, copy the `Local URL` address printed from the previous command and paste it in the browser, then press enter. The address is generally `http://localhost:8501

### Screenshots:

Naviagte to the folder you just downloaded the repository to:
![alt text](https://imgur.com/bA6fqJE.png)

Install the python  requirements:
![alt text](https://imgur.com/pBRXTPv.png)

Run the app, from the command line:
![alt text](https://imgur.com/B8LJUmC.png)

## Linux/Mac:

1. Install [Python 3](https://www.python.org/downloads/), then open up a terminal ([Mac](https://www.businessinsider.com/how-to-open-terminal-on-mac), [Linux](https://www.howtogeek.com/686955/how-to-launch-a-terminal-window-on-ubuntu-linux/#:~:text=Run%20a%20Command%20to%20Open,to%20launch%20a%20terminal%20window.&text=You%20can%20run%20many%20other,Alt%2BF2%20window%2C%20too.)).

2. Download the git repository. There are two ways to do this:
    1. Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Then clone the repository:
    `git clone https://github.com/mark-koren/bracket_pool_outcome_generator.git`
    2. Download the zip folder (green Code button in upper right). Naviagte to the folder containing the zip folder and unzip.
    `cd Downloads/`
    `cd bracket_pool_outcome_generator-main/`

3. Naviagteto the folder you just downloaded the repository to.
`cd bracket_pool_outcome_generator-main/`

4. Install the python required python dependencies.
`python3 -m pip install -r requirements.txt`

5. Launch the app
`python3 -m streamlit run main.py`

6. The app should open in your internet browser automatically. If it does not, copy the `Local URL` address printed from the previous command and paste it in the browser, then press enter. The address is generally `http://localhost:8501`

### Screenshots:
Naviagte to the folder you just downloaded the repository to:
![cd to bracket](https://imgur.com/BJz1lkD.png)

Install the python  requirements:
![pip install](https://imgur.com/oVtvLEo.png)

Run the app, from the command line:
![run](https://imgur.com/k8hRNJ9.png)

# Troubleshooting

Windows in particular may give you a couple issues.
During the pip installation, the installation of a package might fail.
If scipy failst to install, you may need to install the [Microsoft C++ build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
If it still doesn't work, or if any other package fails to install, you can try to install that package manually:
`py -m pip install scipy`
Once a package is installed manually, open `requirements.txt.` and delete the line that installs that pacakge.
Then rerun the pip installation.


