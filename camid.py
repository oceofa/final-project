import cv2

for i in range(5):  # Thử 5 ID đầu
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Webcam found at index {i}")
        cap.release()
