# parsing video to image by frame
import cv2
import os
from tqdm import tqdm

from glob import glob


video_list = sorted(glob('./2023_AI_Competition/' + '**/*.mp4'))

save_path = './datasets/additional_data'
os.mkdir(save_path)

def save_capture(i, idx):
    video = cv2.VideoCapture(i)
    
    if not video.isOpened():
        print("Could not Open :", i)
        exit(0)
    
    #불러온 비디오 파일의 정보 출력
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    
    count = 0

    while(video.isOpened()):
        ret, image = video.read()
        if(int(video.get(1)) % 10 == 0) and ret: #앞서 불러온 fps 값을 사용하여 1초마다 추출
            cv2.imwrite(save_path + '/' + str(idx) + "_frame%d.png" % count, image)
            #print('Saved frame number :', str(int(video.get(1))))
            count += 1
        if not ret:  
            break
        
    video.release()

idx = 0
for i in tqdm(video_list):
    save_capture(i, idx)
    idx +=1
    
print('finished')