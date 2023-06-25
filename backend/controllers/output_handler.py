import pandas as pd
from datetime import timedelta
import time
from backend.controllers.market_generator import sell_orders
from backend.controllers.player_info import basic_info
from backend.controllers.file_access import config_reader, file_path

def run_program():
    """
    Runs the program. Takes each individual dataframe (market data & player data)
    and uses a writer to output to one file as separate sheets.
    """

    output_name = str(config_reader('data','output_name'))
    writer = pd.ExcelWriter(file_path(f'outputs/{output_name}.xlsx'), engine = 'xlsxwriter')

    # Handle the output to each sheet #
    print('\n--------------\nStarting the program...')
    start_time = time.monotonic()
    
    sell_orders().to_excel(writer, sheet_name = 'Market Data', index = False)
    basic_info().to_excel(writer, sheet_name = 'Player Data', index = False)
    writer.close()

    end_time = time.monotonic()
    print(f'\nDONE! Check data/outputs.\nProgram took {str(timedelta(seconds = end_time - start_time)).split(".")[0]} minutes.\n')