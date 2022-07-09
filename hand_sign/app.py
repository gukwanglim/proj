#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque

import cv2 as cv
import numpy as np
import mediapipe as mp
from queue import Queue
from PIL import ImageFont, ImageDraw, Image
import random


from utils import CvFpsCalc
from model import KeyPointClassifier

result = ""          #현재 결과
before_result = ""  #이전 결과
result_que = Queue(3) #result들을 저장하는 큐 생성. 현재 결과까지 최대 2개 저장
#0, 1이 입력되면 good 출력
continuous= {'이번' : ['1','2'], '발표' : ['3', '4'], '질의' : ['5', '6'], '응답과' : ['7', '8'], '요약을' : ['9', '10'], '맡은' : ['11', '12'], '담당자' : ['13', '14']  }
    
one = {'0':'저는',  '15' : '입니다'}

list_of_key = list(continuous.keys())
list_of_value = list(continuous.values())

#한글을 출력할 폰트 설정
b,g,r,a = 255,255,255,0
fontpath = "./gulim.ttc"
font = ImageFont.truetype(fontpath, 20)



def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args


def main():
    # 인수 해석 #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = True

    # 카메라 준비 ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # 모델 로드 #############################################################
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=2,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    keypoint_classifier = KeyPointClassifier()


    # 라벨 로드 ###########################################################
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]
    # vocab 생성 #######################################################
    # vocab = {keypoint_classifier_labels[0]:"", }

    # FPS측정모듈 ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len=10)

    # 좌표 이력 #################################################################
    # history_length = 16
    # point_history = deque(maxlen=history_length)

    # 핑거 제스처 이력 ################################################
    # finger_gesture_history = deque(maxlen=history_length)

    #  ########################################################################
    mode = 0
    
    # 손마리 연결 코드
    # frame_queue = Queue()
    # darknet_image_queue = Queue(maxsize=1)
    # detections_queue = Queue(maxsize=1)
    # fps_queue = Queue(maxsize=1)

    while True:
        fps = cvFpsCalc.get()

        # 키처리(ESC：종료) #################################################
        key = cv.waitKey(10)
        if key == 27:  # ESC
            break
        number, mode = select_mode(key, mode)

        # 카메라 캡쳐 #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # 미러 표시
        debug_image = copy.deepcopy(image)

        # 검출 실시 #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        #  ####################################################################
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # 외접 직사각형의 계산
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                # 랜드마크 계산
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # 상대 좌표·정규화 좌표로의 변환
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)
                # pre_processed_point_history_list = pre_process_point_history(
                #     debug_image, point_history)
                # 학습 데이터 저장
                logging_csv(number, mode, pre_processed_landmark_list)

                # 핸드사인 분류
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                
             

                # 드로잉
                debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info_text(
                    debug_image,
                    brect,
                    handedness,
                    keypoint_classifier_labels[hand_sign_id],
                )
                debug_image = drawing(debug_image,
                                      keypoint_classifier_labels[hand_sign_id],
                                     )
        else:
            pass
        # debug_image = draw_point_history(debug_image, point_history)
        debug_image = draw_info(debug_image, fps, mode, number)

        # 화면반영 #############################################################
        cv.imshow('Hand Sign Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()


def select_mode(key, mode):
    number = -1
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k
        mode = 1

    return number, mode


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # 키포인트
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # 상대 좌표로 전환
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # 1차원 목록으로 변환
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # 정규화
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def logging_csv(number, mode, landmark_list):
    if mode == 0:
        pass
    if mode == 1 and (0 <= number <= 9):
        csv_path = 'model/keypoint_classifier/keypoint.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])
        # index 랑 landmark_point 확인 #############
        # print(number,'\n',landmark_list)
  
    return


def draw_landmarks(image, landmark_point):
    # 연결선
    if len(landmark_point) > 0:
        # 엄지
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (255, 255, 255), 2)

        # 검지
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (255, 255, 255), 2)

        # 중지
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (255, 255, 255), 2)

        # 약지
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (255, 255, 255), 2)

        # 소지
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (255, 255, 255), 2)

        # 손바닥
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (255, 255, 255), 2)

    # 키포인트
    for index, landmark in enumerate(landmark_point):
        if index == 0:  # 손목1
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 1:  # 손목2
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 2:  # 엄지：뿌리
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 3:  # 엄지：제1관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 4:  # 엄지：손가락끝
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 5:  # 검지：뿌리
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 6:  # 검지：제2관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 7:  # 검지：제1관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 8:  # 검지：손가락끝
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 9:  # 중지：뿌리
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 10:  # 중지：제2관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 11:  # 중지：제1관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 12:  # 중지：손가락끝
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 13:  # 약지：뿌리
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 14:  # 약지：제 2관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 15:  # 약지：제 1관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 16:  # 약지：손가락끝
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 17:  # 소지：뿌리
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 18:  # 소지：제 2관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 19:  # 소지：제 1관절
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 20:  # 소지：손가락끝
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

    return image


