# K-Water-AI-Competition
[2023 제3회 K-water AI 경진대회] 어종(魚種) 식별 및 분류 알고리즘 개발 1st solution

![K-water_project Logo](https://cdn.aifactory.space/images/20231018120320_NhMR.jpg)

## 대회 주제
낙동강 하굿둑 물고기 영상에서 농어, 베스, 숭어, 강준치, 블루길, 잉어, 붕어, 누치 8개의 어종을 식별하고 분류하는 AI 모델 개발

## 데이터 설명
- 대회에서 제공한 데이터(학습 약 100,000개 / 테스트 약 45,000개)

## 모델 접근 방식
- YOLOv8 series 적용
  - m과 x 모델 평가 후 모델의 크기가 성능에 영향을 주지 않는다는 점을 발견하여 m으로 학습 진행
- pre-trained 모델 적용
  - open images v7 dataset은 fish class를 가지고 있기 때문에, 물고기에 분류를 위한 특징을 어느정도 학습해뒀을것이라고 생각.
  - 이에 따라 해당 데이터셋으로 사전학습된 yolov8 m 모델을 사용함. 또한 pre-trained 여부가 모델의 성능이 영향을 미치는 것을 확인함. (mAP 측면에서 3 가량의 차이를 보임)
- freezing 적용
  - 사전학습된 모델의 경우 저수준 (가장자리 등)의 간단한 특징은 이미 잘 추출할 것으로 판단함.
  - 또한, freeze 하지 않았을 경우와 결과 비교 시, 모델의 성능에 큰 차이가 없음을 확인함.
  - 따라서, 앞쪽 3개의 layer에 대해 freeze를 적용하여 학습파라미터를 줄이고, 학습 시간을 빠르게 할 수 있었음  

## 모델 학습 관련 접근 방식
- 배경 이미지 모두 사용
  - foreground(객체)가 존재하는 이미지들로 학습 후 cam으로 시각화 진행.
  - 모델이 학습하지 못한 배경에 대해서도 객체를 잡는 False positive 확인.
  - 따라서, 이러한 노이즈 자체를 학습시키기 위해 배경 이미지도 모두 학습으로 사용
- Custom Cutout 적용
  - albumentations 라이브러리의 cutout 적용 시 객체 / 배경 간 구분을 힘들어하는 점을 확인.
  - 객체가 존재하는 이미지 영역에만 cutout을 적용하는 custom cutout을 작성 및 적용
- Mixup 적용
  - Yolov8 CAM 깃허브를 참조하여 모델을 시각화해본 결과, 모델이 객체를 잡는 근거로 너무 과한 특징을 잡는다는 것을 확인.
  - 이에 따라, mixup을 적용하여, 모델이 과하게 확신하는 것을 방지하고자 함.
- Label smoothing 적용
  - mixup과 마찬가지로, 모델이 과하게 확신하는 것을 방지하고자 적용.
- semi supervised 방식 적용 : 모델의 전체 학습 과정은 아래와 같음
  0. 주최측에서 제공한 참고동영상을 각 frame 별로 이미지화 (additional data로 명명)
  1. 제공받은 training data 전체를 object yolov8 m 모델로 학습함.
     - 이 때, mixup 적용함 
  2. 학습된 모델로부터 additional data를 inference
     - 결과 중 객체가 탐지 된 이미지들 및 결과를 기존 training data에 추가
  3. 새로 만들어진 training data로 모델을 학습
     - 이 때는 mixup을 제거함 : 학습 후반부에 loss Nan 발생
  4. 최종적으로 test dataset에 대해 inference 진행

## Member
| 이름       | 학년 | 전공          | 역할                          |
|------------|-----|---------------|------------------------------|
| 백근주    | 4    | 지능기전공학부 무인이동체공학전공 | Custom Cutout 개발, CAM based analysis, 수도라벨링 적용 |
| 김동영    | 4    | 지능기전공학부 무인이동체공학전공 | YOLOv8 baseline 작성, Ablation Study, Custom Blur 개발 |

## 개발 환경
- Python: 3.9.16
