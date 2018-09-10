import json
from slackclient import SlackClient

secrets = json.load(open('local.json'))
slack_token = secrets['slacktoken']
sc = SlackClient(slack_token)

def send_slack_message_with_list(tribe, hotfix_dates_urls):
    """
    Use slacks API to post to a room of your choosing based on tribe.json
    must generate a slack api token here: https://api.slack.com/custom-integrations/legacy-tokens
    TODO: Look into making an application since legacy tokens are no longer supported
    
    :param tribe: 
    :param hotfix_dates_urls:
    """

    if len(hotfix_dates_urls) > 0: 
        slack_message = "Hey {} take a look at these hotfixes  ".format(tribe.tribe_name) + str(hotfix_dates_urls)

        # https://github.com/slackapi/python-slackclient
        sc.api_call(
            "chat.postMessage",
            channel=tribe.slack_channel,
            text=slack_message
        )
    else: 
        empty_list = "{} Tribe has no hotfixes this week cheers".format(tribe.tribe_name)

        # https://github.com/slackapi/python-slackclient
        sc.api_call(
            "chat.postMessage",
            channel=tribe.slack_channel,
            text=empty_list
        )