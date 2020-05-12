### Server
import socket
from threading import *
import socket
import pygame
import pygame.camera
from pygame.locals import *
import cv2

###заменить способ доступа к камере vidcapture не кросссплатформенный

def server():
#########################ORIGINAL#####################################
#    try:
#    	print ("\nServer started at " + str(socket.gethostbyname(socket.gethostname())) + " at port " + str(90)	)
#    	port = 90
#    	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    	serversocket.bind(("",port))
#    	serversocket.listen(10)
#    	pygame.camera.init()
#    	cam = pygame.camera.Camera(0,(640,480),"RGB")
#    	cam.start()
#    	img = pygame.Surface((640,480))
#    	while (True):
#    		connection, address = serversocket.accept()
#    		print ("GOT_CONNECTION")
#    		cam.get_image(img)
#    		data = pygame.image.tostring(img,"RGB")
#    		connection.sendall(data)
#    		connection.close()
#    except:
#    	pass

##########################TEMP########################################

#    print ("\nServer started at " + str(socket.gethostbyname(socket.gethostname())) + " at port " + str(90)	)
#    port = 90
#    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    serversocket.bind(("",port))
#    serversocket.listen(10)
#    pygame.camera.init()
#    cam = pygame.camera.Camera(0,(640,480),"RGB")
#    cam.start()
#    img = pygame.Surface((640,480))
#    while (True):
#    	connection, address = serversocket.accept()
#    	print ("GOT_CONNECTION")
#    	cam.get_image(img)
#    	data = pygame.image.tostring(img,"RGB")
#    	connection.sendall(data)
#    	connection.close()

###################################MY#################################
    
    print ("\nServer started at " + str(socket.gethostbyname(socket.gethostname())) + " at port " + str(90)	)
    port = 90
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #serversocket.bind(('',port))
    serversocket.bind((socket.gethostname(),port))
    serversocket.listen(10)
    
    #pygame.camera.init()
    #cam = pygame.camera.Camera(0,(640,480),"RGB")
    #cam.start()
    #img = pygame.Surface((640,480))

    capture=cv2.VideoCapture(0) #!!!

    while (True):
    	connection, address = serversocket.accept()
    	print ("GOT_CONNECTION")
    	#cam.get_image(img)
    	#data = pygame.image.tostring(img,"RGB")
    	ret, frame = capture.read() #!!!
    	#new
    	#frame=str(frame).encode('utf-8')
    	print(frame)
    	connection.sendall(bytes(str(frame), 'utf-8'))#data
    	connection.close()
    
server()
