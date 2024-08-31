# ToGu: Your AI Tour Guide 🗺️

ToGu is an AI-powered virtual tour guide that interacts with users through Telegram.
Built with Python, ToGu leverages AI to provide personalized travel recommendations based on user preferences and current weather conditions. 
This project is designed for educational purposes and fun, with no intention for real deployment (That's why there is a single-user authorization)

## Technologies Used

- **Python**: The core programming language for this project.
- **agency-swarm**: Framework for building and orchestrating AI agents, wrapping OpenAI assistants api.
- **python-telegram-bot**: A library for creating Telegram bots with Python.
- **Foursquare**: A locations search service - provides an API for geo-data querying.

## Getting Started

Follow these instructions to set up and run the ToGu project on your local machine.

### Prerequisites

- Python 3.x installed on your machine.
- Telegram account and a bot token (can be obtained from the BotFather on Telegram).
- OpenAI API key.
- Foursquare API token.
- Your Telegram user id

### Installation
After cloning and setting up your environment with the required packages, set the needed environment values as shown in the example.env file.

## Usage
### Running the bot
To start the Telegram bot and begin interacting with ToGu, run the following:
```bash
python bot.py
```
Just make sure your Telegram User ID is listed in the .env file so the bot would authorise your user.

### Interacting with the AI agent locally
If you want to interact with the AI agent directly, you can use the self-hosted Gradio interface by running the following:
```bash
python TourGuideAgency/agency.py
```

## Future Enhancements
- Incorporate a programmatically generated map of the user's location and the recommendations into the bot's response.
- Create a timeout for a user's session within the bot.
    https://docs.python-telegram-bot.org/en/stable/examples.timerbot.html
- Implement a weather cache to reduce api calls.