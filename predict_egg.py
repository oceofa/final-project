import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO(r"best.pt")


# Open the default webcam (camera index 0)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Không thể mở webcam.")
    exit()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc frame từ webcam.")
        break

    # Perform inference on the frame
    results = model(frame)

    # Process the results and draw bounding boxes and labels on the frame
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Get confidence score
            conf = box.conf[0]

            # Get class index
            cls = int(box.cls[0])

            # Get class name
            names = model.names
            class_name = names[cls]

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label with confidence score
            label = f'{class_name}: {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the processed frame
    cv2.imshow('YOLOv8 Webcam Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()