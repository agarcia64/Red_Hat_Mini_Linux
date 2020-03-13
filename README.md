# Red_Hat_Mini_Linux
Simulate a basic version of the grep, ls and df commands found in linux. 

To use
1. Run "python LinuxMiniUntils.py" 
2. Enter desired command in the shell, using the following syntax
  2.1. "./mini-command -option(s) PATTERN ["\\FILE\\" or "\\PATH\\"]"
  
If commands are incorrectly entered, errors will be thrown and the user will be asked to try again. Most error handling happens
during the parsing of user input. FILEs and PATHs must be full directories. 
