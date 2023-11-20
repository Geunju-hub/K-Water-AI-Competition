import os
import shutil
import natsort
import random
from tqdm.auto import tqdm
from glob import glob

random_seed = 42
random.seed(random_seed)

# 경로 설정
folder_path = "./datasets/additional_data/labels"
move_images_folder = './datasets/train/labels'

txt_files = glob("./ultralytics/run/base/labels/*")
for txt_file in txt_files:
    shutil.copy(txt_file, os.path.join(folder_path, txt_file.split('/')[-1]))

# 폴더 내 파일 이동
label_file_list = [file_name for file_name in os.listdir(folder_path) if file_name.endswith('.txt')]

print(len(label_file_list))

for index, label_name in tqdm(enumerate(label_file_list)):
    label_path = os.path.join(folder_path, label_name)
    image_path = os.path.join(folder_path.replace('labels','images'), label_name.replace('txt','png'))
    shutil.move(label_path, os.path.join(move_images_folder, label_name))
    shutil.move(image_path, os.path.join(move_images_folder.replace('labels','images'), label_name.replace('txt','png')))
