import os
import shutil
import random

# ===== BASE DIRECTORY =====
base_dir = os.getcwd()   # your main folder

# ===== CLASSES =====
classes = ["cleaning", "cooking", "cutting", "washing", "theft"]

# ===== OUTPUT DATASET =====
output_dir = os.path.join(base_dir, "dataset")

# ===== SPLIT RATIO =====
split_ratio = 0.8  # 80% train

# ===== CREATE TRAIN + VAL FOLDERS =====
for split in ["train", "val"]:
    for cls in classes:
        path = os.path.join(output_dir, split, cls)
        os.makedirs(path, exist_ok=True)

# ===== PROCESS EACH CLASS =====
for cls in classes:
    class_path = os.path.join(base_dir, cls)

    images = os.listdir(class_path)

    # Shuffle images randomly
    random.shuffle(images)

    split_index = int(len(images) * split_ratio)

    train_images = images[:split_index]
    val_images = images[split_index:]

    # Copy train images
    for img in train_images:
        src = os.path.join(class_path, img)
        dst = os.path.join(output_dir, "train", cls, img)
        shutil.copy(src, dst)

    # Copy val images
    for img in val_images:
        src = os.path.join(class_path, img)
        dst = os.path.join(output_dir, "val", cls, img)
        shutil.copy(src, dst)

    print(f"{cls}: {len(train_images)} train, {len(val_images)} val")

print("✅ Dataset split completed!")