import os  # for API Token and Security Key stored in Environment Variables
from bs4 import \
    BeautifulSoup  # for parsing and modifying twiml response - need lxml

from praw import Reddit # python wrapper for Reddit API

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse


def get_joke():
    reddit_client_id = os.environ['REDDIT_CLIENT_ID']
    reddit_client_secret = os.environ['REDDIT_CLIENT_SECRET']

    reddit = Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent="A Joke")

    joke = []
    for submission in reddit.subreddit("3amjokes").hot(limit=1):
        joke.append(submission.title.strip())
        if submission.selftext:
            joke.append(submission.selftext.strip())

    return joke

def create_message(messages):
    with open("outline.xml", 'r') as outline:
        outline_xml = BeautifulSoup(outline.read(), features="xml")
        for message in messages:
            say_tag = outline_xml.new_tag('Say')
            say_tag.string = message
            outline_xml.Response.append(say_tag)
        # print(outline_xml.prettify())
    return outline_xml.prettify()

def place_call(caller, reciever, message):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml=message,
        to=reciever,
        from_=caller
    )

    response = VoiceResponse()
    response.gather()
    print(response)


def joke_text():
    pass

def joke_call(call_list):
    for person_to_call in call_list:
        place_call('+15103190442', person_to_call, create_message(get_joke()))
