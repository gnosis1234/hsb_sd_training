import pdb

from diffusers import DiffusionPipeline, UNet2DConditionModel, StableDiffusionPipeline
from transformers import CLIPTextModel
from PIL import Image
import torch
import numpy as np

root = "/scratch/hong_seungbum/results/stable_diffusion"

model_path = "sd-2_ep-100_data-gpt_v4" 
# model_path = "sd_1_4"
# Use the Euler scheduler here instead
unet = UNet2DConditionModel.from_pretrained(f"{root}/{model_path}/checkpoint-29199/unet", torch_dtype=torch.float16, safety_checker = None)

# if you have trained with `--args.train_text_encoder` make sure to also load the text encoder
# text_encoder = CLIPTextModel.from_pretrained(f"{root}/{model_path}/checkpoint-22000/text_encoder")


pipe = StableDiffusionPipeline.from_pretrained(f"{root}/{model_path}", unet=unet,torch_dtype=torch.float16, safety_checker = None)
pipe.to("cuda")

# prompt = "Flower shop's embroidery dress. The dress features a delicate color scheme with soft shades of pink, purple, and gray, evoking a sense of whimsy and romance. The dress is perfect for a relaxed, bohemian look and is sure to turn heads with its unique design."
prompt = "real trend floral woman dress"
images = pipe(num_inference_steps=50, prompt=prompt).images


for idx, image in enumerate(images):
    image.save(f"test{idx}_{model_path}.png") 
