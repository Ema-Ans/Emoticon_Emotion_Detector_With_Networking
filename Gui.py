#for now only the questions "q" works, i still need to put the model together with the gui as well as the server and the client
#hence why only "enter" and "q" work in the gui for now :p

#start 2 comes after you have captured your image!


#remember by pressing c we are just connecting
#however u start tyrping in the chatting mode which you get after connect

#we press Right arrow key to send the text

#press v to connect
from re import A
from cmu_112_graphics import *
from tkinter import *
import random
  
from tkinter import *
from PIL import Image,ImageTk
import socket

#for opencv
import cv2
import numpy as np
from keras.preprocessing import image
import warnings
warnings.filterwarnings("ignore")
from keras.preprocessing.image import load_img, img_to_array 
from keras.models import  load_model
import matplotlib.pyplot as plt
import numpy as np


def test(app):
    connect(app)
    receive(app)

def appStarted(app):
    app.run = True
    app.captured = False
    app.response = None
    app.emotion = None #the one that you get from the model
    app.dataavailable = None
    app.socket = None
    app.mode = "Beginning" #make sure to reset this to Beginning
    app.timerS = 0 
    app.coords = []
    app.timerB = 0
    app.timerUni = 0
    app.timerHapB = 0
    app.text = "'Press Enter to establish a connection'"
    app.questions = False
    app.happinessLevel = 0
    app.sadnessLevel = 0
    app.coordinate = None
    app.happPerc = 0
    app.received = []
    app.messages = [] #contains mesages as a sentence, will be sent to clients and the servers
    app.words = ["Start Typing..."] #actively whatver the user types
    app.mywords = "" #to actively draw whatever the user types
    app.coordtimer = 0
    app.messages2 = []
    url = 'https://media.istockphoto.com/photos/nicelooking-attractive-gorgeous-glamorous-elegant-stylish-cheerful-picture-id1165055006?k=20&m=1165055006&s=612x612&w=0&h=OD4-_BceL_R2eaaBzDQrXNIyydwYXOJX-m-0z12z17s='
    app.image1 = app.loadImage(url).resize((app.width//2,app.height//2), Image.ANTIALIAS) #party
    url2 = 'https://i.pinimg.com/736x/e9/a0/dd/e9a0dd5b66a0a2aac0078dad7b72c456.jpg'
    app.image2 = app.loadImage(url2).resize((app.width//2,app.height//2), Image.ANTIALIAS) #netflix
    url3 = "https://media.istockphoto.com/photos/furious-businesswoman-throws-a-punch-into-computer-screaming-picture-id465381160?k=20&m=465381160&s=612x612&w=0&h=va2IhLUP0b2EOYolC_YZbtqKuuIXaEVnslIBkCwXcEw="
    app.image3 = app.loadImage(url3).resize((app.width//2,app.height//2), Image.ANTIALIAS) #computer
    url4 = "https://leetcode.com/static/images/LeetCode_Sharing.png"
    app.image4 = app.loadImage(url4).resize((app.width//2,app.height//2), Image.ANTIALIAS) #computer
    url5 = "https://www.incimages.com/uploaded_files/image/1920x1080/getty_912592258_366180.jpg"
    app.image5 = app.loadImage(url5).resize((app.width//2,app.height//2), Image.ANTIALIAS) #doggy
    url6 = "https://thumbs.dreamstime.com/b/funny-sad-young-freezing-cat-wrapped-scarf-striped-woolen-preparation-winter-cold-85191302.jpg"
    app.image6 = app.loadImage(url6).resize((app.width//2,app.height//2), Image.ANTIALIAS) #Cat
    url7 = "https://cdn.pixabay.com/photo/2015/01/07/15/51/woman-591576__480.jpg"
    app.image7 = app.loadImage(url7).resize((app.width//2,app.height//2), Image.ANTIALIAS) #happy and free
    url8 = "https://static.statusqueen.com/dpimages/thumbnail/dp_image36-849.jpg"
    app.image8 = app.loadImage(url8).resize((app.width//2,app.height//2), Image.ANTIALIAS) #sad boi
    url9 = "https://i.pinimg.com/236x/78/b2/e5/78b2e57240307b084a9edac2e13dc84c.jpg"
    app.image9 = app.loadImage(url9).resize((app.width,app.height), Image.ANTIALIAS)
    app.connectionmade = False
    app.first = True #to empty the list of the messages
    app.extra = 0 #everytime you send a messsage you use this to add extra space betweeen messages
    app.extra2 = 0
    app.word = ""
    app.sent = [0,0,0,0,0,0] #6 zeroes
    app.model =  load_model("best_model.h5")
    app.mess1 = ""
    app.mess2 = ""
    app.mess3 = ""
    app.mess4 = ""
    app.mess5 = ""
    app.mess6 = ""
    app.rec1 = ""
    app.rec2 = ""
    app.rec3 = ""
    app.rec4 = ""
    app.rec5 = ""
    app.rec6 = ""
    app.questions2 = False
    app.charac = [chr(128512), chr(128532), chr(128528)]
    app.final = ""
    app.receivedFirst = False
    app.sentFirst = False
    #app.image1 = app.scaleImage(app.image2, 2)
    #app.image1 = app.loadImage('party.jpg')
    #app.image2 = app.loadImage('netflix.jpg')

def captureImage(app):
    model = load_model("best_model.h5")
    face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while True:
        ret, test_img = cap.read()  # captures frame and returns boolean value and captured image
        if not ret:
            continue
        gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
            roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
            roi_gray = cv2.resize(roi_gray, (224, 224))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255
            predictions = model.predict(img_pixels)
            # find max indexed array
            max_index = np.argmax(predictions[0])
            emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
            predicted_emotion = emotions[max_index]
            cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        resized_img = cv2.resize(test_img, (1000, 700))
        cv2.imshow('Facial emotion analysis ', resized_img)

        if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
            app.emotion = predicted_emotion
            #print("your emotion", predicted_emotion)
            
            
            break

    cap.release()
    cv2.destroyAllWindows
    
def receive(app):    #this should prolly be in the timer fired
    app.dataavailable = True
    try:
        
        app.response = app.socket.recv(4069)  #app.socket.recv(1024)
        
    except:
        app.dataavailable = False
    if app.dataavailable:
        
        
        app.response = app.response.decode('utf-8')
       
        app.response = eval(app.response)
        
        app.receivedFirst = True
    return app.response
        
        

def keyPressed(app,event):
    
    # print(event.key)
    if event.key == "Enter" and app.mode == "Beginning":
        app.mode = "Beginning2"
    if app.mode == "Beginning2" and event.key == "h":
        app.mode = "help"
    if app.mode == "help" and event.key == "Enter":
        app.mode = "Start"
    if app.mode == "Start2" and event.key == "Enter":
        app.mode = "Start"
    if app.mode == "Start" and event.key == "c":
        app.mode = "capturing"
    if app.mode == "Start" and event.key == "q" and app.captured:
        app.mode = "questions"
    if event.key == "Enter" and app.mode == "happLev":
        app.mode = "Start"
    if event.key == "v" and app.mode == "Start":
        connect(app)
        app.mode = "chatting"
    if app.mode == "chatting" and event.key == "Tab":
        app.run = True
        app.captured = False
        app.response = None
        app.emotion = None #the one that you get from the model
        app.dataavailable = None
        app.socket = None
        app.mode = "Beginning" #make sure to reset this to Beginning
        app.timerS = 0 
        app.coords = []
        app.timerB = 0
        app.timerUni = 0
        app.timerHapB = 0
        app.text = "'Press Enter to establish a connection'"
        app.questions = False
        app.happinessLevel = 0
        app.sadnessLevel = 0
        app.coordinate = None
        app.happPerc = 0
        app.received = []
        app.messages = [] #contains mesages as a sentence, will be sent to clients and the servers
        app.words = ["Start Typing..."] #actively whatver the user types
        app.mywords = "" #to actively draw whatever the user types
        app.coordtimer = 0
        app.messages2 = []
        app.connectionmade = False
        app.first = True #to empty the list of the messages
        app.extra = 0 #everytime you send a messsage you use this to add extra space betweeen messages
        app.extra2 = 0
        app.word = ""
        app.sent = [0,0,0,0,0,0] #6 zeroes
        app.model =  load_model("best_model.h5")
        app.mess1 = ""
        app.mess2 = ""
        app.mess3 = ""
        app.mess4 = ""
        app.mess5 = ""
        app.mess6 = ""
        app.rec1 = ""
        app.rec2 = ""
        app.rec3 = ""
        app.rec4 = ""
        app.rec5 = ""
        app.rec6 = ""
        app.questions2 = False
        app.charac = [chr(128512), chr(128532), chr(128528)]
        app.final = ""
        app.receivedFirst = False
        app.sentFirst = False
    if app.mode == "contradiction":
        app.run = True
        app.captured = False
        app.response = None
        app.emotion = None #the one that you get from the model
        app.dataavailable = None
        app.socket = None
        app.mode = "Start" #make sure to reset this to Beginning
        app.timerS = 0 
        app.coords = []
        app.timerB = 0
        app.timerUni = 0
        app.timerHapB = 0
        app.text = "'Press Enter to establish a connection'"
        app.questions = False
        app.happinessLevel = 0
        app.sadnessLevel = 0
        app.coordinate = None
        app.happPerc = 0
        app.received = []
        app.messages = [] #contains mesages as a sentence, will be sent to clients and the servers
        app.words = ["Start Typing..."] #actively whatver the user types
        app.mywords = "" #to actively draw whatever the user types
        app.coordtimer = 0
        app.messages2 = []
        app.connectionmade = False
        app.first = True #to empty the list of the messages
        app.extra = 0 #everytime you send a messsage you use this to add extra space betweeen messages
        app.extra2 = 0
        app.word = ""
        app.sent = [0,0,0,0,0,0] #6 zeroes
        app.model =  load_model("best_model.h5")
        app.mess1 = ""
        app.mess2 = ""
        app.mess3 = ""
        app.mess4 = ""
        app.mess5 = ""
        app.mess6 = ""
        app.rec1 = ""
        app.rec2 = ""
        app.rec3 = ""
        app.rec4 = ""
        app.rec5 = ""
        app.rec6 = ""
        app.questions2 = False
        app.charac = [chr(128512), chr(128532), chr(128528)]
        app.final = ""
        app.receivedFirst = False
        app.sentFirst = False
    if app.run:
        if app.connectionmade and app.mode == "chatting":
            if app.receivedFirst:
                app.extra = 50
                app.extra2 = 1
              
            else:
                app.extra2 = 50
                app.extra = 1
               
        app.run = False


        
    if app.mode == "chatting":
        if app.first:
            app.words = [] #it will orginally contain "Start Typing..."
        y = event.key
        app.first = False #we have pressed our first key
        
        if y == "Space":
            y = " "
        
            if app.words != []:
                app.words = app.words
        if event.key != "Right":
            app.words.append(str(y)) #to draw on the canvas #["h","E","l","l","O"] #this list draws on tryping bar
            if y == "Backspace":
                app.words = app.words[:-2]
        
            #print(app.words)
        else:
            app.messages.append("".join(app.words)) #to create a sentence#this is going to be sent to the user #this sends the message to the server
            #and this list is also printed on the chatting side of the client
            app.words = ["Start Typing..."] # reset it back to this after the user presses enter
            app.first = True #so we can empty the list again
            app.rightPressed = True
        
            if len(app.messages) > 1:
                app.word = app.messages[-1]
                if app.word[0] == "{":
                    app.word = app.word[1:-1]
                    app.messages2 = [app.word]
                else:
                    app.messages2 = [app.messages[-1]]

                msg = {"type":"msg","emotion":app.emotion, "msg":app.messages2}
                app.messages2 = []
            else:
                msg = {"type":"msg","emotion":app.emotion, "msg":app.messages}
            app.sentFirst = True #here we have sent before receiving
            app.socket.sendall(str(msg).encode())  # send a message
           
            print("sending to server")
        
            
            # if the user presses rigth key then it should send it to the server
            
        
        

def timerFired(app):
    if app.mode == "happLev" and app.questions:
    
        if app.emotion == "happy" and app.happPerc < 50:
            app.mode = "contradiction"
        if app.emotion == "sad" and app.happPerc> 50:
            app.mode = "contradiction"
        if app.emotion == "neutral" and app.happPerc == 50:
            app.mode = "contradiction"
    if app.mode == "Start2" and app.coordtimer%10 == 0:
        y = random.randint(0,app.width)
        x = random.randint(0,app.width)
        charac = random.choice(app.charac)

        app.coords.append((x,y, charac))
        app.questions = True 
        


    if app.mode == "Beginning":

        app.timerB += 1
        app.timerS = 0
        app.timerUni += 1
        if app.timerUni == 50:
            app.timerUni = 0
        if app.timerB%20 == 0:
            app.text = " "
        else:
            app.text = "'Press Enter to establish a connection'"
    if app.mode == "Start" or app.mode == "Beginning2": #only start timer when the mode is start
        #make sure to reset this in other modes
        app.timerS += 1
        app.timerUni += 1
    if app.timerUni == 50:
        app.timerUni = 0
    if app.timerS == 5:
        app.text = "Today we are"
    if app.mode == "capturing":
        captureImage(app)
        app.captured = True
        app.mode = "Start2"#add something else ehrrer

        
    if app.mode == "questions" or app.mode == "question2" or app.mode == "question3" or \
       app.mode == "question4" or app.mode == "happLev" or app.mode == "help":
        app.timerUni += 1
        if app.timerUni == 50:
            app.timerUni = 0
    if app.mode == "happLev":
        app.timerHapB += 1
        app.questions2 = True 
        app.happPerc = int((app.happinessLevel / 40)* 100)
 
    if app.mode == "chatting" and app.connectionmade:

        app.mywords = "".join(app.words)
    if app.messages != [] and app.mode == "chatting" and app.connectionmade:
           
        app.mess1 = "".join(app.messages[0]) #app.i to get the first
        if len(app.messages) == 7:
            app.messages = app.messages[1:] #so only shows the latest 6 messages
            

        if len(app.messages) >= 2:
            app.mess2 = "".join(app.messages[1])
        if len(app.messages) >= 3:
            app.mess3 = "".join(app.messages[2])
        if len(app.messages) >= 4:
            app.mess4 = "".join(app.messages[3])
            #print("app.mess4", app.mess4)
        if len(app.messages) >= 5:
            app.mess5 = "".join(app.messages[4])
        if len(app.messages) >= 6:
            app.mess6 = "".join(app.messages[5])

    if app.received != [] and app.mode == "chatting" and app.connectionmade:
        
        app.rec1 = "".join(app.received[0]) #app.i to get the first
        
        if len(app.received) == 7:
            app.received = app.received[1:] #so only shows the latest 6 messages
            
            
        if len(app.received) >= 2:
           
            app.rec2 = app.received[1]
        if len(app.received) >= 3:
            app.rec3 = app.received[2]
        if len(app.received) >= 4:
            app.rec4 = app.received[3]
            #print("app.mess4", app.mess4)
        if len(app.received) >= 5:
            app.rec5 = app.received[4]
        if len(app.received) >= 6:
            app.rec6 = app.received[5]


    if app.mode == "chatting" and app.connectionmade == True:
        app.final = receive(app)

        if app.final != None: #so we dont append None
            if app.received == []:
                app.received.append(app.final)
            else:
                if app.final != app.received[-1]: #so only appends the new thing
                    print("this is what you receive", app.received)
                    app.received.append(app.final)
                #print("hey there", app.received)
        
            
            
        
def connect(app):
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 15112        # The port used by the server
    
    app.emotion = "Happy"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((HOST, PORT))
    client_socket.setblocking(False)
    app.socket = client_socket

    msg = {"type":"emotion","emotion":app.emotion}
    app.socket.sendall(str(msg).encode())
    app.connectionmade = True
           
def mousePressed(app,event):
    if app.mode == "questions":
        app.coordinate = event.x//(app.width//2)
        if app.coordinate == 0:
            app.happinessLevel += 5
        else:
            app.happinessLevel  = app.happinessLevel
        if app.coordinate == 0 or app.coordinate == 1:
            app.mode = "question2"
            app.coordinate = None
            
    elif app.mode == "question2":
        
        app.coordinate = event.x//(app.width//2)
    
        
        if app.coordinate == 0:
            app.happinessLevel = app.happinessLevel
        else:
            app.happinessLevel += 5
        if app.coordinate == 0 or app.coordinate == 1:
            app.mode = "question3"
            app.coordinate =  None
            
    elif app.mode == "question3":

        app.coordinate = event.x//(app.width//2)
        
        if app.coordinate == 0:
            app.happinessLevel = app.happinessLevel
        else:
            app.happinessLevel += 5
        if app.coordinate == 0 or app.coordinate == 1:
            app.mode = "question4"
    elif app.mode == "question4":
        app.coordinate = event.x//(app.width//2)
        
        if app.coordinate == 0:
            app.happinessLevel += app.happinessLevel
        else:
            app.happinessLevel = app.happinessLevel
        if app.coordinate == 0 or app.coordinate == 1:
            app.mode = "happLev"

            app.happPerc = (app.happinessLevel // 30)* 100


            
        
    
def background(app, canvas):
        canvas.create_rectangle(0,0, app.width, app.height, fill = "white")
        canvas.create_line(0,0, 0,\
                           app.height, width = 10, fill="#fceed1" )
        canvas.create_line(0, app.height, app.width,\
                           app.height, width = 10, fill="#fceed1" )
    
        canvas.create_polygon([(.68*app.width), 0, app.width,app.height//2, (.68*app.width), app.height],fill ="#fceed1") 

        canvas.create_polygon([0,0,(.68*app.width), 0,(.68*app.width), app.height, 0, app.height], fill= "#fceed1")
        if app.questions:
            canvas.create_text(int(0.80 * app.width), int(0.10*app.height), \
                        text = f"Happiness Level:{app.happinessLevel}", font = "Serif 13 bold" , anchor = "w", fill = "#7d3cff")
        ### addding characters:
        if (app.timerUni<=10) or (app.timerUni>=40):
            canvas.create_text(app.width - 300,\
                                       app.height-100,text = chr(128512),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
        if (app.timerUni <= 20) or app.timerUni>=40:
            canvas.create_text(app.width - 200,\
                                       app.height-100 ,text = chr(128532),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
        if (app.timerUni <= 30) or app.timerUni>= 40:
            
        
            canvas.create_text(app.width - 100,\
                                       app.height-100,text = chr(128528),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
    
def redrawAll(app, canvas):
 
    
    if app.mode == "Beginning2":
        canvas.create_rectangle(0,0, app.width, app.height, fill = "white")
        canvas.create_line(0,0, 0,\
                           app.height, width = 10, fill="#fceed1" )
        canvas.create_line(0, app.height, app.width,\
                           app.height, width = 10, fill="#fceed1" )
        canvas.create_polygon([0, 0, app.width,0, 0, app.height],fill ="#fceed1")
        if (app.timerUni<=10) or (app.timerUni>=40):
            canvas.create_text(app.width - 300,\
                                       app.height - 100,text = chr(128512),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
        if (app.timerUni <= 20) or app.timerUni>=40:
            canvas.create_text(app.width - 200,\
                                       app.height - 100,text = chr(128532),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
        if (app.timerUni <= 30) or app.timerUni>= 40:
            
        
            canvas.create_text(app.width - 100,\
                                       app.height-100,text = chr(128528),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
        if app.timerS >5:
            canvas.create_text(10, 10,text= "At", font = "Serif 13" , anchor = "nw", fill = "#7d3cff")
        if app.timerS>15:
            canvas.create_text(10, 40, text = "Emoticon...", anchor = "nw", font = "Forte 100 bold", fill = "#7d3cff")
        if app.timerS>25:
            canvas.create_text(10, 250, text = "You'll find friends through thick and thin :)",   font = "Serif 13" , anchor = "nw", fill = "#7d3cff")
        if app.timerS>35:
            canvas.create_text(app.width//2, app.height//2 +250, text="'Press h for help on how to begin'", font = "Serif 13" , anchor = "w", fill = "#7d3cff")

    if app.mode == "Start":
        background(app, canvas)
        canvas.create_text(10, 40, text = "Emoticon", anchor = "nw", font = "Forte 100 bold", fill = "#7d3cff")
        if app.captured == False and app.questions == False:
            
            canvas.create_text(app.width//2 - 350,\
                                            app.height//2,text = chr(128512),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
        
            canvas.create_text(app.width//2 - 300, app.height//2, text = "'Press c to capture your emotion'" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        if app.captured:
            canvas.create_text(app.width//2 - 300, app.height//2 + 60, text = "'Press q' for questions" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
            #if app.timerS>40:
            canvas.create_text(app.width//2 - 350,\
                                       app.height//2 + 60 ,text = chr(128532),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
           # canvas.create_text(app.width//2, app.height//2 + 60, text = "'Press c to capture your emotion'" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        
        if app.questions2 == True:
            canvas.create_text(int(0.80 * app.width), 100, text = f"Happiness Percentage: {app.happPerc}%" ,font = "Serif 13 bold" , anchor = "w", fill = "#7d3cff")
            canvas.create_text(app.width//2 - 350,\
                                       app.height//2 + 120 ,text = chr(128528),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
            canvas.create_text(app.width//2 - 300, app.height//2 + 120, text = "'Press v to connect'" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
            #canvas.create_text(app.width//2 - 300, app.height//2 + 180, text = "'Press u to begin chatting'" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
            
            
            
    if app.mode == "help":
        background(app,canvas)
        canvas.create_text(10, 40, text = "Emoticon", anchor = "nw", font = "Forte 100 bold", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 350,\
                                       app.height//2,text = chr(128512),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
        canvas.create_text(app.width//2 - 350,\
                                       app.height//2 + 60 ,text = chr(128532),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
        canvas.create_text(app.width//2 - 350,\
                                       app.height//2 + 120 ,text = chr(128528),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2, text = "Start by caputring your image" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2 + 60, text = "Then you will be asked a set of questions, to confirm your emotion" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2 + 120, text = "After which you can connect with people , who are feeling the same emotion as you" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 150, app.height//2 + 200, text = "Press 'Enter' to start" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
    if app.mode == "Beginning":
        canvas.create_rectangle(0,0, app.width, app.height, fill = "white")
        canvas.create_line(0,0, 0,\
                           app.height, width = 10, fill="#fceed1" )
        canvas.create_line(0, app.height, app.width,\
                           app.height, width = 10, fill="#fceed1" )
        
    
        canvas.create_polygon([(.68*app.width), 0, app.width,app.height//2, (.68*app.width), app.height],fill ="#fceed1") 

        canvas.create_polygon([0,0,(.68*app.width), 0,(.68*app.width), app.height, 0, app.height], fill= "#fceed1")
        canvas.create_text(10, app.height//2 - 30, text = "Emoticon", font = "Forte 100 bold",anchor = "w", fill = "#7d3cff")
        if (app.timerUni<=10) or (app.timerUni>=40):
            canvas.create_text(app.width - 300,\
                                       app.height - 100,text = chr(128512),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
        if (app.timerUni <= 20) or app.timerUni>=40:
            canvas.create_text(app.width - 200,\
                                       app.height - 100,text = chr(128532),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
        if (app.timerUni <= 30) or app.timerUni>= 40:
            
        
            canvas.create_text(app.width - 100,\
                                       app.height-100,text = chr(128528),\
                                       font=f'Arial 50 bold', fill = "#7d3cff")
        
        if app.timerB>10:

            canvas.create_text(15, app.height//2 + 100, text = "A place where your feelings are ...", font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        if app.timerB> 20:
            canvas.create_text(15, app.height//2 + 130, text = "validated, shared and celebrated!", font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        if app.timerB> 30:
            canvas.create_text(app.width//2 - 300, app.height//2 + 250, text = app.text, font = "Serif 13" , anchor = "w", fill = "#7d3cff")
            
        
    if app.mode == "questions":
        #the baseee:
        background(app,canvas)
             ### the elements
        canvas.create_image(0,app.height//2 -200, image=ImageTk.PhotoImage(app.image1), anchor = "nw")
        canvas.create_image(app.width//2,app.height//2 -200, image=ImageTk.PhotoImage(app.image2), anchor = "nw")
        canvas.create_line(app.width//2, app.height//2-200, app.width//2, app.height, width = 10 , fill = "#fceed1")
        #canvas.create_text(int(0.80 * app.width), int(0.10*app.height), \
                           #text = f"Happiness Level:{app.happinessLevel}", font = "Serif 13 bold" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(15, app.height//2 - 300, text = "What looks more appealing? Close your eyes and ask yourself, where do you want to be?",\
                           font = "Serif 16 bold" , anchor = "w", fill = "#7d3cff")
        
    if app.mode == "question2":
        background(app, canvas)
        #adding the elements
        canvas.create_text(15, app.height//2 - 300, text = "Which one looks like something you would want to do right now?",\
                           font = "Serif 16 bold" , anchor = "w", fill = "#7d3cff")
            
        canvas.create_image(0,app.height//2 -200, image=ImageTk.PhotoImage(app.image3), anchor = "nw")
        canvas.create_image(app.width//2,app.height//2 -200, image=ImageTk.PhotoImage(app.image4), anchor = "nw")
        canvas.create_line(app.width//2, app.height//2-200, app.width//2, app.height, width = 10 , fill = "#fceed1")
        
    if app.mode == "question3":
        
        background(app, canvas)
    ### adding the elements tha we are working on
         ### adding the elements
        canvas.create_text(15, app.height//2 - 300, text = "Which one looks cuter? Shh, no one's gonna know your choices :p",\
                           font = "Serif 16 bold" , anchor = "w", fill = "#7d3cff")
        canvas.create_image(0,app.height//2 -200, image=ImageTk.PhotoImage(app.image6), anchor = "nw")
        canvas.create_image(app.width//2,app.height//2 -200, image=ImageTk.PhotoImage(app.image5), anchor = "nw")
        canvas.create_line(app.width//2, app.height//2-200, app.width//2, app.height, width = 10 , fill = "#fceed1")
    
    if app.mode == "question4":
        background(app, canvas)
         ### adding the elements
        canvas.create_text(15, app.height//2 - 300, text = "Which one resonates with you more?",\
                           font = "Serif 16 bold" , anchor = "w", fill = "#7d3cff")
        canvas.create_image(0,app.height//2 -200, image=ImageTk.PhotoImage(app.image7), anchor = "nw")
        canvas.create_image(app.width//2,app.height//2 -200, image=ImageTk.PhotoImage(app.image8), anchor = "nw")
        canvas.create_line(app.width//2, app.height//2-200, app.width//2, app.height, width = 10 , fill = "#fceed1")
        
    if app.mode == "happLev":
        background(app, canvas)
        canvas.create_text(app.width//2, app.height//2 + 240, text = "'Press Enter to return Back'" ,font = "Serif 13" , fill = "#7d3cff")
        if app.timerHapB % 5 != 0:
            canvas.create_rectangle(app.width//2 -300, app.height//2 -100, app.width//2 + 300, app.height//2 +60, fill = "#7d3cff", outline =  "#7d3cff" )
            canvas.create_text(app.width//2, app.height//2, text = f"Your happiness percentage is {app.happPerc}%",\
                           font = "Serif 16 bold" , fill = "#fceed1")
        if app.happPerc < 50:
                 #canvas.create_text(app.width//2, app.height//2, text = f"Your happiness percentage is {app.happPerc}%",\
                           #font = "Serif 16 bold" , fill = "#fceed1")
            canvas.create_text(app.width//2, app.height//2 + 100, \
                                    text = "Which is absolutely amazing!" ,font = "Serif 13 italic" , fill = "#7d3cff")
            canvas.create_text(app.width//2, app.height//2 + 150, \
                                    text = "Being sad is completely normal" ,font = "Serif 13 italic" , fill = "#7d3cff")
        if app.happPerc == 50:
            canvas.create_text(app.width//2, app.height//2 + 100, \
                                    text = "Unsure, are we?" ,font = "Serif 13 italic" , fill = "#7d3cff")
            canvas.create_text(app.width//2, app.height//2 + 150, \
                                    text = "So what! Being uncertain is completely normal at emoticon :p" ,font = "Serif 13 italic" , fill = "#7d3cff")
        if app.happPerc>50:
            canvas.create_text(app.width//2, app.height//2 + 100, \
                                    text = "Aha!!! Sunshine :)" ,font = "Serif 13 italic" , fill = "#7d3cff")
            canvas.create_text(app.width//2, app.height//2 + 150, \
                                    text = "That beam is blinding :p" ,font = "Serif 13 italic" , fill = "#7d3cff")
    if app.mode == "capturing":
        background(app,canvas)
        canvas.create_text(10, 40, text = "Emoticon", anchor = "nw", font = "Forte 100 bold", fill = "#7d3cff")
        ###
        canvas.create_text(app.width//2 - 350,\
                                       app.height//2,text = chr(128512),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
        canvas.create_text(app.width//2 - 350,\
                                       app.height//2 + 60 ,text = chr(128532),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
        canvas.create_text(app.width//2 - 350,\
                                       app.height//2 + 120 ,text = chr(128528),\
                                       font=f'Arial 25 bold', fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2, text = "There you are :)" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2 + 60, text = "Flaunt that smile of yours" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2 + 120, text = "Or give me your dreadful Stare ;)" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 150, app.height//2 + 200, text =  "Wait for the box to blink, 'Press q when you are done'" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")

        ###
    
    if app.mode == "Start2":
        background(app,canvas)
        #canvas.create_text()
        for (x,y,c) in app.coords:
            canvas.create_text(x,y, text = c, font = f'Arial 20 bold', fill = "#7d3cff" )
        canvas.create_text(10, 40, text = "Emoticon", anchor = "nw", font = "Forte 100 bold", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2, \
                                    text = f"Your Emotion that we detected is  {app.emotion}" ,font = "Serif 20 italic bold" , fill = "#7d3cff")
        canvas.create_text(app.width//2- 150, app.height//2 + 150, \
                                    text = "Press 'Enter' to continue" ,font = "Serif 13 italic" , fill = "#7d3cff")
        

    

            
    if app.mode == "chatting":
        #press "Tab" to exit back
        canvas.create_rectangle(0,0,app.width, app.height,  fill = "#7d3cff", outline =  "#7d3cff" )
        canvas.create_rectangle(0, 0.70*app.height, app.width,0.90*app.height, fill = "#fceed1")
        canvas.create_text(0.20*app.width, 0.75*app.height, text = app.mywords, fill = "black", font = "Serif 15 bold" ) #the typin thing that u are writing
        if app.messages != []:
            
            canvas.create_text(0.15*app.width,10 + app.extra, text = app.mess1, fill = "white", anchor = "w", font = "Serif 15 bold") #add the ovals
            if len(app.messages) >= 2:
                canvas.create_text(0.15*app.width,50 + app.extra, text = app.mess2, fill = "white", anchor = "w", font = "Serif 13 bold")
            if len(app.messages) >= 3:
                canvas.create_text(0.15*app.width,100 + app.extra, text = app.mess3, fill = "white", anchor = "w", font = "Serif 13 bold")
            if len(app.messages) >= 4:
                canvas.create_text(0.15*app.width,150 + app.extra, text = app.mess4, fill = "white", anchor = "w",font = "Serif 13 bold")
            if len(app.messages) >= 5:
                canvas.create_text(0.15*app.width,200 + app.extra, text = app.mess5, fill = "white", anchor = "w",font = "Serif 13 bold") 
            if len(app.messages) >= 6:
                canvas.create_text(0.15*app.width,250 + app.extra, text = app.mess6, fill = "white", anchor = "w", font = "Serif 13 bold")
    if app.received != []:
        canvas.create_text(0.85*app.width,10 + app.extra2, text = app.rec1, fill = "white", anchor = "e", font = "Serif 13 bold") #add the ovals
        if len(app.received) >= 2:
            canvas.create_text(0.85*app.width,50 + app.extra2, text = app.rec2, fill = "white", anchor = "e", font = "Serif 13 bold" )
        if len(app.received) >= 3:
            canvas.create_text(0.85*app.width,100 + app.extra2, text = app.rec3, fill = "white", anchor = "e", font = "Serif 13 bold")
        if len(app.received) >= 4:
            canvas.create_text(0.85*app.width,150 + app.extra2, text = app.rec4, fill = "white", anchor = "e", font = "Serif 13 bold")
        if len(app.received) >= 5:
            canvas.create_text(0.85*app.width,200 + app.extra2, text = app.rec5, fill = "white", anchor = "e", font = "Serif 13 bold") 
        if len(app.received) >= 6:
            canvas.create_text(0.85*app.width,250 + app.extra2, text = app.rec6, fill = "white", anchor = "e",font = "Serif 13 bold")

    if app.mode == "contradiction":
        background(app, canvas)
        canvas.create_text(10, 40, text = "Emoticon", anchor = "nw", font = "Forte 100 bold", fill = "#7d3cff")

        canvas.create_text(app.width//2 - 300, app.height//2, text = "Aahhh!!!" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2 + 60, text = "There is a confusion ;(" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 300, app.height//2 + 120, text = f"Your happiness Percentage, {app.happPerc} doesn't matches your emotion, {app.emotion}" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
        canvas.create_text(app.width//2 - 150, app.height//2 + 200, text =  "Forgive this poor technology and press 'Enter' to start again" ,font = "Serif 13" , anchor = "w", fill = "#7d3cff")
       
         
        
        
    
        


                 
runApp(width=1920, height=986)
# import everything from tkinter module
#from tkinter import *   
 
# create a tkinter window



