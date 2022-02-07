import cv2
import numpy as np
import math

def perp(a ) :
     b = np.empty_like(a)
     b[0] = -a[1]
     b[1] = a[0]
     return b

 # line segment a given by endpoints a1, a2
 # line segment b given by endpoints b1, b2
 # return
 
def movingAverage(avg, new_sample, N=15):
     if (avg == 0):
         return new_sample
     avg -= avg / N;
     avg += new_sample / N;
     return avg

def seg_intersect(a1,a2, b1,b2):
     da = a2-a1
     db = b2-b1
     dp = a1-b1
     dap = perp(da)
     denom = np.dot( dap, db)
     num = np.dot( dap, dp )
     return (num / denom.astype(float))*db + b1

def perspective_transform(image, corners, debug=False, xoffset=0):
    
     height, width = image.shape[0:2]
     output_size = height/2
     
     new_top_left=np.array([corners[0,0],0])
     new_top_right=np.array([corners[3,0],0])
     offset=[xoffset,0]    
     img_size = (image.shape[1], image.shape[0])
     src = np.float32([corners[0],corners[1],corners[2],corners[3]])
     dst = np.float32([corners[0]+offset,new_top_left+offset,new_top_right-offset ,corners[3]-offset]) 
    
     M = cv2.getPerspectiveTransform(src, dst)

     warped = cv2.warpPerspective(image, M, (width, height), flags=cv2.INTER_LINEAR)
     
     if debug:
         drawQuad(image, src, [255, 0, 0])
         drawQuad(warped, dst, [255, 255, 0])
         plt.imshow(image)
         plt.show()
         plt.imshow(warped)
         plt.show()
         
     return warped,  src,  dst

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    return lines

