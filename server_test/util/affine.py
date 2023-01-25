# coding:utf-8
# Affine Transform / affine2.py

import cv2
import numpy as np

def affine_transform(img,pts1,pts2):
    if len(img.shape) == 2: rows,cols = img.shape
    if len(img.shape) == 3: rows,cols,ch = img.shape
    M = cv2.getAffineTransform(pts1,pts2)
    #print 'affine matrix = ',M
    dst = cv2.warpAffine(img,M,(cols,rows))

    return dst

def cutting(img,pts1,pts2):
    x = np.linalg.norm(pts2[1]-pts2[0])			# norm x
    y = np.linalg.norm(pts2[2]-pts2[1])			# norm y

    dst = affine_transform(img,pts1,pts2)
    out = dst[0:int(y),0:int(x)]

    return out

def rotate(img):
    h,w,c = np.shape(img)
    img_t = np.zeros((w,w,c)).astype(np.uint8)
    img_t[0:h,0:w,:] = img[:,:,:]

    pts1 = np.float32([[0,h],[0,0],[w,0]]) #[x1,y1],[x2,y2],[x3,y3]
    pts2 = np.float32([[0,0],[h,0],[h,w]]) #[x1,y1],[x2,y2],[x3,y3]
    out = cutting(img_t,pts1,pts2)
    
    return out 

def expand(img):
    h,w,c = np.shape(img)
    h_instax = 800
    w_instax = 600

    pts1 = np.float32([[w,0],[0,0],[0,h]])           #[x1,y1],[x2,y2],[x3,y3]
    pts2 = np.float32([[w_instax,0],[0,0],[0,h_instax]])    #[x1,y1],[x2,y2],[x3,y3]
    
    if h> h_instax: hs =h
    else: hs =  h_instax
    
    if w>w_instax: ws =w
    else: ws = w_instax

    img_t = np.zeros((hs,ws,3)).astype(np.uint8)
    img_t[0:h,0:w,:] = img[:,:,:]
    out = cutting(img_t,pts1,pts2)

    return out

def padding(img): #Full image with frame
    h,w,c = np.shape(img)
    if w>h:
         img = rotate(img)

    h,w,c = np.shape(img)
   
    if 3*h/4>w:
        img_t = 255*np.ones((int(h),int(3*h/4),3))
        offset = np.abs(int((3*h/4 - w)/2))
        img_t[0:h,offset:offset+w,:] = img[:,:,:]  
    else:
        img_t = 255*np.ones((4*w/3,w,3))
        offset = np.abs((4*w/3 - h)/2)
        img_t[offset:offset+h,0:w,:] = img[:,:,:]
 
    return img_t

def padding2(img): #Partial image without frame
    h,w,c = np.shape(img)
    if w>h:
         img = rotate(img)

    h,w,c = np.shape(img)
   
    if 3*h/4>w:
        img_t = 255*np.ones((int(4*w/3),int(w),3))
        offset = np.abs(int((h - 4*w/3)/2))
        img_t[:,:,:] = img[offset:offset+int(4*w/3),0:w,:]  
    else:
        img_t = 255*np.ones((int(h),int(3*h/4), 3))
        offset = np.abs(int((w - 3*h/4)/2))
        img_t[:,:,:] = img[0:h,offset:int(offset+3*h/4),:]
 
    return img_t

def processing(img):
    img = padding2(img) #Partial image without frame
    img = expand(img)

    #plt.imshow(img)
    #plt.show()

    return img

if __name__=='__main__':
    import matplotlib.pyplot as plt    
    from PIL import Image

    img = np.array(Image.open('kurin_n_SQ.jpg'))
    plt.imshow(img)
    plt.show()

    img = processing(img)

    plt.imshow(img)
    plt.show()

    img = Image.fromarray(np.uint8(img))
    img.save("image.jpg")
