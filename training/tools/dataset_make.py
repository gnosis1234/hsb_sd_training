import argparse
import csv
import json
import os
import pdb
import sys
import time

import backoff
import openai
from colorthief import ColorThief
from dotenv import load_dotenv
from googletrans import Translator
from libs.s3_utils import upload_json_string
from openai.error import RateLimitError
from tqdm import tqdm
from training.tools.split_merge_text import chunk_text_byte, wrap_text, unwrap_text


def csv_file_read(source_file_path):
    data = []

    # CSV 파일을 읽고 딕셔너리 형태로 변환
    with open(source_file_path, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def translate_func(texts):
    translator = Translator()

    translation = ""
    for splitted_text in chunk_text_byte(wrap_text(texts)):
        translation += translator.translate(text=splitted_text, src="ja", dest="en").text + "\n"

    return translation


@backoff.on_exception(backoff.expo, RateLimitError)
def turn_natural_sentence(text, image, item_type, translated_text):
    image = ColorThief(f"/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/onepiece/train/{image}")
    dominant_color = image.get_color(quality=1)

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
            "content": "so I will give you the name of the item, can you give me a description of this item?",
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

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.7,
    )
    chatgpt_text = response.choices[0].message.content
    
    # chatgpt_text = chatgpt_text.replace(f'Based on the RGB values you provided and the name "{text}"', "")
    # print(text, translated_text)
    return f"{translated_text} {item_type}. {chatgpt_text.replace(text, translated_text)}"


if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.environ.get("openai")
    translator = Translator()
    # Argument parser 생성
    parser = argparse.ArgumentParser(description="Copy a file to a specified location.")

    # 파라미터 추가
    parser.add_argument("start_idx", type=int, help="dataset start idx", default=0)
    parser.add_argument(
        "--source",
        type=str,
        help="Path of the source file",
        default="/scratch/hong_seungbum/datasets/CoconeM_Data/hsd.csv",
    )
    parser.add_argument("--destination", type=str, help="Path of the destination file", default="datasets/version4")
    parser.add_argument("--use_nogpt", action='store_false')
    parser.add_argument("--item-type", type=str, help="Cocone M dataset itemType", default="onepiece")

    # 파라미터를 분석
    args = parser.parse_args()
    dataset_path = "/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/"

    if not os.path.exists(args.destination):
        os.makedirs(args.destination, exist_ok=True)

    data = csv_file_read(args.source)

    texts = []
    names = []
    for data_dict in data:
        item_type = data_dict["filterType"]

        if item_type == "nono" or item_type != args.item_type:
            continue

        name = data_dict["resourceId"]
        text = data_dict["name"]

        texts.append(text)
        names.append(name)

    translation = translate_func(texts)

    results = []
    start_idx = int(args.start_idx)
    print(start_idx)
    print(len(texts))


    n_idx = 50
    print(args.use_nogpt)
    # for idx, translated_text in enumerate(tqdm(result_data)):
    start = start_idx * n_idx
    end = (start_idx + 1) * n_idx if len(texts) > (start_idx + 1) * n_idx else len(texts)
    translated_texts = unwrap_text(translation[:-1])[start:end]
    japan_texts = texts[start:end]
    for idx, (translated_text, japan_text) in enumerate(zip(translated_texts, japan_texts)):
        filename = f"{names[start + idx]}.png"
        file_path = os.path.join(dataset_path, args.item_type, "train", filename)
        if os.path.exists(file_path):
            result_text = translated_text
            if args.use_nogpt:
                result_text = turn_natural_sentence(text=japan_text, image=filename, item_type=args.item_type, translated_text=translated_text)

            result = {"file_name": filename, "text": result_text, "additional_feature": "", "ori_text": japan_text, "google": translated_text}
            results.append(result)
        # else:
        #     time.sleep(1)

    with open(
        os.path.join(args.destination, f"hsd_{args.item_type}_{start_idx}.json"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)
    json_data = json.dumps(results)
    upload_json_string(json_data, key_name=f"hsd_{args.item_type}_{start_idx}.json")
