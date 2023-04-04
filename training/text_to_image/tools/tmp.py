import openai
from colorthief import ColorThief
from googletrans import Translator

image = ColorThief("/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/onepiece/train/A1803HS15.png") # A1712LT9.png")

dominant_color = image.get_palette(color_count=2)


openai.api_key = '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'
tranlation = "大好きなりきりシナモロール" #"オーナメントスノウワンピ" #'Ornament Snow Wanpi'

message = [{"role": 'user', "content": "I'll tell you about a game from now on"},
           {"role": 'assistant', "content": "Sure, I'm all ears. What game are you going to tell me about?"},
           {"role": 'user', "content": "You’re invited to enter the world of Sanrio characters "},
           {"role": 'assistant', "content": "That sounds interesting! Can you tell me more about the game? What kind of Sanrio characters are featured in the game? And how does the gameplay work?"},
           {"role": 'user', "content": "the game could Style your clothes and room The game is could a cozy conversation with your favorite character"},
           {"role": 'assistant', "content": "That sounds like a great way to interact with your favorite Sanrio characters! It's always fun to be able to personalize your clothes and room, and having a cozy conversation with your favorite character sounds like a great way to unwind and relax. Do you know if there are any specific tasks or challenges involved in the game, or is it more of a casual, relaxing experience? And are there any other features or modes in the game that you know of?"},
           {"role": 'user', "content": " it more of a casual, relaxing experience"},
           {"role": 'assistant', "content": "That's great to hear! It's always nice to have a casual, relaxing game to unwind with. I'm sure fans of Sanrio characters will enjoy being able to style their clothes and room, and having cozy conversations with their favorite characters. It sounds like the game could be a great way to destress and take a break from the hustle and bustle of daily life. Thanks for sharing this game with me - I'm sure many people will enjoy it!"},
           {"role": 'user', "content": "so I will give you the name of the item, can you give me a description of this item?"},
           {"role": 'assistant', "content": "Sure, I'll do my best to describe the item for you."},
           {"role": 'user', "content": f"This item is a only one-piece item, the item name is {tranlation} and the main colors are {dominant_color} in rgb color.  In deep learning, tell the picture in this tone like captionIng labeling"}]

# オーナメントスノウワンピ

response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.7
    )

translated_text = response.choices[0].message.content# .choices[0].text.strip()

translator = Translator()
text = translator.translate(text=tranlation, src='ja', dest='en').text

print(translated_text.replace(tranlation, text))