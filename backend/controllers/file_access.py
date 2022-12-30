from pathlib import Path
import os.path

def file_path(upath):
    """
    gets the filepath
    """
    return Path(__file__).parent.resolve() / '../../data' / upath # Points to the file

def all_files():
    """
    Returns all excel files in the folder.
    """
    path = Path(__file__).parent.parent.parent.resolve() / 'data'
    res = [f.__str__().rsplit('\\', 1)[-1] for f in path.glob('*.xlsx')] # f.__str__() faster than str(f). rsplit splits based on \ and gets just file name.
    return res