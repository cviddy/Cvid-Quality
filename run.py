import requests
import json
import datetime

from diff import get_diff

from slackclient import SlackClient

toDate = datetime.datetime.today()
toDateStr = toDate.strftime("%Y-%m-%d")

fromDate = toDate - datetime.timedelta(days=7)
fromDateStr = fromDate.strftime("%Y-%m-%d")

base_url = 'https://api.github.com'
search = '/search/issues'

secrets = json.load(open('local.json'))

# When creating github api calls you always need access token at the end of url
query = base_url + search + '?q=org:hudl+label:"Type: Hotfix"+is:merged+merged:{from_date}..{to_date}&access_token={token}'.format(
    from_date=fromDateStr,
    to_date=toDateStr,
    token=secrets['token'])

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
old_hot = get_diff(hotfixes)

hotfix_dates_urls = []
for hot in hotfixes:
    # https://developer.github.com/v3/pulls/#get-a-single-pull-request
    query2 = hot + '?access_token={token}'.format(token=secrets['token'])
    response2 = requests.get(query2)
    body2 = response2.json()

    url = body2['html_url']
    merged_date = body2['merged_at']

    dates_urls = str(merged_date) + ' - ' + url

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

# https://github.com/slackapi/python-slackclient
sc.api_call(
    "chat.postMessage",
    channel="CC756Q56U",
    text=slack_message
)