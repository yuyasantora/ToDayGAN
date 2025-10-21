#!/bin/bash
# Training script for traffic light dataset (4 domains: sd, rd, sn, rn)
# Domains: 0=Sunny Day, 1=Rainy Day, 2=Sunny Night, 3=Rainy Night

python train.py \
    --dataroot ./datasets/traffic_light_4domain \
    --name traffic_light_4domain \
    --n_domains 4 \
    --niter 75 \
    --niter_decay 75 \
    --loadSize 512 \
    --fineSize 384 \
    --display_id 0 \
    --gpu_ids 0
