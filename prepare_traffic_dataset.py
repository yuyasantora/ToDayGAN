#!/usr/bin/env python3
"""
Script to organize traffic light dataset for ToDayGAN training
Splits images by domain (sd, rd, sn, rn) and train/test
"""

import os
import shutil
from glob import glob
import random

# Configuration
SOURCE_DIR = '/home/yuya/デスクトップ/KG/traffic_light_autoware/images'
DEST_DIR = '/home/yuya/デスクトップ/KG/ToDayGAN/datasets/traffic_light_4domain'
TRAIN_RATIO = 0.8  # 80% for training, 20% for testing

# Domain mapping
# 0: sd (Sunny Day), 1: rd (Rainy Day), 2: sn (Sunny Night), 3: rn (Rainy Night)
DOMAINS = {
    'sd': 0,
    'rd': 1,
    'sn': 2,
    'rn': 3
}

def get_domain_from_filename(filename):
    """Extract domain type from filename"""
    parts = filename.split('_')
    if len(parts) >= 3:
        domain_key = parts[2]
        return DOMAINS.get(domain_key, None)
    return None

def main():
    print("Organizing traffic light dataset for ToDayGAN...")

    # Get all images
    all_images = glob(os.path.join(SOURCE_DIR, '*.jpg'))
    print(f"Found {len(all_images)} total images")

    # Group images by domain
    images_by_domain = {0: [], 1: [], 2: [], 3: []}

    for img_path in all_images:
        filename = os.path.basename(img_path)
        domain = get_domain_from_filename(filename)

        if domain is not None:
            images_by_domain[domain].append(img_path)

    # Print statistics
    domain_names = {0: 'sd (Sunny Day)', 1: 'rd (Rainy Day)',
                   2: 'sn (Sunny Night)', 3: 'rn (Rainy Night)'}
    for domain_id, images in images_by_domain.items():
        print(f"Domain {domain_id} ({domain_names[domain_id]}): {len(images)} images")

    # Split and copy images
    for domain_id, images in images_by_domain.items():
        # Shuffle images
        random.seed(42)  # For reproducibility
        random.shuffle(images)

        # Calculate split point
        split_idx = int(len(images) * TRAIN_RATIO)
        train_images = images[:split_idx]
        test_images = images[split_idx:]

        print(f"\nDomain {domain_id}: {len(train_images)} train, {len(test_images)} test")

        # Copy training images
        train_dir = os.path.join(DEST_DIR, f'train{domain_id}')
        for img_path in train_images:
            shutil.copy2(img_path, train_dir)

        # Copy test images
        test_dir = os.path.join(DEST_DIR, f'test{domain_id}')
        for img_path in test_images:
            shutil.copy2(img_path, test_dir)

    print("\nDataset preparation complete!")
    print(f"Dataset location: {DEST_DIR}")
    print("\nFolder structure:")
    print("  train0/ - Sunny Day (training)")
    print("  train1/ - Rainy Day (training)")
    print("  train2/ - Sunny Night (training)")
    print("  train3/ - Rainy Night (training)")
    print("  test0/  - Sunny Day (testing)")
    print("  test1/  - Rainy Day (testing)")
    print("  test2/  - Sunny Night (testing)")
    print("  test3/  - Rainy Night (testing)")

if __name__ == '__main__':
    main()
