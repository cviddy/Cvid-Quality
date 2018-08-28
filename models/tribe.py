class Tribe(object):
    def __init__(self,
                 tribe_name,
                 github_label,
                 slack_channel):
        self.tribe_name = tribe_name
        self.github_label = github_label
        self.slack_channel = slack_channel