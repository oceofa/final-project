import serial
import time
import cv2
import threading

# Biến toàn cục để kiểm soát webcam
webcam_running = False
cap = None

def open_webcam():
    global webcam_running, cap
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Không thể mở webcam.")
        webcam_running = False
        return

    print("Webcam đang chạy. Nhấn nút để tắt.")
    webcam_running = True

    while webcam_running:
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc frame.")
            break

        cv2.imshow("Webcam", frame)

        # Cho phép tắt bằng phím 'q' (tuỳ chọn)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    webcam_running = False

def close_webcam():
    global webcam_running
    if webcam_running:
        webcam_running = False
        print("Đã tắt webcam.")

def listen_to_arduino(port='COM3', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Đang kết nối đến {port}...")
        time.sleep(2)

        while True:
            if ser.in_waiting:
                data = ser.readline().decode().strip()
                print(f"Tín hiệu nhận được: {data}")

                if data == "S" and not webcam_running:
                    # Mở webcam trong luồng riêng để không chặn đọc serial
                    threading.Thread(target=open_webcam).start()
                elif data == "Q":
                    close_webcam()

    except serial.SerialException:
        print("Không thể kết nối đến Arduino. Kiểm tra cổng COM.")
    except KeyboardInterrupt:
        print("Đã dừng chương trình.")
        close_webcam()

# 👉 Thay COM3 nếu cần
listen_to_arduino(port='COM3')
