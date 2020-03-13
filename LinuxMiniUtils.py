##############################################################################
# Libraries
##############################################################################
import os
import re
import pathlib
import shutil

class MiniLinux():
	##############################################################################
	# Variables
	##############################################################################
	def __init__(self):
		# user command variables
		self.userInputString = ''		# the input string 
		self.commandString = ''			# the command the user wants to execute
		self.commandArgList = []			# the list of arguments for the command
		self.commandOptionsList = [] 	# the list of options for the command, if they exist
		self.commandRemainingArgs = [] 	# the list of arguments that are NOT options\
		self.commandPATHs = []			# the [PATTERN] arguments, if they exist
		self.commandFILEs = []     		# the [FILE] arguments, if they exist
		self.commandPATTERN = ''			# the [PATH] argument, if it exists

		# legal arguments
		self.LEGAL_COMMANDS = ['./mini-grep','./mini-ls','./mini-df']	# the three legal commands
		self.LEGAL_GREP_OPTIONS = ['-q']								# the legal grep options
		self.LEGAL_LS_OPTIONS = ['-r']									# the legal ls options
		self.LEGAL_DF_OPTIONS = ['-h']									# the legal df options

	##############################################################################
	# "mini-grep"
	# -----------
	#
	# Usage:
	#
	#     ./mini-grep [-q] -e PATTERN [FILE...]
	#
	# `mini-grep` goes through every argument in FILE and prints the whole
	# line in which PATTERN is found. By default `mini-grep` also outputs
	# the line number of each printed line.
	#
	# - PATTERN has to be a valid regex
	# - FILE can be zero or more arguments. If zero args are given,
	#   `mini-grep` will parse entries from the standard input.
	# - If given, the `-q` options only outputs lines but omits the matching
	#   line numbers.
	##############################################################################
	def q_option_output(self):
		if len(self.commandFILEs) == 0:
			# get the files from the current directory
			tempCurrentDir = pathlib.Path().absolute()

			# all files in the current directory
			tempCurrentDirFileList = os.listdir(tempCurrentDir)

			# search each file
			for file in tempCurrentDirFileList:
				for lineNum, lineString in enumerate(open(file)):
					for match in re.finditer(self.commandPATTERN, lineString):
						print('File:', file, ', Line Num:', lineNum+1)

		# else, search for PATTERN in each file
		else:
			for file in self.commandFILEs:
				for lineNum, lineString in enumerate(open(file)):
					for match in re.finditer(self.commandPATTERN, lineString):
						print('File:', file, ', Line Num:', lineNum+1)

	def mini_grep(self):

		# if q option is selected
		if '-q' in self.commandOptionsList:
			self.q_option_output()
		else: 
			# if FILEs is empty, search for PATTERN in files in the current directory
			if len(self.commandFILEs) == 0:
				# get the files from the current directory
				tempCurrentDir = pathlib.Path().absolute()

				# all files in the current directory
				tempCurrentDirFileList = os.listdir(tempCurrentDir)

				# search each file
				for file in tempCurrentDirFileList:
					for lineNum, lineString in enumerate(open(file)):
						for match in re.finditer(self.commandPATTERN, lineString):
							print('File:', file, ', Line Num:', lineNum+1, ', Line String:', lineString)

			# else, search for PATTERN in each file
			else:
				for file in self.commandFILEs:
					for lineNum, lineString in enumerate(open(file)):
						for match in re.finditer(self.commandPATTERN, lineString):
							print('File:', file, ', Line Num:', lineNum+1, ', Line String:', lineString)

	##############################################################################
	# "mini-ls"
	# ---------
	#
	# Usage
	#
	#     ./mini-ls [-r] [FILE...]
	#
	# `mini-ls` lists information about the paths given in FILE. The
	# information required are: Owner, Permission, Modified Time.
	#
	# - FILE can be zero or more arguments. If zero args are given,
	#   `mini-ls` will list information about the current directory.
	# - If given, the `-r` option will make `mini-ls` run recursively on any
	#   directory it comes across.
	##############################################################################
	def r_option_output(self, currentDir):
		# if the current dir is not same as parent
		if currentDir != pathlib.PurePath(currentDir).parent:
			# get the current directory
			tempCurrentDir = currentDir

			# get parent 
			tempCurrentDirParent = pathlib.PurePath(tempCurrentDir).parent

			# get info for each path in the dir
			for path in pathlib.Path(tempCurrentDirParent).iterdir():
				# retreive Owner, Permission, Modified Time
				st_mode, _, _, _, st_uid,st_gid, _, _, st_mtime, _ = os.stat(path) 

				# print the data to the user per path
				print('PATH:', path, 'st_mode:', st_mode, ', Owner id:', st_uid, ', Group id:', st_gid, ', Modified time:', st_mtime)

			# recurse
			self.r_option_output(tempCurrentDirParent)

		# end recursion
		else:
			return 

	def mini_ls(self):

		if '-r' in self.commandOptionsList:
			# if PATHs is empty, recurse from the current directory
			if len(self.commandPATHs) == 0:
				self.r_option_output(pathlib.Path().absolute())
			# else recurse thru each path
			else:
				for path in self.commandPATHs:
					print("")
					self.r_option_output(path)

		else:
			# if PATHs is empty, list owner, permission and modified time in the current path
			if len(self.commandPATHs) == 0:
				# get the current directory
				tempCurrentDir = pathlib.Path().absolute()

				# all files in the current directory
				tempCurrentDirFileList = os.listdir(tempCurrentDir)

				# get info for each path in the dir
				for path in tempCurrentDirFileList:
					# retreive Owner, Permission, Modified Time
					st_mode, _, _, _, st_uid,st_gid, _, _, st_mtime, _ = os.stat(path) 

					# print the data to the user per path
					print('PATH:', path, 'st_mode:', st_mode, ', Owner id:', st_uid, ', Group id:', st_gid, ', Modified time:', st_mtime)
			# return data for each path
			else:
				for path in self.commandPATHs:
					tempCurrentDir = path

					# get info for each path in the dir
					for path in pathlib.Path(tempCurrentDir).iterdir():
						# retreive Owner, Permission, Modified Time
						st_mode, _, _, _, st_uid,st_gid, _, _, st_mtime, _ = os.stat(path) 

						# print the data to the user per path
						print('PATH:', path, 'st_mode:', st_mode, ', Owner id:', st_uid, ', Group id:', st_gid, ', Modified time:', st_mtime)


	##############################################################################
	# "mini-df"
	# ---------
	#
	# Usage:
	#
	#     ./mini-df [-h] [PATH...]
	#
	# `mini-df` outputs the file system disk space usage of each entry in
	#  PATH. The information required is: Total Space, Free Space, Used
	#  Space. The result should be in Bytes.
	#
	# - PATH can be zero or more arguments. IF zero args are given,
	#   `mini-df` will list the disk space usage of the current directory.
	# - If given `-h` will output the result in human-readable format.
	##############################################################################
	def h_option_output(self, packed):
		total, used, free = packed
		print('total space:', total, 'bytes, used space:', used, 'bytes, free space:', free, 'bytes')

	def mini_df(self):
		# if PATHs is empty, list the disk space usage of the cur dir
		if len(self.commandPATHs) == 0:
			# get the current directory
			tempCurrentDir = pathlib.Path().absolute()

			# check the -h option
			if '-h' not in self.commandOptionsList:
				# total space in bytes, used space in bytes, free space in bytes
				total, used, free = shutil.disk_usage(tempCurrentDir)
				print(total, used, free)

			# elif the -h option is being used
			else:
				self.h_option_output(shutil.disk_usage(tempCurrentDir))
		# return the data for each PATH
		else:
			for path in self.commandPATHs:
				tempCurrentDir = path

				# check for the -h option
				if '-h' not in self.commandOptionsList:
					# total space in bytes, used space in bytes, free space in bytes
					total, used, free = shutil.disk_usage(tempCurrentDir)
					print(total, used, free)
				# elif the -h option is being used
				else:
					self.h_option_output(shutil.disk_usage(tempCurrentDir))

	##############################################################################
	# "intersection"
	# input:  2 lists
	# output: 1 list, the intersection of the 2 input lists
	##############################################################################
	def intersection(self, listx, listy):
		listxy = [x for x in listx if x in listy]
		return listxy

	##############################################################################
	# "complement"
	# input:  2 lists
	# output: 1 list, return everything in list x that is not in list y 
	##############################################################################
	def complement(self, listx, listy):
		listxy = [x for x in listx if x not in listy]
		return listxy

	##############################################################################
	# "union"
	# input:  2 lists
	# output: 1 list, return everything in both lists, no duplicates
	##############################################################################
	def union(self, listx, listy):
		listxy = list(set(listx) | set(listy))
		return listxy

	##############################################################################
	# "reset_vars"
	# reset all command variables and the user input string
	##############################################################################
	def reset_vars(self):
		# user command variables
		self.userInputString = ''		# the input string 
		self.commandString = ''			# the command the user wants to execute
		self.commandArgList = []			# the list of arguments for the command
		self.commandOptionsList = [] 	# the list of options for the command, if they exist
		self.commandRemainingArgs = [] 	# the list of arguments that are NOT options\
		self.commandPATHs = []			# the [PATTERN] arguments, if they exist
		self.commandFILEs = []     		# the [FILE] arguments, if they exist
		self.commandPATTERN = ''			# the [PATH] argument, if it exists

	##############################################################################
	# "print_command_vars"
	##############################################################################
	def print_command_vars(self, lineNum):
		## DEBUGGING ##
		print('\n')
		print('line ', lineNum)
		print('Command: ', self.commandString)
		print('Options: ', self.commandOptionsList)
		print('Remaining Args: ', self.commandRemainingArgs)
		print('PATHs:    ', self.commandPATHs)
		print('FILEs:    ', self.commandFILEs)
		print('PATTERN: ', self.commandPATTERN)	
		print('isInputValid: ', self.isInputValid)
		print('\n')

	##############################################################################
	# "throw_error"
	# print the error, reset vars
	##############################################################################
	def throw_error(self, string):
		print()
		print(string)
		self.reset_vars()

	##############################################################################
	# "get_command_arg"
	# get all legal options from the input string
	##############################################################################
	def get_command_and_option_args(self):
		# store the command in commandString
		self.commandString = self.userInputStringList[0]

		# get all strings starting with a '-'
		for string in self.userInputStringList:
			# is the string an option?
			if string[0] == '-':
				# is the option legal for the corresponding command?
				if self.commandString == './mini-grep':
					# is the option legal?
					if string  in self.LEGAL_GREP_OPTIONS:
						# add option to options list
						self.commandOptionsList.append(string)
						# remove option from input list

					else:
						self.throw_error("Error, illegal options detected! Please check that all options are legal")

				elif self.commandString == './mini-ls':
					# is the option legal?
					if string  in self.LEGAL_LS_OPTIONS:
						# add option to options list
						self.commandOptionsList.append(string)
					else:
						self.throw_error("Error, illegal options detected! Please check that all options are legal")

				elif self.commandString == './mini-df':
					# is the option legal?
					if string  in self.LEGAL_DF_OPTIONS:
						# add option to options list
						self.commandOptionsList.append(string)
					else:
						self.throw_error("Error, illegal options detected! Please check that all options are legal")

				else:
					self.throw_error("Error, illegal command! Please use ./mini-grep, ./mini-ls or ./mini-df")

		# check for leftover arguments and add them to commandRemainingArgs
		for string in self.userInputStringList:
			if string not in self.commandString and string not in self.commandOptionsList:
				self.commandRemainingArgs.append(string)


	##############################################################################
	# "get_paths_or_files"
	# checks list of strings for valid files and paths
	##############################################################################
	def get_path_or_file_args(self):
		# check for a list of files or paths
		if '[' in self.userInputString:
			# get everything within the [] as a string
			tempLeftBracketIndex = self.userInputString.index('[') + 1
			tempRightBracketIndex = len(self.userInputString.strip())

			# keep track of left brackets
			tempLeftBracketCounter = 0
			tempIsListClosed = False
			# store everything in between [] as a string
			tempStr = ''

			# from the index at '[' to the index at ']''
			for char in range(tempLeftBracketIndex, tempRightBracketIndex):
				# ignore ', " and ]
				if self.userInputString[char] != "'" and self.userInputString[char] != '"' and self.userInputString[char] != ']':
					tempStr = tempStr + self.userInputString[char]
				# inc the counter if [ is found
				if self.userInputString[char] == '[':
					tempLeftBracketCounter += 1
				#  is there a closing ]
				if self.userInputString[char] == ']':
					# is the ] closing the list?
					if tempLeftBracketCounter != 0:
						tempLeftBracketCounter -= 1 
						tempStr = tempStr + self.userInputString[char]
					else:
						# the list is closed, if there is more text after throw an error
						tempIsListClosed = True

				# if the list is closed and there are characters after, throw an error
				if tempIsListClosed: 
					if char < tempRightBracketIndex-1:
						self.throw_error("Error, arguments found after list")
						break
					else:
						break

			# store the list of files / paths
			tempFileorPathList = tempStr.split(", ")

			# check if the paths and files are valid
			for string in tempFileorPathList:
				# path?
				if os.path.isdir(string):
					self.commandPATHs.append(string)
			
				# file?
				elif os.path.isfile(string):
					self.commandFILEs.append(string)

	##############################################################################
	# "get_pattern_arg"
	# after the command, options, files and paths have been removed, the only 
	# string that could remain is a pattern argument
	##############################################################################
	def get_pattern_arg(self):
		
		if len(self.commandRemainingArgs) != 0:
			# only ./mini-grep will accept pattern args
			if self.commandString == './mini-grep':
				# there should only be one argument remaining, split to check for spaces
				# the first argument must be a pattern
				if len(self.commandRemainingArgs) >= 1:
					self.commandRemainingArgs = self.commandRemainingArgs[0].split(" ")
					# store PATTERN if it is a regex
					if re.match('^[a-zA-Z0-9]+$', self.commandRemainingArgs[0]):
						self.commandPATTERN = self.commandRemainingArgs[0]
						# remove pattern from remaining args
						self.commandRemainingArgs.remove(self.commandPATTERN)

					else:
						self.throw_error("Error, PATTERN must be a valid regular expression")
				# if there are mutliple args left, throw an error
				else:
					self.throw_error("Error, too many arguments")
					return					

		# there are no args left, there is no PATTERN arg for the grep function
		elif len(self.commandRemainingArgs) == 0:
			# if there is no PATTERN arg for mini-grep, throw an error
			if self.commandString == './mini-grep':
				self.throw_error("./mini-grep requires a PATTERN argument!")

	##############################################################################
	# "validate_input()"
	##############################################################################
	def validate_input(self):
		# ./mini-grep [-q] -e PATTERN [FILE...]
		if self.commandString == './mini-grep':	
			# if no pattern is found, throw an error
			if len(self.commandPATTERN) == 0:
				self.throw_error("Error, ./mini-grep needs a PATTERN argument!")
			# if a pattern is found, and there are no remaining args, the input is valid
			elif len(self.commandRemainingArgs) == 0:
				self.isInputValid = True
			# else there are too many arguments or some args may be invalid
			else:
				self.throw_error("Error, too many arguments or some arguments are invalid! Please check the syntax")

		# ./mini-ls [-r] [FILE...] or ./mini-df [-h] [PATH...]
		elif self.commandString == './mini-ls' or self.commandString == './mini-df':
			# after all arguments are parsed, there should be no arguments left
			if len(self.commandPATTERN) != 0:
				self.throw_error("Error, too many arguments!")
			else:
				self.isInputValid = True

		else:
			self.reset_vars()

		#self.print_command_vars(328)

	##############################################################################
	# "parse_user_input"
	# get a string from the user and make sure the command and args are valid
	##############################################################################
	def parse_user_input(self):
		# loop until the program receives valid input
		self.isInputValid = False
		# all legal options
		self.legalOptionsList = self.union(self.LEGAL_GREP_OPTIONS, self.union(self.LEGAL_LS_OPTIONS, self.LEGAL_DF_OPTIONS))

		# loop until we get valid input
		while not self.isInputValid:
			# get the input string from the user
			self.userInputString = input("Please enter a mini-command:\n")

			# if no input was detected, try again
			while self.userInputString == "":
				self.throw_error('Error, the command you entered was not legal, command syntax is: "./mini-cmd -option(s) PATTERN ["\\FILE\\" or "\\PATH\\"]" ')
				self.userInputString = input("Error, no input. Please enter a mini-command:\n")
				self.userInputString.strip()

			# split up the input string into a list of strings
			self.userInputStringList = self.userInputString.split()

			# is the command legal?
			if self.userInputStringList[0] in self.LEGAL_COMMANDS:				
				# get the needed data from the input string
				self.get_command_and_option_args()
				self.get_path_or_file_args()
				self.get_pattern_arg()
				# check if the input is legal
				self.validate_input()

			# the command is not legal, let the user know and try again
			else:
				self.throw_error('Error, the command you entered was not legal, command syntax is: "./mini-cmd -option(s) PATTERN ["\\FILE\\" or "\\PATH\\"]" ')


##############################################################################
# main function
##############################################################################
if __name__ == '__main__':

	miniLinuxInstance = MiniLinux()

	try:
		# main loop
		while True:
			# get user input only if the command and args are legal 
			miniLinuxInstance.parse_user_input()

			# some space for clarity
			print('')

			# exectute the desired command
			if miniLinuxInstance.commandString == './mini-grep':
				miniLinuxInstance.mini_grep()
			elif miniLinuxInstance.commandString == './mini-ls':
				miniLinuxInstance.mini_ls()
			elif miniLinuxInstance.commandString == './mini-df':
				miniLinuxInstance.mini_df()

			# some space for clarity
			print('')

			# reset all variables
			miniLinuxInstance.reset_vars()

			

	# exit on ctrl-c
	except KeyboardInterrupt:
		print("Stopping program...")
	