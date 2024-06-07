import cv2
import face_recognition

# Load the image of the person you want to recognize
known_image = face_recognition.load_image_file("kullanıci_yuzu.jpg")

# Encode the known image
known_image_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize the camera
video_capture = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = video_capture.read()

    # Convert the frame to RGB format
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through all the faces in the current frame
    for face_encoding in face_encodings:
        # Compare the face encoding with the known image encoding
        results = face_recognition.compare_faces([known_image_encoding], face_encoding)

        # If the face is recognized, print the name and draw a bounding box around the face
        if True in results:
            (top, right, bottom, left) = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
video_capture.release()
cv2.destroyAllWindows()