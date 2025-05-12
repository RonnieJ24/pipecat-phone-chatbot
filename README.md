Pipecat Phone Chatbot
This is a submission for the Pipecat AI Software Engineer challenge. It demonstrates a voice-enabled AI assistant that handles incoming phone calls using Twilio and OpenAI GPT.

🌟 Features

- Accepts inbound Twilio calls
- Uses speech recognition and OpenAI to respond
- Detects 10+ seconds of silence and prompts user
- Ends call gracefully after 3 unanswered prompts
- Logs call stats: duration, silence events, and user input

📂 Project Structure

- app.py — Main Flask app
- call_log.txt — Summary of each call
- .env — (not committed) holds the OpenAI key
- requirements.txt — List of dependencies

🚀 Setup Instructions

1- Clone the repo
git clone https://github.com/RonnieJ24/pipecat-phone-chatbot.git
cd pipecat-phone-chatbot

2- Create a virtual environment
python -m venv venv
venv\Scripts\activate (Windows)
or
source venv/bin/activate (Mac/Linux)

3- Install dependencies
pip install -r requirements.txt

4- Set your OpenAI key
Create a .env file:
OPENAI_API_KEY=your-key-here
You can get your key from: https://platform.openai.com/account/api-keys

5- Run the app
python app.py
The server will run on http://127.0.0.1:5000

📞 Use with Ngrok

To expose your app to Twilio:
- Start your server
- Open another terminal and run:
- ngrok http 5000
- Copy the https://xxxxx.ngrok-free.app URL
- Set Twilio webhook for voice calls to:
https://xxxxx.ngrok-free.app/incoming-call

✅ Notes

- The .env file is ignored by Git
- No real-time weather/time API is used — GPT gives conversational responses

📌 Sample Call

User: Hello, can you hear me?
AI: Yes, I can hear you loud and clear! How can I assist you today?

User: What's the weather in Toronto today?
AI: The weather today in Toronto is currently 22 degrees Celsius with scattered clouds. There may be some rain later.

🧠 Tech Stack

- Python + Flask
- Twilio Voice
- OpenAI GPT-3.5
- Ngrok (for tunneling)

🙋‍♂️ Author

Rani Yaqoob

