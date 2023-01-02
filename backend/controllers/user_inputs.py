from tkinter import NUMERIC
from unicodedata import numeric
import pandas as pd
from backend.controllers.file_access import file_path, all_files

def get_file_name():
    '''
    Gets the name of the file being accessed. 
    '''
    current_files = all_files()
    # while True:
    #     file_input = input(f'Which Excel File would you like to work with?:\n{current_files}\n> ') # User input

    #     if file_input[-5:] != '.xlsx':
    #         file_input = file_input + '.xlsx'

    #     try:
    #         file_name = file_path(file_input)
    #         df = pd.read_excel(file_name)
    #         break
    #     except FileNotFoundError:
    #         print('Invalid file name.')

    # return file_path(file_input)
    return file_path('itemIDs.xlsx')

def sheet_selection(data_selection):
    '''
    Lets user select which sheet to work with.
    '''
    data_check = pd.ExcelFile(data_selection) # Loads the excel file
    sheets = [x for x in data_check.sheet_names] # Places the sheet names in a list

    if len(sheets) > 1: # Ensures the sheet exists
        print(f'\nWhich sheet?\n--------------\n{sheets}\n')
        while True:
            sheet_choice = input('> ')
            if sheet_choice not in sheets:
                print('This sheet does not exist.')
            else:
                break

        return data_check.parse(sheet_choice)

def option_selection(data_selection):
    '''
    Lets user select what to do with the data.
    '''
    print('\nWhat would you like to do? Type the number to continue.\n1. View Data\n2. Modify Data\n--------------\n')
    while True: # Ensures a valid input is given
        user_choice = input('> ')
        try:
            if int(user_choice) and 0 < int(user_choice) <= 4: # Not working
                break
        except ValueError:
            print('Please make a valid selection from the list.')

    if user_choice == '1': # View Data 
        df = sheet_selection(data_selection)
        print(df)
    elif user_choice == '2': # Modify Data
        df = sheet_selection(data_selection)

        # User alert on pricing auto update starting.
        sheet_check = [x for x in df.columns]
        if sheet_check[1] == 'Price':
            print('Initiating market data update...')
        
        print(df)
        pass

    return user_choice