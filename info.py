import datetime
import json
import time

from utils.date_util import get_date_from_date_string
from tasks.update_sheets import SheetNames, update_sheet

def get_tribe_label_from_tribes_json(tribe):
    label = 