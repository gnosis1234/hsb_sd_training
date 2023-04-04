import pdb

from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler, PNDMScheduler
from PIL import Image
import torch
import numpy as np

root = "/scratch/hong_seungbum/results/stable_diffusion"

model_path = "stable-diffusion-2" 
# model_path = "sd_1_4"
# Use the Euler scheduler here instead

pipe = StableDiffusionPipeline.from_pretrained(f"{root}/{model_path}", torch_dtype=torch.float16, safety_checker = None)
pipe.to("cuda")

# prompt = "Flower shop's embroidery dress. The dress features a delicate color scheme with soft shades of pink, purple, and gray, evoking a sense of whimsy and romance. The dress is perfect for a relaxed, bohemian look and is sure to turn heads with its unique design."
prompt = "item name is Sky Blue Matsuri Yukata, backgorund color is black"
images = pipe(num_inference_steps=50, prompt=prompt).images


for idx, image in enumerate(images):
    image.save(f"test{idx}_{model_path}.png") 
