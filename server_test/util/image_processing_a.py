# Instax image processing
# for the exhibition in OI-Jam 
# image_processing_a.py

import cv2
import numpy as np

photo_w = 600
photo_h = 800
frame_w = 600
frame_h = 800


# img:original image img_f:frame image
def img_process(img, img_f):
    # photo data resize
    img_canvas = np.zeros((frame_h, frame_w, 3), dtype=np.uint8)
    h, w = img.shape[:-1]
    m = int((w - h * float(photo_w)/float(photo_h))/2)
    img_t = img[0 : h, m : w - m]
    img_photo = cv2.resize(img_t, dsize=(photo_w, photo_h))
    img_canvas[0:photo_h, 0:photo_w] = img_photo

    # frame
    mask =  (255 - img_f[:photo_h,:,3])/ 255
    for i in range(3):
        img_canvas[:photo_h,:,i] = img_canvas[:photo_h,:,i] * mask
        img_f[:photo_h,:,i] = img_f[:photo_h,:,i] * (1 - mask)

    

    return img_canvas + img_f[:,:,:-1]

if __name__ == "__main__":
    img = cv2.imread("./test_image/kurin1.jpg")
    img_f = cv2.imread("./frame/frame.png",-1)
    img_out = img_process(img, img_f)
    cv2.imshow("frame", img_out)
    cv2.imwrite("frame_test.png", img_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows

