import cv2
from mtcnn.mtcnn import MTCNN
class Detector:
    def detection(self,img):
        detector = MTCNN()
        # cap = cv2.VideoCapture(0) #dont show logging of open cv
        # while True: 
            #Capture frame-by-frame
        # import pdb; pdb.set_trace()
        frame=cv2.imread(img,1)
        f1=frame
        #Use MTCNN to detect faces
        result = detector.detect_faces(frame)
        if result != []:
            return True
        return False

                

# obj=Detector()
# obj.detection()