import requests
import json
import datetime

secrets = json.load(open('local.json'))

def github_search_api_query(tribe):
    """
    Query for the github api that uses search
    :param tribe: 
    """

    toDate = datetime.datetime.today()
    toDateStr = toDate.strftime("%Y-%m-%d")

    fromDate = toDate - datetime.timedelta(days=7)
    fromDateStr = fromDate.strftime("%Y-%m-%d")


    base_url = 'https://api.github.com'
    search = '/search/issues'

    query = base_url + search + '?q=org:hudl+label:"Type: Hotfix"+label:"{tribes}"+is:merged+merged:{from_date}..{to_date}&access_token={token}'.format(
        tribes=tribe.github_label,
        from_date=fromDateStr,
        to_date=toDateStr,
        token=secrets['token'])

    response = requests.get(query)
    body = response.json()
    
    return body

def github_merge_date_PR_query(hot):
    """
    Hits githubs PR api to get PR information

    :param hot: 
    """

    # https://developer.github.com/v3/pulls/#get-a-single-pull-request
    query2 = hot + '?access_token={token}'.format(token=secrets['token'])
    response2 = requests.get(query2)
    body2 = response2.json()

    url = body2['html_url']
    merged_date = body2['merged_at']

    dates_urls = str(merged_date) + ' - ' + url + ' ' 

    return dates_urls
