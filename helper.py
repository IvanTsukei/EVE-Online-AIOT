from pathlib import Path
import requests

def file_path(upath):
    """
    gets the filepath
    """
    return Path(__file__).parent.resolve() / upath # Points to the file