def draw_lane_lines(img, lines, color=[255, 0, 0], thickness=2):
     """
     NOTE: this is the function you might want to use as a starting point once you want to 
     average/extrapolate the line segments you detect to map out the full
     extent of the lane (going from the result shown in raw-lines-example.mp4
     to that shown in P1_example.mp4).  
     
     Think about things like separating line segments by their 
     slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
     line vs. the right line.  Then, you can average the position of each of 
     the lines and extrapolate to the top and bottom of the lane.
     
     This function draws `lines` with `color` and `thickness`.    
     Lines are drawn on the image inplace (mutates the image).
     If you want to make the lines semi-transparent, think about combining
     this function with the weighted_img() function below
     """
     # state variables to keep track of most dominant segment
     largestLeftLineSize = 0
     largestRightLineSize = 0
     largestLeftLine = (0,0,0,0)
     largestRightLine = (0,0,0,0)          
     line_img = np.zeros_like(img)
     inputImg = np.copy(img)
     intersectionPoint = (0, 0)
    
     avgLeft = (0,0,0,0)
     avgRight = (0,0,0,0)
    
     if lines is None:
        avgx1, avgy1, avgx2, avgy2 = avgLeft
        cv2.line(line_img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line
        avgx1, avgy1, avgx2, avgy2 = avgRight
        cv2.line(line_img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw right line
        return inputImg,  intersectionPoint
        
     if lines is not None:
          for line in lines:
            for x1,y1,x2,y2 in line:
                size = float(math.hypot(x2 - x1, y2 - y1))
                slope = float((y2-y1)/(x2-x1))                
                # Filter slope based on incline and
                # find the most dominent segment based on length
                if (slope > 0.1): #right
                    if (size > largestRightLineSize):
                        largestRightLine = (x1, y1, x2, y2)                    
                    cv2.line(line_img, (x1, y1), (x2, y2), (255,0, 0),2) #Show every line found
                elif (slope < -0.1): #left
                    if (size > largestLeftLineSize):
                        largestLeftLine = (x1, y1, x2, y2)
                    cv2.line(line_img, (x1, y1), (x2, y2), (255,0,0),2)    #Show every line found
                
     # Show largest line found on either sid
     #cv2.line(inputImg, (largestRightLine[0], largestRightLine[1]), (largestRightLine[2], largestRightLine[3]), (255,0,0),8)
     #cv2.line(inputImg, (largestLeftLine[0], largestLeftLine[1]), (largestLeftLine[2], largestLeftLine[3]), (255,0,0),8) 

     # Define an imaginary horizontal line in the center of the screen
     # and at the bottom of the image, to extrapolate determined segment
     imgHeight, imgWidth = (inputImg.shape[0], inputImg.shape[1])
     upLinePoint1 = np.array( [0, int(imgHeight - (imgHeight/2))] )
     upLinePoint2 = np.array( [int(imgWidth), int(imgHeight - (imgHeight/2))] )
     downLinePoint1 = np.array( [0, int(imgHeight)] )
     downLinePoint2 = np.array( [int(imgWidth), int(imgHeight)] )
    
     # Find the intersection of dominant lane with an imaginary horizontal line
     # in the middle of the image and at the bottom of the image.
     p3 = np.array( [largestLeftLine[0], largestLeftLine[1]] )
     p4 = np.array( [largestLeftLine[2], largestLeftLine[3]] )
     upLeftPoint = seg_intersect(upLinePoint1,upLinePoint2, p3,p4)
     downLeftPoint = seg_intersect(downLinePoint1,downLinePoint2, p3,p4)
     
     if (math.isnan(upLeftPoint[0]) or math.isnan(downLeftPoint[0])):
         avgx1, avgy1, avgx2, avgy2 = avgLeft
         #cv2.line(inputImg, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line
         avgx1, avgy1, avgx2, avgy2 = avgRight
         #cv2.line(inputImg, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw right line
     else:
         cv2.line(line_img, (int(upLeftPoint[0]), int(upLeftPoint[1])), (int(downLeftPoint[0]), int(downLeftPoint[1])), [0, 0, 255], 8) #draw left line
     
     # Calculate the average position of detected left lane over multiple video frames and draw
     if (math.isnan(upLeftPoint[0])== False and math.isnan(downLeftPoint[0]) == False):
         avgx1, avgy1, avgx2, avgy2 = avgLeft
         avgLeft = (movingAverage(avgx1, upLeftPoint[0]), movingAverage(avgy1, upLeftPoint[1]), movingAverage(avgx2, downLeftPoint[0]), movingAverage(avgy2, downLeftPoint[1]))
         avgx1, avgy1, avgx2, avgy2 = avgLeft
         cv2.line(inputImg, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line
      
     # Find the intersection of dominant lane with an imaginary horizontal line
     # in the middle of the image and at the bottom of the image.
     p5 = np.array( [largestRightLine[0], largestRightLine[1]] )
     p6 = np.array( [largestRightLine[2], largestRightLine[3]] )
     upRightPoint = seg_intersect(upLinePoint1,upLinePoint2, p5,p6)
     downRightPoint = seg_intersect(downLinePoint1,downLinePoint2, p5,p6)
     if (math.isnan(upRightPoint[0]) or math.isnan(downRightPoint[0])):
         avgx1, avgy1, avgx2, avgy2 = avgLeft
         #cv2.line(inputImg, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line
         avgx1, avgy1, avgx2, avgy2 = avgRight
         #cv2.line(inputImg, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw right line
     else:
         cv2.line(line_img, (int(upRightPoint[0]), int(upRightPoint[1])), (int(downRightPoint[0]), int(downRightPoint[1])), [0, 0, 255], 8) #draw left line
      
      # Calculate the average position of detected right lane over multiple video frames and draw
     if (math.isnan(upRightPoint[0])== False and math.isnan(downRightPoint[0]) == False):
         avgx1, avgy1, avgx2, avgy2 = avgRight
         avgRight = (movingAverage(avgx1, upRightPoint[0]), movingAverage(avgy1, upRightPoint[1]), movingAverage(avgx2, downRightPoint[0]), movingAverage(avgy2, downRightPoint[1]))
         avgx1, avgy1, avgx2, avgy2 = avgRight         
         cv2.line(inputImg, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw right line
      
     # Calculate intersection of detected lane lines
     if avgLeft == (0, 0, 0, 0) and avgRight != (0, 0, 0, 0):
         ar1 = np.array( [avgRight[0],  avgRight[1]] )
         ar2 = np.array( [avgRight[2],  avgRight[3]] )
         intersectionPoint = seg_intersect(ar1, ar2, upLinePoint1, upLinePoint2)
     if avgLeft != (0, 0, 0, 0) and avgRight == (0, 0, 0, 0):
         al1 = np.array( [avgLeft[0],  avgLeft[1]] )
         al2 = np.array( [avgLeft[2],  avgLeft[3]] )
         intersectionPoint = seg_intersect(al1, al2, upLinePoint1, upLinePoint2)
     if avgLeft != (0, 0, 0, 0) and avgRight != (0, 0, 0, 0):
         al1 = np.array( [avgLeft[0],  avgLeft[1]] )
         al2 = np.array( [avgLeft[2],  avgLeft[3]] )
         ar1 = np.array( [avgRight[0],  avgRight[1]] )
         ar2 = np.array( [avgRight[2],  avgRight[3]] )
         intersectionPoint = seg_intersect(al1, al2, ar1, ar2)

     if (math.isnan(intersectionPoint[0])== False and math.isnan(intersectionPoint[1]) == False): 
         cv2.circle(inputImg, (int(intersectionPoint[0]), int(intersectionPoint[1])), 12, (0, 255, 0), -1)
     
     return inputImg,  intersectionPoint
