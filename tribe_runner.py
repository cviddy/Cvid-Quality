import requests
import json
import datetime

from github.github import *
from info import *

from models.create_file import write_results_to_local_file
from models.slack import send_slack_message_with_list


from diff import get_diff

tribes= get_tribes_from_json('tribes.json')

# When creating github api calls you always need access token at the end of url
for tribe in tribes: 

    body = github_search_api_query(tribe)

    # Creates list of urls for api call to get single PR information
    hotfixes = []
    for item in body['items']:
        hotfixes.append(item['pull_request']['url'])

    # Can use this to exclude urls of PRs we don't want to track
    # Eventually might want to remove npm packages and js bundles
    # Can add more ifs to list below to exclude any repos
    hotfixes = [
        url for url in hotfixes
        if 'npm' not in url.lower()
    ]

    # Eventually we will want to make sure we aren't double posting based on when we run the query. 
    # we can avoid this by setting on a schedule from day to day but we can also use this to remove dups
    # old_hot = get_diff(hotfixes)

    hotfix_dates_urls = []
    for hot in hotfixes:

        dates_urls = github_merge_date_PR_query(hot)

        hotfix_dates_urls.append(dates_urls)

    print(hotfix_dates_urls)

    # Or write to a file if you want.
    write_results_to_local_file(hotfix_dates_urls)

    send_slack_message_with_list(tribe, hotfix_dates_urls)