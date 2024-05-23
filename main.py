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
character_attributes = {
    "INT": 9,
    "STR": 7,
    "DEF": 5,
    "LUC": 1,
    "AGI": 6,
    "WIS": 2,
    "CON": 4,
    "CHA": 0,
    "DEX": 2,
}

base_prompt = """Vamos jogar uma partida de RPG. Você será o mestre de uma historia deverá ser baseada em uma aventura de busca ao tesouro na grécia antiga, onde elementos da mitologia grega deverão ser inseridas no desenrolar da historia. As principais regras do jogo são:

1- O jogador não pode escolher uma ação diferente das fornecidas pelo mestre.
2- A partida deve ter bastante iterações, cenas de ação e testes para o jogador

O personagem será um professor de história brasileiro, mal humorado e azarado que teve um problema com seu voo voltando do Japão para o Brasil e precisou fazer uma parada forçada na Grécia enquanto manifestações tomam as ruas do país. O professor não é uma pessoa muito sociável, mas se envolve com outras personagens que tentam desvendar as reviravoltas da história. Os atributos do personagem são os seguintes: 
"""
base_prompt = base_prompt + str(character_attributes)


def print_image(image_path: str):
    output = climage.convert(image_path)
    print(output)


def roll_dice():
    image_file_name_list = os.listdir("./images")
    image_file_name = random.choice(image_file_name_list)
    print(image_file_name)
    return image_file_name


def run_single_image_query(image_path: str):
    img = Image.open(image_path)
    response = vision_model.generate_content(["Diga qual foi o valor da jogada", img])
    print("model: ", response.text)


def start_chat():
    prompt = ""
    chat = text_model.start_chat(history=[])
    response = chat.send_message(
        base_prompt
        + "\nGere um resumo empolgante para o inicio de uma partida com as intruções anteriores"
    )
    print(response.text)

    while prompt != "quit":
        prompt = input("jogador: ")
        if prompt == "jogar dado":
            image_path = roll_dice()
            print_image(image_path)
            img = Image.open(image_path)
            response = vision_model.generate_content(
                ["Diga qual foi o valor da jogada", img]
            )
            print("mestre: ", response.text)
        else:
            response = chat.send_message(prompt)
            for chunk in response:
                print(chunk.text, end="")
        print("\n")


if __name__ == "__main__":
    start_chat()
