import sys
import numpy as np
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = # sample r'C:\Program Files\Tesseract-OCR\tesseract'
crop_position = [620,720,270,865] # change your source subtitles area
#crop_position = [815,890,370,1150] 記事に掲載したときのサイズ
white_threshold = 210 # subtitles color

def detect(img):
    img = img[crop_position[0] : crop_position[1], crop_position[2] : crop_position[3]]
    crop_size = img.shape[0] * img.shape[1]

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, img_th = cv2.threshold(img_gray, white_threshold, 255, cv2.THRESH_OTSU)

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_th)

    if nlabels > 1:
        median = np.median(stats[:,4])
       
        for idx in range(1, nlabels):

            if( stats[idx][4] >= median * 2 ): # not average size
                img_th[labels == idx, ] = 0

            elif( stats[idx][4] < 5 ): # too small
                img_th[labels == idx, ] = 0

            elif( (stats[idx][4] / crop_size) > 0.25): # too big
                img_th[labels == idx, ] = 0

            else:
                pass

    text = pytesseract.image_to_string(img_th, lang='spa')

    return img_th, text

def save(result_list, path):

    with open(path, "w", encoding = "utf-8") as file:
        for line in result_list:
            file.write(line + "\n")
        print("save file " + path)

def img(filename, save_file):
    img = cv2.imread(filename)

    img_result, text = detect(img)

    print('Texto: ', text)
    cv2.imshow('Resultado', img_result)
    save([text], save_file)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def video(filename, save_file):
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    skip_second = 1
    result_list = [""]
    print(fps *skip_second)
    cnt = 0
    while (cap.isOpened()):

        ret, frame = cap.read()

        if not ret:
            break
        
        if (cnt == int(fps * skip_second)):
            img_result, text = detect(frame)

            cv2.imshow('Resultado', img_result)

            if result_list[-1] != text:
                print('Texto: ',text)
                result_list.append(text)
            
            cnt = 0

        cnt = cnt + 1

        k = cv2.waitKey(1)
        if k in [27, ord('q')]:
            break

    save(result_list, save_file)
    cap.release()
    cv2.destroyAllWindows()

#command example
#python tesseract_subtitles_detection.py image ./data/sample.png ./result/test.txt
#python tesseract_subtitles_detection.py video ./data/sample.mp4 ./result/test.txt
if __name__ == '__main__':
    mode = sys.argv[1]
    source_file = sys.argv[2]
    save_file = sys.argv[3]

    if(mode == "video"):
        video(source_file, save_file)
    elif(mode == "image"):
        img(source_file, save_file)
    else:
        print("Command arguments mismatch." + mode +" must change video or image")