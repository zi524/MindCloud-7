import cv2
import os
import shutil
state1= input("do you need to add person in data base(yes/no): ")

if (state1=="yes"):
    #take name of person 
    name = input("enter name of the person : ")
    os.mkdir(f"images/{name}")

    #open the camera
    cap = cv2.VideoCapture(0)
    
    
    #save images in folder and show it in extrnal tab
    for i in range (3):
        #take a photo 
        ret , frame = cap.read()
        cv2.waitKey(1000)
        if ret :
           image_path = f"images/{name}/{i}.jpg"

           cv2.imwrite(image_path,frame)
           cv2.imshow('Captured Image', frame)
           
           cv2.destroyAllWindows()
    print("images saved")

#to delete person 
state2= input("do you need to delete person from data base(yes/no): ")
if(state2=="yes"):
    removed_image=input("enter name of person you want to delete: ")
    #remove folder =>shutil.rmtree
    #remove file =>os.remove
    shutil.rmtree(f"images/{removed_image}")
    print("images deleted")
    



        




