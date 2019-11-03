"""
Image Stitching Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to stitch two images of overlap into one image.
To this end, you need to find feature points of interest in one image, and then find
the corresponding ones in another image. After this, you can simply stitch the two images
by aligning the matched feature points.
For simplicity, the input two images are only clipped along the horizontal direction, which
means you only need to find the corresponding features in the same rows to achieve image stiching.

Do NOT modify the code provided to you.
You are allowed use APIs provided by numpy and opencv, except “cv2.findHomography()” and
APIs that have “stitch”, “Stitch”, “match” or “Match” in their names, e.g., “cv2.BFMatcher()” and
“cv2.Stitcher.create()”.
"""
import cv2
import numpy as np
import random

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    #get a copy of images to process
    left_gray = left_img
    right_gray = right_img
    #usging ORB with Brute-force Matcher for feature detection and matching
    orb_reader=cv2.ORB_create()
    key_points1, description1=orb_reader.detectAndCompute(right_gray,None)
    key_points2, description2=orb_reader.detectAndCompute(left_gray,None)
    retval=cv2.BFMatcher()
    matches = retval.knnMatch(description1,description2, k=2)
    
    #extract only the inliers of matches
    good = []
    for m,n in matches:
        if m.distance < 1.1*n.distance:
            good.append(m)
    #im=cv2.drawMatches(right_img,key_points1,left_img,key_points2,good,None)
    #cv2.imwrite('results/task2_result-lst.jpg',im)
    
    #getpoints for homography
    if len(good) > 8:
        source = np.zeros((len(matches), 2), dtype=np.float32)
        destination = np.zeros((len(matches), 2), dtype=np.float32)
       
        for i,match in enumerate(good):
          source[i, :] = key_points1[match.queryIdx].pt
          destination[i, :] = key_points2[match.trainIdx].pt
           
        # Find homography
        homography, mask = cv2.findHomography(source.reshape(-1,1,2), destination.reshape(-1,1,2), cv2.RANSAC,5.0)
    #get perstive of the image
    h,w,z = left_gray.shape
        
    result = cv2.warpPerspective(right_img,homography,(left_img.shape[1] + right_img.shape[1], left_img.shape[0]))
    #cv2.imwrite('results/task2_result-perspective.jpg',result)
    #merge images
    result[0:left_img.shape[0], 0:left_img.shape[1]] = left_img
        
    #cv2.imwrite('results/task2_result-final.jpg',dst)
    
    return result
    #raise NotImplementedError

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task2_result.jpg',result_image)


