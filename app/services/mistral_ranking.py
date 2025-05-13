import json
from mistralai import Mistral
import os

API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-large-latest"

def get_top_response_ids(responses: list) -> list:
    client = Mistral(api_key=API_KEY)
 
    prompt = (
    "You are given a list of freight responses in JSON. Each response has a unique 'id'.\n\n"
    "Rank the responses based on:\n"
    "1. Lowest price\n"
    "2. Earliest delivery_date\n\n"
    "Both criteria are equally important.\n"
    "Return only the top 5 IDs in ranked order (ascending, top 3 on top), as a plain array like: [2, 5, 1, 3, 4]\n"
    "Do not explain. Do not include anything else.\n\n"
    f"List:\n{json.dumps(responses, indent=2)}"
)


    response = client.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_output = response.choices[0].message.content.strip()
    print("\n🧠 Raw Mistral Output:\n", raw_output)

    try:
        return json.loads(raw_output)
    except Exception as e:
        print("❌ Failed to parse Mistral response:", e)
        return []

    
def get_full_responses_by_ids(top_ids: list, all_responses: list) -> list:
    id_to_response = {r["id"]: r for r in all_responses}
    return [id_to_response[i] for i in top_ids if i in id_to_response]
