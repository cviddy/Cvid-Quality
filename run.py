import requests
import json

from_date = '2018-06-01'
to_date = '2018-06-27'

base_url = 'https://api.github.com'
search = '/search/issues'

secrets = json.load(open('local.json'))

query = base_url + search + '?q=org:hudl+label:"Type: Hotfix"+is:merged+merged:{from_date}..{to_date}&access_token={token}'.format(
    from_date=from_date,
    to_date=to_date,
    token=secrets['token'])

response = requests.get(query)
body = response.json()

print(query)
print(body)

hotfixes = []

for item in body['items']:
    hotfixes.append(item['pull_request']['html_url'])


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