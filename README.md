# CommandCenter

CommandCenter is a tool designed to track your favorite people, artists and actors across multiple social networks, games, and systems such as Spotify, LinkedIn, League of Legends and others. The idea for this application is to notify on Slack whenever these actors posts something new in an attempt to facilitate communication among so many overwhelming apps for the real important people you want to follow.

## Features

- **Multi-Platform Tracking:** Monitor actors on various social networks and systems including Spotify, LinkedIn, and more.
- **Real-Time Notifications:** Receive instant Slack notifications whenever a new post is uploaded.
- **Customizable Watchlist:** Easily add or remove actors from your watchlist.
- **User-Friendly Interface:** Simple and intuitive interface for seamless user experience.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- A Slack account and a Slack App with appropriate permissions
- API keys for the social networks and systems you want to track

### Contribution

1. Clone the repo:
   ```sh
   git clone https://github.com/abaddonpuff/commandCenter.git
   cd commandCenter

3. Install requirements from the requirements file
   ```sh
   pip install -r requirements.txt

3. Install PostgreSQL

2. Create a .env file and add your configuration details:
    ```sh
      X_API_KEY=YOUR_X_API_KEY
      X_API_SECRET=YOUR_X_API_SECRET
      X_BEARER_TOKEN=X_BEARER_TOKEN
      X_ACCESS_TOKEN=YOUR_X_ACCESS_TOKEN
      X_ACCESS_TOKEN_SECRET=YOUR_X_TOKEN_SECRET
      CLIENT_ID=YOUR_X_CLIENT_ID
      CLIENT_SECRET=YOUR_X_CLIENT_SECRET
      SPOTIFY_CLIENTID=YOUR_SPOTIFY_CLIENT_ID
      SPOTIFY_CLIENT_SECRET=YOUR_SPOTIFY_CLIENT_SECRET
      LEAGUE_API_KEY=YOUR_LEAGUE_OF_LEGENDS_API_KEY
      SLACKBOT_OAUTH=YOUR_SLACKBOT_OAUTH_KEY
      SLACK_C2NOTIFIER=YOUR_SLACK_CHANNEL_WEBHOOK
      SECRET_KEY=A_DJANGO_SECRET_KEY
      ALLOWED_HOSTS=.localhost,.herokuapp.com
      DEBUG=True
      DATABASE_URL=postgres://postgres:password@0.0.0.0:5432/commandcenter


### Deployment
The app can be deployed with the right API on AWS, Heroku, etc.

https://stark-escarpment-39840-ce9415be8f72.herokuapp.com/


