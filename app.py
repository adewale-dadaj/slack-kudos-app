import os
import re
from detenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# 1. Configuration Layer
load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# 2. The Storage (In-memory - volatile)
# Key = USer ID, Value = Integer (Kudos Count)
kudos_memory = {}

# 3. The Logic Layer
@app.event("message")
def handle_message(event, say):
    # Security check: ignore other bots
    if "bot_id" in event:
        return

    text = event.get("text", "")

    # Check for trigger pattern
    if "?++" in text:
        # Regex to find the <@U12345> pattern
        match = re.search(r"<@(\w+)>", text)

        if match:
            receiver_id = match.group(1)
            sender_id = event["user"]

            # Guard clause: Prevent self-kudo
            if receiver_id == sender_id:
                say(text="Nice try! You can't give yourself kudos. 😉", thread_ts=event["ts"])
                return

            # Update the Dictionary
            # .get(receiver_id, 0) checks for the user; if not found, starts at 0
            kudos_memory[receiver_id] = kudos_memory.get(receiver_id, 0) + 1
            new_total = kudos_mem[receiver_id]

            # Feedback to user
            say(
                text=f"Confirmed! <@{receiver_id}> now has *{new_total}* kudos! 🚀"
                thread_ts=event["ts"]
            )
# 4. Startup
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()