# NFT Sales Twitter Bot for the Immutable X Layer 2 Scaling Solution 🤖

## Aims 🎯

The aim is to monitor all sales across the `Immutable X` roll-up for a given contract.

In order to find the relevant Layer 2 contract for your project, [Immutascan.io](https://immutascan.io/) is a good a resource to leverage. Right now the bot has used the `contract address` for Book Games NFT - you can see the output on Twitter [here](https://twitter.com/BookGamesBotv2).

## Donations 💵

Donations are always appreciated!🙏

Eth Address: 0xc2e54856b0F02E52299573dfd7F4971b275b17a9

## Setup 🔧

### - Twitter

- Request a [Twitter Developer Account](https://developer.twitter.com/en/apply-for-access) (with [Elevated Access](https://developer.twitter.com/en/portal/products/elevated), then create a Twitter Developer App (make sure you change it to have both read/write permissions)

- Make sure you are logged in to the Twitter account you want the bot to run on (as the next step will be authorizing the bot to post on your account)

### - Heroku

The bot provided can run locally, however if you want to use a cloud hosting platform to do some of the heavy listing, Heroku is likely the most convenient solution. What I have provided in this repo can be used with any service. If you choose to push to Heroku, you will need to take some extra steps, by following this guide - [Heroku / Python framework](https://devcenter.heroku.com/articles/getting-started-with-python).

If you are having any issues with this step, feel free to reach out and I can walk you through it, but in short:

- Create a new Heroku account + app& set the project as a remote branch of your git repo (see [Heroku Remote](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote))

Now you're ready to release - just push up the code via. git to the Heroku remote (see [Heroku Remote](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote) if unsure how, and if any issues, ensure you are following the [Heroku / Python framework](https://devcenter.heroku.com/articles/getting-started-with-python).

Make sure you are using `worker` dynos and not `web` dynos - you can set this in the CLI your project with:

```sh
heroku ps:scale web=0
heroku ps:scale worker=1
```

## License 📃

This code is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

Please include proper attribution to my original repo if you fork, modify or utilize this repo in any way. Thank you!
