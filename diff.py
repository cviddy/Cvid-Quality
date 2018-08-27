import requests
import json
import datetime


def get_diff(hotfixes):
    """
    At somepoint we will be running these consistenly where we might have overlap in timeframes. 
    This diff should give us a list of urls that aren't overlapping.
    """

    toDate = datetime.datetime.today()
    sevenDaysAgo = toDate - datetime.timedelta(days=7)
    sevenDayStr = sevenDaysAgo.strftime("%Y-%m-%d")

    fourteenDaysAgo = toDate - datetime.timedelta(days=14)
    fourteenDayStr = fourteenDaysAgo.strftime("%Y-%m-%d")

    base_url = 'https://api.github.com'
    search = '/search/issues'

    secrets = json.load(open('local.json'))

    # When creating github api calls you always need access token at the end of url
    oldQuery = base_url + search + '?q=org:hudl+label:"Type: Hotfix"+is:merged+merged:{from_date}..{to_date}&access_token={token}'.format(
        from_date=fourteenDayStr,
        to_date=sevenDayStr,
        token=secrets['token'])

    oldResponse = requests.get(oldQuery)
    oldBody = oldResponse.json()

    # Creates list of urls for api call to get single PR information
    old_hotfixes = []
    for item in oldBody['items']:
        old_hotfixes.append(item['pull_request']['url'])

    # Can use this to exclude urls of PRs we don't want to track
    # Eventually might want to remove npm packages and js bundles
    # Can add more ifs to list below to exclude any repos
    old_hotfixes = [
        url for url in old_hotfixes
        if 'npm' not in url.lower()
    ]

    diff_hotfixes = []
    for diff in hotfixes:
        if diff not in old_hotfixes:
            diff_hotfixes.append(diff)

    diff_hotfixes = diff_hotfixes + old_hotfixes

    print(diff_hotfixes)

    return diff_hotfixes