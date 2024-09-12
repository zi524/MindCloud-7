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
    

#to change password   
state3= input ("do you need to change password (yes/no): ")
#create file contains the current password
with open("password.txt","r") as data:
    old_password = data.read()
if(state3=="yes"):
       
   password=input("old password : ")
   new_password=input("new password : ")
   confirm_new_password=input("confirm password : ")


   if(password==old_password):

      if(new_password == confirm_new_password):
            
            with open("password.txt","w") as data:
                pass
            with open("password.txt","w") as data:
                data.write(new_password)

            print("password changed")

      else:
            print("The two passwords do not match")
        
   else:
      print("old password is wrong")


        




