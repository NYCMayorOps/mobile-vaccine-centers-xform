### User Notes ###
Execute this the executable conversion_script_3_7.exe. Make sure that your input XLSX sheet is named "vax_testing_input.xlsx" and placed in the same folder as the executable (exe) file. 

### Developer notes ###
to compile:
pyinstaller --add-data 'src/vax_testing_input.xlsx;.' --onefile conversion_script_3_7.py
pyinstaller conversion_script_3_7.spec