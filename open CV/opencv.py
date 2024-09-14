import cv2
import os
import numpy as np
import shutil
import serial
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def face_recognition():
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
                return 1

                
            else:
                cv2.putText(frame, "unknown", (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), thickness=2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 4)
                return 0

        cv2.imshow('Detected Face', frame)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


def password_verification():
    state1 = input("Do you need to add a person to the database (yes/no): ")

    if state1 == "yes":
        name = input("Enter the name of the person: ")
        os.makedirs(f"images/{name}", exist_ok=True)
        cap = cv2.VideoCapture(0)
        for i in range(3):
            ret, frame = cap.read()
            cv2.waitKey(1000)
            if ret:
                image_path = f"images/{name}/{i}.jpg"
                cv2.imwrite(image_path, frame)
                cv2.imshow('Captured Image', frame)
                cv2.destroyAllWindows()
        print("Images saved")

    state2 = input("Do you need to delete a person from the database (yes/no): ")
    if state2 == "yes":
        removed_image = input("Enter the name of the person you want to delete: ")
        shutil.rmtree(f"images/{removed_image}")
        print("Images deleted")

    state3 = input("Do you need to change the password (yes/no): ")
    if state3 == "yes":
        with open("password.txt", "r") as data:
            old_password = data.read().strip()
        password = input("Old password: ")
        new_password = input("New password: ")
        confirm_new_password = input("Confirm new password: ")
        if password == old_password:
            if new_password == confirm_new_password:
                with open("password.txt", "w") as data:
                    data.write(new_password)
                print("Password changed")
            else:
                print("The two passwords do not match")
        else:
            print("Old password is wrong")

    pswrd = input("Enter the password: ")
    with open("password.txt", "r") as data:
        password = data.read().strip()
    if pswrd == password:
        return 1
    else:
        print("Wrong password")
        return 0

print(f"choose a)face recognition")
print(f"\n")
res=input("b)password verification")
if res=="a":
  p=password_verification() 

elif res=="b":
  p=face_recognition()
else:print(f"error please renter a or b")
if (p):
    ser = serial.Serial('COM3', 9600)
    ser.write(b'recognised')
    ser.close()
   '''connection to microcobtrollers
    Serial.begin(9600);#setup fn 
    in the loop fn :
    if (Serial.available() > 0) {
    String input = Serial.readString(); 
   if (input == "RECOGNIZED")}'''

   
