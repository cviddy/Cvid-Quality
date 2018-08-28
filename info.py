import datetime
import json
import time

from models.tribe import Tribe

def get_tribes_from_json(file):
    """
    Gets tribes from the json file. 
    This will allow us to add and delete tribes as they become available. 

    :param file: 

    """

    tribes = json.load(open(file))

    new_tribe_list = []

    for tribe in tribes['tribes']:
        new_tribe = Tribe(tribe['tribe_name'], tribe['github_label'], tribe['slack_channel'])
        new_tribe_list.append(new_tribe)

    return new_tribe_list
