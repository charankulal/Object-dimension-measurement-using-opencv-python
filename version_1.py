import cv2
from measuring_and_detecting.object_detector import *
import numpy as np

# Load aruco detector
parameters = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

# Load object detector
detector = HomogeneousBgDetector()

# Load the Cap
cap = cv2.VideoCapture('http://100.70.206.220:8080/video')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# List to store object dimensions
object_dimensions = []
frame_count = 0

while True:
    _, img = cap.read()

    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    if corners:

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20

        contours = detector.detect_objects(img)

        # Draw objects boundaries and save dimensions
        if contours:
            frame_count += 1  # Increment frame count if objects are detected
            for cnt in contours:
                # Get rect
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect

                # Get Width and Height of the Objects by applying the Ratio pixel to cm
                object_width = w / pixel_cm_ratio
                object_height = h / pixel_cm_ratio

                # Save dimensions
                object_dimensions.append((round(object_width, 1), round(object_height, 1), frame_count))

                # Display rectangle
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.polylines(img, [box], True, (255, 0, 0), 2)
                cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

            # Save the current frame as an image
            cv2.imwrite(f"detected_frame_{frame_count}.png", img)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

# Save dimensions to a file
with open('object_dimensions.txt', 'w') as f:
    for dims in object_dimensions:
        f.write(f"Width: {dims[0]} cm, Height: {dims[1]} cm, Frame: {dims[2]}\n")

print("Object dimensions and images saved.")
