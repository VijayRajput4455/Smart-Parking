import cv2
import pickle
import cvzone
import numpy as np

# Constants
WIDTH, HEIGHT = 107, 48

# Load video feed
cap = cv2.VideoCapture(r'CarPark.mp4')

# Load parking space positions
with open('CarParkingLocation', 'rb') as f:
    pos_list = pickle.load(f)

def check_parking_space(img_processed, img):
    space_counter = 0

    for pos in pos_list:
        x, y = pos
        img_crop = img_processed[y:y + HEIGHT, x:x + WIDTH]
        count = cv2.countNonZero(img_crop)

        # Determine the color and thickness of the rectangle based on the parking space occupancy
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        # Draw rectangles and put count text on the parking space
        cvzone.putTextRect(img, str(count), (x, y + HEIGHT - 3), scale=1,
                           thickness=2, offset=0, colorR=color)
        cv2.rectangle(img, pos, (x + WIDTH, y + HEIGHT), color, thickness)

    # Display the total number of free spaces
    cvzone.putTextRect(img, f'Free: {space_counter}/{len(pos_list)}', (0, 50), scale=3,
                       thickness=2, offset=20, colorR=(0, 200, 0))

while True:
    # Reset the video to the beginning if it reaches the end
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        break

    # Image processing steps
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    # Check parking space availability
    check_parking_space(img_dilate, img)

    # Show the image with detected parking spaces
    cv2.imshow("Image", img)

    # Exit the loop if 'ESC' key is pressed
    if cv2.waitKey(10) == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
