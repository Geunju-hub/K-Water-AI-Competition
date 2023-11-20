import os
import shutil
import random
from tqdm.auto import tqdm
from glob import glob

random_seed = 42
random.seed(random_seed)

# 경로 설정
BASE_FOLDER = "./datasets/full"

folder_path = "./datasets"
train_folder = os.path.join(folder_path, 'train')
valid_folder = os.path.join(folder_path, 'valid')
train_images_folder = os.path.join(train_folder, 'images')
train_labels_folder = os.path.join(train_folder, 'labels')
valid_images_folder = os.path.join(valid_folder, 'images')
valid_labels_folder = os.path.join(valid_folder, 'labels')

# train 폴더 생성
os.makedirs(train_folder, exist_ok=True)
os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(train_labels_folder, exist_ok=True)

# valid 폴더 생성
os.makedirs(valid_folder, exist_ok=True)
os.makedirs(valid_images_folder, exist_ok=True)
os.makedirs(valid_labels_folder, exist_ok=True)

# 폴더 내 파일 이동
image_file_list = [file_name for file_name in os.listdir(BASE_FOLDER) if file_name.endswith('.png')]

# 리스트를 랜덤하게 섞음
random.shuffle(image_file_list)

train_ratio = 0.8
train_file_count = int(len(image_file_list) * train_ratio)

for index, file_name in tqdm(enumerate(image_file_list)):
    image_path = os.path.join(BASE_FOLDER, file_name)
    label_name = os.path.splitext(file_name)[0] + '.txt'
    label_path = os.path.join(BASE_FOLDER, label_name)

    if index < train_file_count:
        shutil.move(image_path, os.path.join(train_images_folder, file_name))
        if os.path.exists(label_path):
            shutil.move(label_path, os.path.join(train_labels_folder, label_name))
    else:
        shutil.copy(image_path, os.path.join(train_images_folder, file_name))
        shutil.move(image_path, os.path.join(valid_images_folder, file_name))
        if os.path.exists(label_path):
            shutil.copy(label_path, os.path.join(train_labels_folder, label_name))
            shutil.move(label_path, os.path.join(valid_labels_folder, label_name))
        
print(f"Train : {len(glob('./dataset/train/images/*'))} files moved")
print(f"Valid : {len(glob('./dataset/valid/images/*'))} files moved")