# Sonic Discord Bot

This is a Python 3 script for a Discord bot that features Sonic the Hedgehog. The bot responds to messages with various types of responses, including positive, neutral, and funny responses. Additionally, it can fetch a random Sonic meme and send it to the chat.

## Prerequisites

This bot requires the following Python packages to be installed:
- discord==1.7.3
- nltk==3.6.2
- numpy==1.21.4
- openai==0.10.5
- requests==2.26.0

You can install the required packages using pip:
> pip install -r requirements.txt


## Configuration

Before running the script, you need to set up your `config.ini` file. You can use the `config.example.ini` file as a template. Here's what you need to do:
- Rename `config.example.ini` to `config.ini`.
- Fill in the `TOKEN` field with your Discord bot token.
- Fill in the `AUTHORIZED_USER`, `TARGET_USER`, and `TARGET_CHANNEL` fields with the user and channel IDs that you want the bot to interact with.
- Fill in the `OpenAi` `TOKEN` field with your OpenAI API key.

## Usage

To run the bot, execute the following command in your terminal:

> python sonic_bot.py

Once the bot is running, it will respond to various commands and messages. You can use the `/` command prefix to trigger specific bot responses.

## Docker

1. Build the Docker image by executing the following command:

> docker build -t sonic-discord-bot .

This will create a new Docker image with the name "sonic-discord-bot".

2. Run the Docker container by executing the following command:

> docker run -d --restart=always sonic-discord-bot

The "-d" flag tells Docker to run the container in detached mode, meaning it will run in the background. The "--restart=always" flag tells Docker to automatically restart the container if it crashes or is stopped.

3. That's it! Your Sonic Discord bot should now be running inside a Docker container. To check if it's working, you can use the Docker logs command:

> docker logs <container_id>


Replace <container_id> with the ID of your running container, which you can find using the docker ps command.

Note: If you make changes to your bot script or requirements, you'll need to rebuild the Docker image and restart the container for the changes to take effect. You can stop the container using the docker stop command, and start it again using the docker start command.

## Author

This script was created by a developer who loves Sonic the Hedgehog!
