# MQTT Map Visualization

## How to Run
1. clone the repository to your computer, or download via zip file:  `git clone https://github.com/savardnm/2002-Field-Visualization.git`
2. open folder in vscode or via command prompt
3. run mapVis.py script using python3 `python3 ./mapVis.py`  [IF RUN FAILS, see 'Required Python Libraries' Section for more details]
4. [optional] when running the file, you may specify the grisize to use with the --gridsize flag `python3 ./mapVis.py --gridsize [size]`
5. log into your mqtt account in the terminal
6. publish data to the mqtt server under the topic '<username>/(x,y)'
   * username is your team in the format team#
   * x/y are integer from 0 to gridsize (default 0-14)
   * data should be a 0 for a white square and 1 for a black square

## Required Python Libraries
This Program runs on python 3 with the following libraries (installation instructions below):
- tkinter
- numpy
- argparse
- paho-mqtt
- copy
- ast

For Installation, View the following Guides:

[Installing Python](https://www.python.org/downloads/)
[Installing pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) (To download additional libraries above)
[Running Python via VScode](https://code.visualstudio.com/docs/languages/python)

To download libraries
1. [Install pip](https://packaging.python.org/en/latest/tutorials/installing-packages/)
2. in command line run the following commands:
   * `pip install tkinter`
   * `pip install numpy`
   * `pip install argparse`
   * `pip install paho-mqtt`
