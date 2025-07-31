import os
from datetime import date, timedelta

def confirm_dir_exists(dir_path):
    """
    Makes sure whether the directory path given exists. If it does not,
    then it creates one and returns the path.
    """

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return dir_path

def get_week_start(d=None):
    """
    Return Monday date as start of week 
    """
    d = d or date.today()
    return d - timedelta(days=d.weekday())
