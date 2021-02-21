import cv2
import numpy as np
import os
import onnxruntime as rt


def RunInference(img):
    # Prepare the img for the model
    img = cv2.resize(img, (227, 227))
    img = np.moveaxis(img, -1,0)
    img = img[np.newaxis,:,:,:]

    # Run inference
    sess = rt.InferenceSession("src/website/ml/model.onnx")
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    pred = sess.run([label_name], {input_name: img.astype(np.float32)})[0]

    # Determine score
    classes = ['fresh', 'rotten']
    pred_class = classes[np.argmax(pred)]
    pred_score = pred[0][np.argmax(pred)]

    return pred_class, pred_score

def GetNannerMask(img):
    # Lab image color segmentation
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB) #tranform it to LAB
    lab_norm = cv2.normalize(lab_img[..., 1], dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    canny_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    lab_canny = cv2.Canny(lab_norm, 5, 100)
    lab_canny = cv2.dilate(lab_canny, canny_kernel)
    #lab_canny = cv2.morphologyEx(lab_canny, cv2.MORPH_CLOSE, canny_kernel)

    contours, hierarchy = cv2.findContours(lab_canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    canny_fill = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(canny_fill, [max(contours, key = cv2.contourArea)], -1, (255, 255, 255), thickness=-1)

    # Draw results
    #cv2.imshow('canny outline', canny_fill)
    #cv2.imshow('lab', lab_norm)

    return cv2.cvtColor(canny_fill, cv2.COLOR_BGR2GRAY)

def FTSaliency(img):
    # Frequency-tuned Salient Region Detection
    mean = np.mean(img, axis=2)
    mean = np.stack((mean,)*3, axis=-1)
    blur = cv2.GaussianBlur(img, (5,5), 0)

    dist = np.sum((mean-blur)**2, axis=2)
    dist = cv2.normalize(dist, dst=None, alpha=0, beta=255,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Otsu's thresholding
    thresh = cv2.threshold(dist.astype("uint8"), 0, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Segment image mask
    kernel = np.ones((5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Draw results
    #cv2.imshow('otsu', 255*thresh)
    #cv2.imshow('dist', dist)
    #cv2.imshow('masked', np.stack((thresh,)*3, axis=-1)*img)

    return 255*thresh

def bananalyze(img):
    # Calculate the ratio of spots on the nanner
    yellow_mask = FTSaliency(img)
    total_mask = GetNannerMask(img)

    color_score = np.sum(yellow_mask) / np.sum(total_mask)

    #cv2.imshow('orig', img)
    #cv2.imshow('yellow_mask', yellow_mask)
    #cv2.imshow('total_mask', total_mask)
    #cv2.waitKey(0)

    # Image classification
    classification, class_score = RunInference(img)
    #print('classification: ', classification)
    #print('class_score: ', class_score)

    # Determine score
    if classification is 'fresh':
        score = np.sqrt(1 - (1 / (7*color_score + 1)))
    else:
        score = color_score

    return score


if __name__ == "__main__":
    folder = 'C:/Users/remma/Downloads/archive/dataset/test/combined/'
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            #image = cv2.imread('C:/Users/remma/repos/FruitParty/src/website/banana.jpg')
            #image = cv2.imread('C:/Users/remma/Downloads/archive/dataset/train/rottenbanana/rotated_by_30_Screen Shot 2018-06-12 at 9.10.41 PM.png')
            #img = cv2.resize(image, (600, 800))

            score = bananalyze(img)

            #print('pickin_score: ', score)
