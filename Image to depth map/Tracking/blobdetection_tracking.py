# USAGE
# python blobdetection_tracking.py --image1 data/Right2.jpg --image2 data/Left2.jpg

# import the necessary packages
import argparse
import imutils
import cv2


def center(image):
    # variable declarations
    blobsCounter = 0
    coordinates = []
    # convert the image to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_TRIANGLE)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] > 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # draw the contour and center of the shape on the image
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(image, str(blobsCounter), (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            # increment number of blobs found
            blobsCounter = blobsCounter+1
            # Save coordinates in coordinates
            coordinates.append([cX, cY])

        # show the image
        # cv2.imshow("Image", image)

    if blobsCounter == 0:
        print('No object detected')
    else:
        print('Objects detected: ', blobsCounter)
        # print(coordinates)
    # cv2.imwrite("results/blobdetection_centers.jpg", image)
    # cv2.waitKey(0)
    return coordinates


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image1", required=True,
                help="path to the input image")
ap.add_argument("-i2", "--image2", required=True,
                help="path to the input image2")
args = vars(ap.parse_args())

############### LOADING IMAGES ###########################
image1 = cv2.imread(args["image1"])
if image1 is None:
    print('Could not open or find the image1:', args.input)
    exit(0)
image2 = cv2.imread(args["image2"])
if image2 is None:
    print('Could not open or find the image2:', args.input)
    exit(0)

#### Find the contours and centers' coordinates of the blobs in these images ####
results1 = center(image1)
results2 = center(image2)
# print(results1)
# print(results2)
# Save the detections in the results folder
cv2.imwrite("results/blobdetection_image1.jpg", image1)
cv2.imwrite("results/blobdetection_image2.jpg", image2)


########### Find out if the camera goes to the left or right #################
xCoord = []
# yCoord = []
test = 0

if len(results1) < len(results2):
    for i in range(len(results1)):
        xCoord.append(results1[i][0] - results2[i][0])
        # yCoord.append(results1[i][1] - results2[i][1])
        test = test + xCoord[i]
else:
    for i in range(len(results2)):
        xCoord.append(results1[i][0] - results2[i][0])
        test = test + xCoord[i]
        # yCoord.append(results1[i][1] - results2[i][1])

# print(xCoord)
print(test)
if test > 0:
    print("camera goes to the right")
else:
    print('camera goes to the left')
