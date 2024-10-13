from utils import llm_utils
from prompts import WORKOUT_LOG_PROMPT

workout_plan = """
Warm-up:
Warm-up 🏎️ Plyometrics      Jump rope               1 min
Warm-up 🦊 Coordination W   Shadow boxing + 30 kicks (e)  20x 

🏋🏻 Technical    1A      Hang clean               3 x 4
🦍 Absolute strength 2A Front Squat              3 x 5
🏎️ Plyometrics   2B      Lunge jumps             3 x 6

🦾 Accessory     3A      Nordics                 3 x 6
🦾 Accessory     3B      Bulgarian split squat   3 x 12

🧘🏻 Flexibility  4A      Horse stance            3 x 45s
🧘🏻 Flexibility  4B      Side kicks              30x
"""

def handle_log(message):
    prompt = WORKOUT_LOG_PROMPT + message
    prompt = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]
    response = llm_utils.run_llm(prompt, "gpt-4o", json_format=True)
    return str(llm_utils.extract_json_from_response(response))

def handle_workout():
    prompt = "This is a user's workout plan. Please pretty the format so it is presentable over a text message."
    prompt += workout_plan
    prompt = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": ""}
    ]
    response = llm_utils.run_llm(prompt, "gpt-4o", json_format=False)
    return response
