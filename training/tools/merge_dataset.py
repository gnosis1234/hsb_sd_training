import json
import pdb
import csv
import os 


def csv_file_read(source_file_path):
    data = []

    # CSV 파일을 읽고 딕셔너리 형태로 변환
    with open(source_file_path, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

data = csv_file_read("/scratch/hong_seungbum/datasets/CoconeM_Data/hsd.csv")

names = []
for data_dict in data:
    item_type = data_dict["filterType"]

    if item_type == "nono" or item_type != 'onepiece':
        continue

    name = data_dict["resourceId"]
 
    names.append(name)

idx = 0
root = "datasets/version4"
results = []
for filename in sorted(os.listdir(root), key=lambda x : int(x.split("_")[-1][:-5])):
    print(filename)
    with open(f"{root}/{filename}") as f:
        datas = json.load(f)
    
    for data in datas:
        # file_path = os.path.join("/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/", "onepiece", "train", names[idx] + ".png")
        # if os.path.exists(file_path):
        result =  {"file_name": data['file_name'] + ".png", "text": data['text'], "additional_feature": ""}
        results.append(result)
        # idx += 1
        
with open(
        os.path.join(f"datasets/metadata.jsonl"), "w", encoding="utf-8"
    ) as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)