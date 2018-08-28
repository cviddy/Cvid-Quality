import requests
import json
import datetime

from github.github import *

from slackclient import SlackClient
from diff import get_diff

# Once tribes become more widely adopted with their labels we can run this to send messages out to tribe channels.
tribes = ["Tribe: Analysis", "Tribe: Starship Enterprise"]

# When creating github api calls you always need access token at the end of url
for tribe in tribes: 

    query = github_search_api_query(tribe)

    print(query)
    response = requests.get(query)
    body = response.json()

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
    with open('results.txt', 'a') as file:

        # DELETE old contents of results
        file.seek(0)
        file.truncate()

        # Add new
        for hotfix in hotfix_dates_urls:
            file.write(hotfix + "\n")


    # Use slacks API to post to a room of your choosing. Currently posting to a test channel
    # must generate a slack api token here: https://api.slack.com/custom-integrations/legacy-tokens
    # TODO: Look into making an application since legacy tokens are no longer supported
    slack_token = secrets['slacktoken']
    sc = SlackClient(slack_token)

    slack_message = "Hey @cvid take a look at these hotfixes  " + str(hotfix_dates_urls)

    if tribe == "Tribe: Analysis":
        # https://github.com/slackapi/python-slackclient
        sc.api_call(
            "chat.postMessage",
            channel="CC756Q56U",
            text=slack_message
        )
    elif tribe == "Tribe: Starship Enterprise":
        # https://github.com/slackapi/python-slackclient
        sc.api_call(
            "chat.postMessage",
            channel="CC756Q56U",
            text=slack_message
        )
    else: 
        pass