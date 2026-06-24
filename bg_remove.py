import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("REMOVE_BG_API_KEY")


def remove_bg(input_path, output_path):
    try:
        with open(input_path, "rb") as image_file:
            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": image_file},
                data={"size": "auto"},
                headers={"X-Api-Key": API_KEY},
                timeout=60
            )

        if response.status_code == requests.codes.ok:
            with open(output_path, "wb") as out:
                out.write(response.content)
            return True

        print(f"Remove.bg failed: {response.status_code}")
        return False

    except Exception as e:
        print(f"Remove.bg error: {e}")
        return False