import os
import climage
import random
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv(".env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
text_model = genai.GenerativeModel("gemini-1.5-pro-latest")
vision_model = genai.GenerativeModel("gemini-1.0-pro-vision-latest")


def print_image(image_path: str):
    output = climage.convert(image_path)
    print(output)


def list_models():
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)


def run_single_text_query():
    prompt = input("user: ")
    response = text_model.generate_content(prompt)
    print("model: ", response.text)


def run_single_image_query():
    image_path = "./images/dado_2.jpg"
    img = Image.open(image_path)
    print_image(image_path)
    response = vision_model.generate_content(["Diga qual foi o valor da jogada", img])
    print("model: ", response.text)


def start_chat():
    prompt = ""
    chat = text_model.start_chat(history=[])

    while prompt != "quit":
        prompt = input("user: ")
        if prompt == "jogar dado":
            run_single_image_query()
        else:
            response = chat.send_message(prompt, stream=True)
            print("model: ")
            for chunk in response:
                print(chunk.text, end="")
        print("\n")


if __name__ == "__main__":
    # list_models()
    # run_single_text_query()
    # run_single_image_query()
    start_chat()
