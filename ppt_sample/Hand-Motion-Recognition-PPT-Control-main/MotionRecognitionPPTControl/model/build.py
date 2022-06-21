# -*- coding: utf-8 -*- 
import os
import sys
import argparse


# C:\\Users\Oseong\AppData\Local\Programs\Python\Python37\python.exe
def main(input_data_path, output_data_path):
    # comp = 'bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --action_env PYTHON_BIN_PATH="D:/anaconda/python.exe" mediapipe/examples/desktop/hand_tracking:hand_tracking_cpu'
    # 명령어 컴파일
    cmd_first = 'set GLOG_logtostderr=1'
    cmd = 'bazel-bin\mediapipe\examples\desktop\hand_tracking\hand_tracking_cpu --calculator_graph_config_file=mediapipe\graphs\hand_tracking\hand_tracking_desktop_live.pbtxt'

    # 미디어 파이프 명령어 저장listfile
    listfile = os.listdir(input_data_path)
    if not (os.path.isdir(output_data_path + "Relative/")):
        os.mkdir(output_data_path + "Relative/")
    if not (os.path.isdir(output_data_path + "Absolute/")):
        os.mkdir(output_data_path + "Absolute/")

    # print(listfile)
    for file in listfile:
        # 해당 디렉토리의 하위 디렉토리 폴더명을 찾음
        # print("file : " + file)
        if not (os.path.isdir(input_data_path + file)):  # ignore .DS_Store
            # print(input_data_path + file)
            continue

        word = file + "/"
        fullfilename = os.listdir(input_data_path + word)
        # print(fullfilename)

        # 하위디렉토리의 모든 비디오들의 이름을 저장
        if not (os.path.isdir(output_data_path + "_" + word)):
            os.mkdir(output_data_path + "_" + word)
        if not (os.path.isdir(output_data_path + "Relative/" + word)):
            os.mkdir(output_data_path + "Relative/" + word)
        if not (os.path.isdir(output_data_path + "Absolute/" + word)):
            os.mkdir(output_data_path + "Absolute/" + word)
        # os.system(comp)
        # print("comp : " + comp)

        outputfilelist = os.listdir(output_data_path + '_' + word)
        for mp4list in fullfilename:
            # print("mp4list : " + mp4list)
            if ".DS_Store" in mp4list:
                continue
            inputfilen = ' --input_video_path=' + input_data_path + word + mp4list
            outputfilen = ' --output_video_path=' + output_data_path + '_' + word + mp4list
            cmdret = cmd + inputfilen + outputfilen
            os.system(cmdret)
            print("cmdret : " + cmdret)

        print('outputlist : {0}'.format(outputfilelist))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='operating Mediapipe')
    parser.add_argument("--input_data_path", help=" ")
    parser.add_argument("--output_data_path", help=" ")
    args = parser.parse_args()
    input_data_path = args.input_data_path
    output_data_path = args.output_data_path
    # print(input_data_path)
    main(input_data_path, output_data_path)
