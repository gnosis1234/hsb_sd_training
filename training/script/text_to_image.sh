export MODEL_NAME="stabilityai/stable-diffusion-2"
export TRAIN_DIR="/scratch/hong_seungbum/datasets/CoconeM_Data/HSD/onepiece/train/"
export OUTPUT_DIR="/scratch/hong_seungbum/results/stable_diffusion/sd-2_ep-100_data-gpt_v4_cosine"

CUDA_VISIBLE_DEVICES=0 nohup accelerate launch training/text_to_image/train_text_to_image.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --train_data_dir=$TRAIN_DIR \
  --use_ema \
  --resolution=512 --random_flip \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --mixed_precision="fp16" \
  --num_train_epochs=100 \
  --checkpointing_steps=-1 \
  --learning_rate=1e-05 \
  --max_grad_norm=1 \
  --lr_scheduler="cosine" --lr_warmup_steps=0 \
  --output_dir=${OUTPUT_DIR} &


    # --num_train_epochs=100 \
      # --max_train_steps=22000 \