import cv2
import pickle

# Define constants for width and height
WIDTH, HEIGHT = 107, 48

# Load the positions list from the file or create a new list if the file does not exist
try:
    with open('CarParkingLocation', 'rb') as f:
        pos_list = pickle.load(f)
except FileNotFoundError:
    pos_list = []

def mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        for i, (x1, y1) in enumerate(pos_list):
            if x1 < x < x1 + WIDTH and y1 < y < y1 + HEIGHT:
                pos_list.pop(i)
                break  # Exit the loop after removing the position to avoid issues with modifying the list during iteration

    with open('CarParkingLocation', 'wb') as f:  # Ensure the correct filename is used for saving
        pickle.dump(pos_list, f)

while True:
    img = cv2.imread('carParkImg.png')

    # Draw all the rectangles for the parking positions
    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0] + WIDTH, pos[1] + HEIGHT), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouse_click)

    # Break the loop when 'ESC' key is pressed
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
