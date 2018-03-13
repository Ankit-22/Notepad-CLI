from sys import argv
from selenium import webdriver
from my_notepad import my_notepad

driver = webdriver.PhantomJS()
driver.set_window_size(1366, 768)
cli = my_notepad(driver, argv[1])
if cli.padContent != "":
	print("The notepad already has contents: ", end = " ")
	print(cli.padContent)
	print("\n\n")
	print("Do you want to append data? (yes / no)")
	if input()[0] == 'y':
		cli.send_data(cli.padContent + argv[2])
		exit()
	else:
		print("Cannot overwrite an old notepad")
		exit()
cli.send_data(argv[2])