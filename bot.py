import requests
import json
import time
import tweepy
import os
import utilities as ut

url = "https://api.x.immutable.com/v1/orders?"
headers = {"Accept": "*/*"}
payload = {'direction': 'desc', 'status': 'filled', 'buy_token_address': '0xac98d8d1bb27a94e79fbf49198210240688bb1ed'} # replace contract address with desired collection (currently for Book Games) 

url2 = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc&per_page=100&page=1&sparkline=false'"
headers2 = {"Accept": "application/json"}

latest_tx = ""
posted_tx = ""

while True:
    response = requests.request("GET", url, headers=headers, params=payload)
    time.sleep(5)
    
    data = response.text
    parse_json = json.loads(data)
    NFT_Txn_Hash = parse_json["result"][0]["order_id"]
    latest_tx = NFT_Txn_Hash
    NFT_Name = parse_json["result"][0]["buy"]["data"]["properties"]["name"]
    NFT_Image_URL = parse_json["result"][0]["buy"]["data"]["properties"]["image_url"]
    NFT_Purchased_By = parse_json["result"][0]["user"]
    NFT_Purchase_Price_API = parse_json["result"][0]["sell"]["data"]["quantity"]
    NFT_Purchase_Price = int(NFT_Purchase_Price_API)/1000000000000000000
    NFT_Purchase_Price_Rounded = str(round(NFT_Purchase_Price,2))
    NFT_Purchase_Currency = parse_json["result"][0]["sell"]["type"]

    response2 = requests.request("GET", url2, headers=headers2)
    data2 = response2.text
    parse_json2 = json.loads(data2)
    Current_ETH_Price = parse_json2[0]['current_price']
    Current_ETH_Price_Rounded = str(round(Current_ETH_Price,-1))
    USD_NFT_Price = Current_ETH_Price * NFT_Purchase_Price
    USD_NFT_Price_Rounded = str(round(USD_NFT_Price,-1))
    
    if NFT_Purchase_Currency == "ETH":
        Tweet_Text = "'"+NFT_Name+"'"+" was just purchased for "+NFT_Purchase_Price_Rounded+NFT_Purchase_Currency+" (~$"+USD_NFT_Price_Rounded+")"+"\n" "Buyer: "+NFT_Purchased_By+"\n" "https://tokentrove.com/collection/BookGames/imx-"+str(NFT_Txn_Hash)+"?sold=trueOrder"+"\n" "#BookGames #VeeFriends"
    else:
        Tweet_Text = "'"+NFT_Name+"'"+" was just purchased for "+NFT_Purchase_Price_Rounded+NFT_Purchase_Currency+"\n" "Buyer: "+NFT_Purchased_By+"\n" "https://tokentrove.com/collection/BookGames/imx-"+str(NFT_Txn_Hash)+"?sold=trueOrder"+"\n" "#BookGames #VeeFriends"
        continue

    print("Latest Tweet:", Tweet_Text)
    
    consumer_token = "" # fill in from Twitter Developer API
    consumer_secret = "" # fill in from Twitter Developer API
    key = "" # fill in from Twitter Developer API
    secret = "" # fill in from Twitter Developer API
    twitter_username = "" # Twitter handle

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

    # Determines whether bot should tweet

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
