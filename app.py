from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import openai


# ✅ Use OpenAI v1+ client syntax with your API key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

SILENCE_LIMIT = 10
MAX_PROMPTS = 3

call_data = {
    "prompts_sent": 0,
    "silence_events": 0,
    "start_time": None,
    "end_time": None,
}


@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    call_data["start_time"] = datetime.now(timezone.utc)
    call_data["prompts_sent"] = 0
    call_data["silence_events"] = 0

    response = VoiceResponse()
    gather = Gather(
        input="speech", timeout=SILENCE_LIMIT, action="/check-response", method="POST"
    )
    gather.say("Welcome to the AI assistant. How can I help you today?")
    response.append(gather)
    response.redirect("/check-response")
    return str(response)


@app.route("/check-response", methods=["POST"])
def check_response():
    response = VoiceResponse()
    speech_result = request.values.get("SpeechResult", "").strip()

    if speech_result:
        print(f"\nUser said: {speech_result}")
        call_data["end_time"] = datetime.now(timezone.utc)
        log_summary(speech_result)

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly voice assistant.",
                    },
                    {"role": "user", "content": speech_result},
                ],
                max_tokens=50,
            )
            ai_response = completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error: {e}")
            ai_response = "Sorry, I had trouble processing that."

        print(f"AI responded: {ai_response}")
        response.say(ai_response)

        gather = Gather(
            input="speech",
            timeout=SILENCE_LIMIT,
            action="/check-response",
            method="POST",
        )
        gather.say("What else would you like help with?")
        response.append(gather)
        response.redirect("/check-response")
    else:
        call_data["prompts_sent"] += 1
        call_data["silence_events"] += 1

        if call_data["prompts_sent"] >= MAX_PROMPTS:
            response.say("No response detected. Ending the call.")
            call_data["end_time"] = datetime.now(timezone.utc)
            log_summary("")
            response.hangup()
        else:
            gather = Gather(
                input="speech",
                timeout=SILENCE_LIMIT,
                action="/check-response",
                method="POST",
            )
            gather.say("Still there? Please say something.")
            response.append(gather)
            response.redirect("/check-response")

    return str(response)


def log_summary(user_input):
    duration = (call_data["end_time"] - call_data["start_time"]).seconds
    print("\n=== CALL SUMMARY ===")
    print(f"Duration: {duration} seconds")
    print(f"Silence events: {call_data['silence_events']}")
    print(f"Prompts sent: {call_data['prompts_sent']}")
    print(f"User input: {user_input}")


if __name__ == "__main__":
    app.run(port=5000)
