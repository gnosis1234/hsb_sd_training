import pdb 

import argparse
import csv
import json
import os
import time
import multiprocessing

from tqdm import tqdm
from googletrans import Translator
import openai
from openai.error import RateLimitError
import backoff
from colorthief import ColorThief

from split_merge_text import wrap_text, unwrap_text, chunk_text_byte

def csv_file_read(source_file_path):
    data = []

    # CSV 파일을 읽고 딕셔너리 형태로 변환
    with open(source_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data 

def translate_func(texts):
    translator = Translator()
    
    translation = ''
    for splitted_text in chunk_text_byte(wrap_text(texts)):
        translation += translator.translate(text=splitted_text, src='ja', dest='en').text + '\n'
    
    return translation

@backoff.on_exception(backoff.expo, RateLimitError)
def turn_natural_sentence(text, image):
    image = ColorThief(f"/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/onepiece/train/{image}")
    dominant_color = image.get_palette(color_count=2)
    
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
           {"role": 'user', "content": f"This item is a only one-piece item, the item name is {text} and the main colors are {dominant_color} in rgb color.  In deep learning, tell the picture in this tone like captionIng labeling"}]
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=0.7,
            )
    chatgpt_text = response.choices[0].message.content
    
    translator = Translator()
    translation = translator.translate(text=text, src='ja', dest='en').text
    

    return chatgpt_text.replace(text, translation)
  
if __name__ == '__main__':
    openai.api_key = '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'
    
    # Argument parser 생성
    parser = argparse.ArgumentParser(description='Copy a file to a specified location.')
    
    # 파라미터 추가
    parser.add_argument('--source', type=str, help='Path of the source file', default='/scratch/hong_seungbum/datasets/CoconeM_Data/hsd.csv')
    parser.add_argument('--destination', type=str, help='Path of the destination file', default='./')
    parser.add_argument('--item-type', type=str, help='Cocone M dataset itemType', default='onepiece')
    
    # 파라미터를 분석
    args = parser.parse_args()
    dataset_path = '/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/'
    
    if not os.path.exists(args.destination):
        os.makedirs(args.destination, exist_ok=True)
        
    
    data = csv_file_read(args.source)
    
    texts = []
    names = []
    for data_dict in data:
        item_type = data_dict['filterType']
        
        if item_type == 'nono' or item_type != args.item_type: continue

        name = data_dict['resourceId']
        text = data_dict['name']
        
        texts.append(text)
        names.append(name)
            
    # translation = translate_func(texts)
    
    
    results = []
    total_100 = 100
    print(len(texts))
    # result_data = unwrap_text(translation[:-1])[0:total_100]
    # for idx, translated_text in enumerate(tqdm(result_data)):
    for idx, text in enumerate(tqdm(texts[400:500])):

        filename = f"{names[idx]}.png"
        file_path = os.path.join(dataset_path, args.item_type, 'train', filename)
        if os.path.exists(file_path):
            translated_text = turn_natural_sentence(text=text, image=filename)

            result = {'file_name': filename, 'text': translated_text, 'additional_feature': "", 'ori_text': text}
            results.append(result)
        
    with open(os.path.join(args.destination, f'hsd_{args.item_type}_4.json'), 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

