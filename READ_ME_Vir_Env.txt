Installing python3:
py -m pip --version
pip 9.0.1 from c:\python36\lib\site-packages (Python 3.6.1)

Upgrade pip:
py -m pip install --upgrade pip

Installing virtualenv:
Mac and Linux: 
    python3 -m pip install --user virtualenv
Windows: 
    py -m pip install --user virtualenv

Creating the virtual environment:
Mac and Linux:
    python3 -m venv SrDesign 
Windows: 
    py -m venv SrDesign

Activating a virtual environment:
Mac and Linux: 
    source SrDesign/bin/activate
Windows:
    .\SrDesign\Scripts\activate

Leaving the virtual environment:
    deactivate 

Using requirements files (have to be inside the virtual environment):
    pip install -r requirements.txt
    (The requirements.txt file will be on github)







