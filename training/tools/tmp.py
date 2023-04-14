import pdb
import os 
import json 

import openai
from dotenv import load_dotenv
from colorthief import ColorThief
from googletrans import Translator

from libs.s3_utils import upload_json_string


image = ColorThief("/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/onepiece/train/A1803HS15.png") # A1712LT9.png")

dominant_color =  image.get_color(quality=1)#image.get_palette(color_count=2)

load_dotenv()

openai.api_key = os.environ.get("openai")
tranlation = "大好きなりきりシナモロール" #"オーナメントスノウワンピ" #'Ornament Snow Wanpi'

message = [
        {"role": "user", "content": "I'll tell you about a game from now on"},
        {"role": "assistant", "content": "Sure, I'm all ears. What game are you going to tell me about?"},
        {"role": "user", "content": "You’re invited to enter the world of Sanrio characters "},
        {
            "role": "assistant",
            "content": "That sounds interesting! Can you tell me more about the game? What kind of Sanrio characters are featured in the game? And how does the gameplay work?",
        },
        {
            "role": "user",
            "content": "the game could Style your clothes and room The game is could a cozy conversation with your favorite character",
        },
        {
            "role": "assistant",
            "content": "That sounds like a great way to interact with your favorite Sanrio characters! It's always fun to be able to personalize your clothes and room, and having a cozy conversation with your favorite character sounds like a great way to unwind and relax. Do you know if there are any specific tasks or challenges involved in the game, or is it more of a casual, relaxing experience? And are there any other features or modes in the game that you know of?",
        },
        {"role": "user", "content": " it more of a casual, relaxing experience"},
        {
            "role": "assistant",
            "content": "That's great to hear! It's always nice to have a casual, relaxing game to unwind with. I'm sure fans of Sanrio characters will enjoy being able to style their clothes and room, and having cozy conversations with their favorite characters. It sounds like the game could be a great way to destress and take a break from the hustle and bustle of daily life. Thanks for sharing this game with me - I'm sure many people will enjoy it!",
        },
        {
            "role": "user",
            "content": "so I will give you the name of the item and color, can you give me a description of this item?",
        },
        {"role": "assistant", "content": "Sure, I'll do my best to describe the item for you."},
        {
            "role": "user",
            "content": f"Please tell me the answer in words, not sentences.",
        },
         {"role": "assistant", "content": "Understood, I will provide a brief and concise description of the item based on the name and color you give me."},
        {
            "role": "user",
            "content": f"There are these {dominant_color} rgb values List the color in word units as an adjective. Please tell me in 50 characters or less",
        },
    ]

# オーナメントスノウワンピ

response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.7
    )

translated_text = response.choices[0].message.content# .choices[0].text.strip()

translator = Translator()
text = translator.translate(text=tranlation, src='ja', dest='en').text

print(translated_text, text)
# result = {'file_name': "good", 'text': text, 'additional_feature': "", 'ori_text': text}
# json_data = json.dumps(result)

# upload_json_string(json_data, key_name="good.json")