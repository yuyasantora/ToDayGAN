#!/bin/bash
# Test script for traffic light dataset

python test.py \
    --phase test \
    --serial_test \
    --name traffic_light_4domain \
    --dataroot ./datasets/traffic_light_4domain \
    --n_domains 4 \
    --which_epoch 150 \
    --loadSize 512 \
    --gpu_ids 0
