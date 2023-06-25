import pandas as pd
from datetime import datetime
from backend.controllers.file_access import config_reader
from backend.controllers.eve_connection import get_char_info

def basic_info():
    """
    Gets basic info on the user. Limited bu an OAuth requirement.
    Returns an excel spreadsheet.
    """

    user_id = str(config_reader('user','user_id'))
    player_data = get_char_info(user_id)['name']

    now = datetime.now()
    time_now = now.strftime("%m/%d/%Y, %H:%M:%S")

    df = pd.concat([pd.DataFrame.from_records([{'player_name': player_data}]), pd.DataFrame.from_records([{'last_ran': time_now}])], axis = 1)

    return df