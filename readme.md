###Overview:###
This is a powershell python script that will prepare the mobile texting site Excel sheet for Castlight.

###Requirements:###
Setting up the python environment is a basic IT task, but it should not be attempted by a non-tech user.
Python > 3.7,
pip or conda to install pandas library,
pandas library, ```pip install pandas```
You will also need administrative access to set the proxy in powershell, and you will need to enable execution of Python scripts in PowerShell.


### User Notes ###
This script has been written for Python 3.7 and 3.8. Place the latest CSV into the input folder. To execute the script, use PowerShell to navigate to the directory and type ```python conversion_script_3_8.py```. If python is executing the wrong version (2.7) you can use ```python3``` to specify the correct python version. Ask your IT department how to execute python scripts in PowerShell if you need help. 

The program will search for the latest XLSX file and will attempt to parse it. If you get an error, it is probably because there is a typo in the city names, a value is missing, or the date is in the wrong column. To fix the date in the wrong column, you can either move the date in the XLSX, or you can modify the source code.
The line that modifies the column to take the date from is here:
[this_date = pd.read_excel(latest_file, nrows=1, header=None)[4]](https://github.com/NYCMayorOps/mobile-vaccine-centers-xform/blob/9b720260e33721cafab5b49eeb4f86979f6e79f8/conversion_script_3_8.py#L118) . The column is 0 indexed, so column E is 4.


