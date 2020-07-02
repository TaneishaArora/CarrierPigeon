import os  # for API Token and Security Key stored in Environment Variables
from praw import Reddit  # python wrapper for Reddit API

from twilio.rest import Client  # to make request to TWILIO API
from twilio.twiml.voice_response import VoiceResponse, \
    Say  # to construct response

# twillio creds
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# reddit creds
reddit_client_id = os.environ['REDDIT_CLIENT_ID']
reddit_client_secret = os.environ['REDDIT_CLIENT_SECRET']


def get_joke():
    reddit = Reddit(client_id=reddit_client_id,
                    client_secret=reddit_client_secret,
                    user_agent="A Joke")

    joke = []
    for submission in reddit.subreddit("3amjokes").hot(limit=1):
        joke.append(submission.title.strip())
        if submission.selftext:
            joke.append(submission.selftext.strip())

    return joke


def create_voice_message(messages):
    response = VoiceResponse()
    for message in messages:
        response.append(Say(message, level='strong', language="en-GB"))

    return response


def create_text_message(messages):
    response = 'Prepare to laugh your guts out!\n\n'

    return response + '\n'.join(messages)


def place_call(caller, receiver, message):
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml=message,
        to=receiver,
        from_=caller
    )

    print(call.sid)


def send_text(caller, receiver, message):
    client = Client(account_sid, auth_token)

    text = client.messages.create(
        body=message,
        to=receiver,
        from_=caller
    )

    print(text.sid)


def joke_text(call_list):
    for person_to_call in call_list:
        send_text('+15103190442', person_to_call,
                  create_text_message(get_joke()))


MEANS = {'call': place_call, 'text': send_text}

def send_joke(call_list, methods):
    joke = get_joke()
    for person_to_call in call_list:
        for method in methods:
            MEANS[method]('+15103190442', person_to_call, create_text_message(
                joke) if method == 'text' else create_voice_message(joke))
