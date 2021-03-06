# Musk Crypto Notifier

## Purpose

To get notified when Elon Musk tweets about cryptocurrency.

As a general use case, this system is able to watch tweets for a particular user (or users) and notify of keyword matches via Discord.

This system could be useful for anyone wanting to get in on the one man pump machine.

## Join the Discord server

To get notified of Musk's tweets via Discord, please follow the invite link:

https://discord.gg/CEfHQ8uc

## Concept

This system watches a Twitter user for any new tweets.

When the user makes a tweet, the system scans the tweet text for references and possible references to cryptocurrency.

There are 2 key threads for tweet detection, these are 'tweets' and 'possible tweets'.

For each thread there is a list of keywords which are very likely to be related to cryptocurrency, e.g. `bitcoin`, `doge`...

The second thread contains possible references to cryptocurrency, words which may in some contexts be appropriate to watch out for, e.g. `to the moon`, `hodl`...

The system is case-insensitive, so as far as it is concerned, `DOGE` is interpreted the same as `doge` and `DoGe`.

For tweets which contain images, analysis is outsourced to Google Vision API

Text within the image can be analysed using the same keywords list.

Features identified by Google Vision API can also be watched for. For example, we might want to look out for pictures of dogs.

## Future work

It would be useful to follow other prominent players in crypto, both for signals of positive and negative impacts.

For example, it might be useful to follow government accounts for news of crypto restrictions, taxes etc.

## Support this project

| Coin          | Address                                    |
|---------------|--------------------------------------------|
| Bitcoin (BTC) | bc1qye7vg6gu23sh4g472j7mjpp6z30h8h86znxx6e |
| Etherium (ETH)| 0xB2AD04EF80e4B92d81DaF6316282cf3185B69e72 |
| Doge (DOGE)   | DRKNh5ZAw6EMgMxQfdy9wTycC1tti2WPiQ         |
| Ripple (XRP)  | rEV2nW8BnLf4p5UCUnyZjTUzWZQqvbtr3W         |

## Contributing

I welcome proposals or contributions to the code, please make a pull request.

I would also be keen to get some other ideas for keywords to include in the system. If you have any ideas please join the discussion on the Discord server.

## Installation

### Prerequisites

* Docker
* Twitter developer account ([apply for one here](https://developer.twitter.com/en/apply-for-access))
* A Discord server with channels for `logs`, `tweets`, and `possible tweets`
* Access to Google Vision API (which requires a billing enabled account)

### Environment variables

The application is configured using settings defined in a file named `.env`. 

These are environment variables which get passed into the Docker container.

```
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
TWITTER_USER_IDS_TO_FOLLOW=1234567890 0987654321
DISCORD_LOGS_WEBHOOK_URL=https://discord.com/api/webhooks/.....
DISCORD_TWEETS_WEBHOOK_URL=https://discord.com/api/webhooks/.....
DISCORD_POSSIBLE_TWEETS_WEBHOOK_URL=https://discord.com/api/webhooks/.....
OFFLINE_MODE=true
```

#### Twitter configuration

In the [Twitter developer portal](https://developer.twitter.com/en/portal/projects-and-apps), create a new app and get the API credentials and copy them into your configuration.

| Key | Description |
|-----|-------------|
| `TWITTER_API_KEY` | API key from Twitter developer account |
| `TWITTER_API_SECRET` | API secret key from Twitter developer account |
| `TWITTER_ACCESS_TOKEN` | Twitter API access token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Secret key for Twitter API access token |
| `TWITTER_USER_IDS_TO_FOLLOW` | Space delimited list of user ids to watch (see [here](https://www.codeofaninja.com/tools/find-twitter-id/) for how to get twitter ids from user name)

#### Google configuration

Set up an account and register for [Cloud Vision API](https://cloud.google.com/vision/) access and set up a service account. Download the client_secrets json file.

For more details on how to set this up, follow [this guide](https://codelabs.developers.google.com/codelabs/cloud-vision-api-python/#0).

Place the file and name it to `google_client_secrets.json` in the same directory as the `docker-compose.yml` file.

Leave the environment varibale `GOOGLE_APPLICATION_CREDENTIALS` to the default set in `.env.example`.

#### Discord configuration

This configuration is needed to tell the bot where to send the logs and crypto tweets.

3 channels are required, one each for logs, definite tweets, and possible tweets.

Discord webhook URLs can be set up for each channel in `Settings -> Integrations`.

| Key | Description |
|-----|-------------|
| `DISCORD_LOGS_WEBHOOK_URL` | Webhook URL for the Discord logs channel |
| `DISCORD_TWEETS_WEBHOOK_URL` | Webhook URL for the Discord definite tweets channel |
| `DISCORD_POSSIBLE_TWEETS_WEBHOOK_URL` | Webhook URI or the Discord possible tweets channel |

#### Other configuration

| Key | Description |
|-----|-------------|
| `OFFLINE_MODE` | Disables access to Twitter and Discord, defaults to `True` so `test.py` can run quick tests without connecting to anything. For running this service, this variable should be set to `False`.

#### Running the service

To build and run the image using Docker, use the following command from the same directory as `docker-compose.yml`.

```shell
docker-compose up --build
```

Or to run it in detached mode (without console logging):

```shell
docker-compose up --build -d
```

### Keywords

The list of keywords analysed can be found in `bot/keywords.json`. The dictionary is split into three sections.

The first section `keywords` is for references that we are certain relate to cryptocurrency.

The section `possible_keywords` is for references which _might_ relate to cryptocurrency.

The section `possible_objects` is for references which the Google Vision API might return.

## Known Issues

* The system searches for keyword matches based on what we give it. For some cases, our keyword may be a part of another word. For example the short name for Etherium `ETH` is likely to show up in commonly used words such as `TEETH`, `DICHLOROMETHANE` and `PLETHYSMOGRAMS`. For this reason, keywords with such common matches are currently excluded. 

* The Python code exits when receiving an error from the Twitter API, however this is saved by Docker, which automatically restarts the service on exit. Ideally, the Python code should be able to handle these errors itself without relying on Docker.



## Risks

It is not possible to predict precisely what keywords can trigger changes in the market.

The current keyword list is pretty much just my best guess for words which may influence the market. I very much welcome ideas for new keywords to include.

There is also a risk of false positive results, this is why the separate keyword list `possible_keywords` is used.

Currently, this service is running on a local physical server. If the power/internet goes out while a crypto tweet comes in the system will miss it. If this service is popular enough I might move it to a cloud server.

## Disclaimer

Under no circumstances shall I, or any other developer on this project be liable for any indirect, incidental, consequential, special or exemplary damages arising out of or in connection with your access or use of or inability to access or not use the application and any third party content and services, whether or not the damages were foreseeable and whether or not I or other developers were advised of the possibility of such damages.

In short, use this application at your own risk, I cannot guarantee its performance, accuracy, or availability.

## License

[MIT](LICENSE)