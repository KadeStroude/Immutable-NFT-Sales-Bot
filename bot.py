import requests
import json
import time
import tweepy
import os
import utilities as ut

url = "https://api.x.immutable.com/v1/orders?"
headers = {"Accept": "*/*"}
payload = {'direction': 'desc', 'status': 'filled', 'buy_token_address': '0xac98d8d1bb27a94e79fbf49198210240688bb1ed'}

latest_tx = ""
posted_tx = ""

while True:
    response = requests.request("GET", url, headers=headers, params=payload)
    time.sleep(10)
    
    data = response.text
    parse_json = json.loads(data)
    NFT_Txn_Hash = parse_json["result"][0]["order_id"]
    latest_tx = NFT_Txn_Hash
    NFT_Name = parse_json["result"][0]["buy"]["data"]["properties"]["name"]
    NFT_Image_URL = parse_json["result"][0]["buy"]["data"]["properties"]["image_url"]
    NFT_Purchased_By = parse_json["result"][0]["user"]
    NFT_Purchase_Price_API = parse_json["result"][0]["sell"]["data"]["quantity"]
    NFT_Purchase_Price = str(int(NFT_Purchase_Price_API)/1000000000000000000)

    Tweet_Text = "'"+NFT_Name+"'"+" was just purchased for "+NFT_Purchase_Price+" ETH by "+NFT_Purchased_By+"\n" "Order ID: "+str(NFT_Txn_Hash)+" #BookGames #VeeFriends"
    print("Latest Tweet:", Tweet_Text)

    consumer_token = ""
    consumer_secret = ""
    key = ""
    secret = ""
    twitter_username = ""

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print("Error! Failed to get request token.")

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Twitter Authentication Success")
    except:
        print("Twitter Authentication Error")

    # Should I tweet

    if latest_tx == posted_tx:
        print("This has been tweeted already, here: ",  latest_tx)
        continue

    image_name = "nft_image.png"
    response = requests.get(NFT_Image_URL)
    file = open(image_name, "wb")
    file.write(response.content)
    file.close()
    ut.create_background(image_name, (96, 131, 151))


    # Post the message in your Twitter Bot account
    # with the image of the sold NFT attached
    media = api.media_upload(image_name)
    # Post the message in your Twitter Bot account
    # with the image of the sold NFT attached
    res_status = api.update_status(
    status=Tweet_Text, media_ids=[media.media_id])

    posted_tx = latest_tx
