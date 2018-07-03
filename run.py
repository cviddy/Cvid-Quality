import requests
import json
import datetime

toDate = datetime.datetime.today()
toDateStr = toDate.strftime("%Y-%m-%d")

fromDate = toDate - datetime.timedelta(days=7)
fromDateStr = fromDate.strftime("%Y-%m-%d")

base_url = 'https://api.github.com'
search = '/search/issues'

secrets = json.load(open('local.json'))

query = base_url + search + '?q=org:hudl+label:"Type: Hotfix"+is:merged+merged:{from_date}..{to_date}&access_token={token}'.format(
    from_date=fromDateStr,
    to_date=toDateStr,
    token=secrets['token'])

response = requests.get(query)
body = response.json()

hotfixes = []

for item in body['items']:
    hotfixes.append(item['pull_request']['html_url'])

# Can use this to exclude urls of PRs we don't want to track
# Eventually might want to remove npm packages and js bundles
# Can add more ifs to list below to exclude any repos
hotfixes = [
    url for url in hotfixes
    if 'npm' not in url.lower()
]

# Print to console
print(hotfixes)

# Or write to a file if you want.
with open('results.txt', 'a') as file:

    # DELETE old contents of results
    file.seek(0)
    file.truncate()

    # Add new
    for hotfix in hotfixes:
        file.write(hotfix + "\n")