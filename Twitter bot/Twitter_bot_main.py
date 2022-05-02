import tweepy

api_key = open("API_KEY.txt").read()
api_key_secret = open("API_KEY_SECRET.txt").read()
access = open("ACCESS_TOKEN.txt").read()
access_secret = open("ACCESS_TOKEN_SECRET.txt").read()
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access, access_secret)

api = tweepy.API(auth)

if __name__ == "__main__":
    try:
        api.verify_credentials()
        api.update_status("Próximamente...")
    except:
        print("Error during authentication")
