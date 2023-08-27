import tweepy
import pandas
import requests
import json

bearer_token = ("AAAAAAAAAAAAAAAAAAAAAIgBigEAAAAAsx5kPMshGB7oKN%2FEdLzqJfxAE0s%3DIVJ5vS2W5EhFweG9HTv4LdhHXoOmrKDpfEC4P1u6iuf9aguR3b")

senators = pandas.read_excel('PoliticianPunch\congress_twitter.xlsx')
reps = pandas.read_excel('PoliticianPunch\congress_twitter.xlsx', sheet_name=2)
client = tweepy.Client(bearer_token)

def create_url(TwitterName):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=" + TwitterName
    user_fields = "user.fields=id"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def createID(TwitterName):
    url = create_url(TwitterName)
    json_response = connect_to_endpoint(url)
    return json.dumps(json_response, indent=4, sort_keys=True).split('"')[5]

def senatorMentionCount(senators):
    tempList = []
    for i in range(0, len(senators.index)):
        link = senators.at[i, 'Link']
        username = link.split('/')[3]
        mentionCount = client.get_recent_tweets_count(username)
        tempList.append(mentionCount.meta['total_tweet_count'])
    senators['Mention Totals'] = tempList

def representativeMentionCount(reps):
    tempList = []
    for i in range(0, 39):
        link = reps.at[i, 'Link']
        username = link.split('/')[3]
        mentionCount = client.get_recent_tweets_count(username)
        tempList.append(mentionCount.meta['total_tweet_count'])
    reps['Mention Totals'] = tempList

def senatorFollowCount(senators):
    tempList = []
    for i in range(0, len(senators.index)):
        link = senators.at[i, 'Link']
        username = link.split('/')[3]
        followerCount = len(client.get_users_followers(createID(username)))
        tempList.append(followerCount)
    senators['Follower Count'] = tempList

def representativeFollowCount(reps):
    tempList = []
    for i in range(0, len(reps.index)):
        link = reps.at[i, 'Link']
        username = link.split('/')[3]
        followerCount = len(client.get_users_followers(createID(username)))
        tempList.append(followerCount)
    reps['Follower Count'] = tempList

def main():
    #senatorMentionCount(senators)
    #senatorFollowCount(senators)
    representativeMentionCount(reps)
    #representativeFollowCount(reps)
    #senators.to_excel('PoliticianPunch\outputCount.xlsx', sheet_name = 'Senators')
    reps.to_excel('PoliticianPunch\outputCount.xlsx', sheet_name = 'RepsTemp')
main()
