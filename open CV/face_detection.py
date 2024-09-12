import cv2
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Create list containing names of owners
owners = os.listdir("images")

    
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


datagen = ImageDataGenerator(
    rotation_range=10,  # Reduced rotation range
    width_shift_range=0.1,  # Reduced width shift
    height_shift_range=0.1,  # Reduced height shift
    shear_range=0.1,  # Reduced shear range
    zoom_range=0.1,  # Reduced zoom range
    horizontal_flip=True,
    fill_mode='nearest'
)

# Function to convert images to grayscale face
def training():
    features = []  # Contain faces in grayscale
    labels = []
 
    for owner in owners:
        label = owners.index(owner)
        # Take 10 images per owner
        for i in range(10):
            img_path = f"images/{owner}/{i}.jpeg"
            img_array = cv2.imread(img_path)
            if img_array is None:
                continue
            # Convert image to grayscale 
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            # Detect the face in grayscale image
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(100, 100))

            if len(faces) == 0:
                print(f"No face detected in {img_path}")
                continue

            # Save grayscale face in the folder 
            for (x, y, w, h) in faces:
                faces_roi = gray[y:y+h, x:x+w]
                faces_roi = cv2.resize(faces_roi, (200,200))
                faces_roi = np.expand_dims(faces_roi, axis=0)  
                faces_roi = np.expand_dims(faces_roi, axis=-1)
                # Data augmentation
                i=0
                for augmented_face in datagen.flow(faces_roi, batch_size=1):
                    features.append(augmented_face[0].astype(np.uint8))
                    labels.append(label)
                    i += 1
                    if i >= 2:  # Stop after generating 20 augmented images
                        break

    features = np.array(features, dtype=np.uint8)
    labels = np.array(labels, dtype=np.int32)

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(features, labels)
    face_recognizer.save('face_trained.yml')
    np.save('features.npy', features)
    np.save('labels.npy', labels)

    print('Training done')
    print(f'Total features: {len(features)}')

training()

# Open camera
cap = cv2.VideoCapture(0)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

while cap.isOpened():
    ret, frame = cap.read()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    Cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    rect = Cascade.detectMultiScale(frame_gray, scaleFactor=1.5, minNeighbors=5, minSize=(100, 100))
    for (x, y, w, h) in rect:
        region_of_interest = frame_gray[y:y+h, x:x+w]
        region_of_interest = cv2.resize(region_of_interest, (200, 200))
        region_of_interest = np.expand_dims(region_of_interest, axis=0)
        region_of_interest = np.expand_dims(region_of_interest, axis=-1)

        prediction, confidence_level = face_recognizer.predict(region_of_interest[0])
        print(f'Prediction: {owners[prediction]}, Confidence: {confidence_level}')
        
    


        if confidence_level > 85:
            cv2.putText(frame, f'{owners[prediction]}', (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), thickness=2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
            # send to microcontroller
        else:
            cv2.putText(frame, "unknown", (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), thickness=2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 4)

    cv2.imshow('Detected Face', frame)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
