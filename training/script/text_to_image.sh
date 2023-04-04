export MODEL_NAME="stabilityai/stable-diffusion-2"
export TRAIN_DIR="/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/onepiece/train"
export OUTPUT_DIR="/scratch/hong_seungbum/results/stable-diffusion-2"

CUDA_VISIBLE_DEVICES=1 accelerate launch text_to_image/train_text_to_image.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --train_data_dir=$TRAIN_DIR \
  --use_ema \
  --resolution=512 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --mixed_precision="fp16" \
  --max_train_steps=20000 \
  --learning_rate=1e-05 \
  --max_grad_norm=1 \
  --lr_scheduler="constant" --lr_warmup_steps=0 \
  --output_dir=${OUTPUT_DIR}