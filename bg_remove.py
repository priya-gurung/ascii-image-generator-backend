import requests
import os

API_KEY = os.getenv("REMOVE_BG_API_KEY")

def remove_bg(input_path, output_path):
    with open(input_path, "rb") as image_file:
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": image_file},
            data={"size": "auto"},
            headers={"X-Api-Key": API_KEY},
            timeout=60,
        )

    if response.status_code != 200:
        raise Exception(
            f"remove.bg API error: {response.status_code} - {response.text}"
        )

    with open(output_path, "wb") as out:
        out.write(response.content)