def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # 외접직사각형
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 0, 0), 1)

    return image


def draw_info_text(image, brect, handedness, hand_sign_text):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                 (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:] # 오른손, 왼손 지울까?
    
    if hand_sign_text != "":
        # hand_sign_text = keypoint_classifier_labels[hand_sign_id]
        
        
        info_text = info_text + ':' + hand_sign_text
        
       
    # text 입력  
    cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
    
    
    return image

def drawing(image, hand_sign_text):
    global result_que
    global before_result
    global result
    
    random.seed(3)   
    label = ""       #detect 결과(실시간으로 detect된 이미지)
    word = ""        #최종으로 출력할 단어
    sentence=[]      #출력할 문장
    
    # result = ""          #현재 결과
    # before_result = ""  #이전 결과
    # result_que = Queue(3) #result들을 저장하는 큐 생성. 현재 결과까지 최대 3개 저장
    x,y = 200, 450
    h, w, c = image.shape
    # print('h, w :',h, w)
    # --> h, w : 720 1280
    # x = (img.shape[1] - textsize[0]) / 2
    # y = (img.shape[0] + textsize[1]) / 2
    # setup text
    font1 = cv.FONT_HERSHEY_SIMPLEX
    
    # 한글 입력을 위해서 이미지 변환
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    hand_image = Image.fromarray(image)
    draw = ImageDraw.Draw(hand_image)
    
    label = hand_sign_text
    
    if label is not None:

        #result가 null이 아닌 경우에만 before_result에 저장
        if result != "":
            before_result = result

        #디텍션 결과가 null이 아닌 경우에만 result에 저장
        if label != "":
            result = label
            

            #이전 결과와 현재 결과가 다른 경우에만 결과 큐에 저장
            if(before_result != result and result not in list(one.keys())):
                if(not result_que.full()):
                    result_que.put(result)
                    # print('!=',list(result_que.queue))

                else:
                    #큐가 가득 차있으면 원소 제거 후 삽입
                    result_que.get()
                    result_que.put(result)
                    
                    # print('full',list(result_que.queue))
            
#             print('label:', label)
#             print('one', one.get(label))
                    
 #########################################여기까지 작동###################################           


            #핵심동작 1개인 수화 출력
            if label in list(one.keys()):
            
                # 텍스트 사이즈 구하기
                textsize = cv.getTextSize(one.get(label), font1, 1, 2)[0]
               
                x_1 = int((w - textsize[0])/2)
                
                # print('1_size:',textsize[0]) # (길이, 높이) 두개의 값 반환
                # cv.putText(image, one.get(label), (x_1, int(h*0.9)), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv.LINE_AA)
                draw.text((x_1, int(h*0.8)), one.get(label), font=ImageFont.truetype('./gulim.ttc', 70), fill=(255, 200, 0))
                

                # print('one', one.get(label))
                result_que = Queue(3)

            list_of_result = list(result_que.queue)
            #큐를 리스트로 변환


            #'완쾌'와 독립적으로 '낫다' 출력
            # if 'recovery1' not in list_of_result and 'recovery2' not in list_of_result and label=='recovery3':
            #     sentence.append('낫다 ')    
            #     draw.text((x, y), "낫다", font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))


            #핵심동작 2개,3개인 수화 출력
            for i in range(len(list_of_key)):
                if list_of_result == list_of_value[i] or list_of_result[1:] == list_of_value[i]:
                    #현재까지 저장된 result들을 토대로 단어 생성
                    word = list_of_key[i]
                    #출력할 문장에 최종 단어 추가
                    
                    #텍스트 사이즈 구하기
                    textsize = cv.getTextSize(word, font1, 1, 2)[0]
                    
                    # 텍스트 중앙으로 오게하는 x 좌표 계산
                    x_2 = int((w - textsize[0])/2)
                                        
                    # cv.putText(image, word, (x_2,int(h*0.9)), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv.LINE_AA)
                    draw.text((x_2, int(h*0.8)), word, font=ImageFont.truetype('./gulim.ttc', 70), fill=(255,200,0))
                    break              
    
    image = np.array(hand_image)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    return image



# -----------------draw_info_text 원본---------------------------------------------------

# def draw_info_text(image, brect, handedness, hand_sign_text):
#     cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
#                  (0, 0, 0), -1)

#     info_text = handedness.classification[0].label[0:]
#     if hand_sign_text != "":
#         info_text = info_text + ':' + hand_sign_text
#     cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
#                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)


#     return image
#---------------------------------------------------------------------------------------

def draw_info(image, fps, mode, number):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
               1.0, (0, 0, 0), 4, cv.LINE_AA)
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
               1.0, (255, 255, 255), 2, cv.LINE_AA)

    mode_string = ['Logging Key Point']
    if 1 <= mode <= 2:
        cv.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                   cv.LINE_AA)
        if 0 <= number <= 9:
            cv.putText(image, "NUM:" + str(number), (10, 110),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                       cv.LINE_AA)
    return image


if __name__ == '__main__':
    main()
