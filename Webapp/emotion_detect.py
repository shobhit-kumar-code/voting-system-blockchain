import requests
#from PIL import Image
#from io import BytesIO
#import os

# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline

class Emotion_Detector:
    def detect(self,img):
        # Replace <Subscription Key`> with your valid subscription key.
        subscription_key = "2f562fb2571f4be1b0bd1911b33028f1" #DSFace API

        # Set image path from local file.
        # image_path = path#os.path.join('D:\\codefundo\\Webapp\\visaSample1.jpg')

        assert subscription_key

        # You must use the same region in your REST call as you used to get your
        # subscription keys. For example, if you got your subscription keys from
        # westus, replace "westcentralus" in the URI below with "westus".
        #
        # Free trial subscription keys are generated in the westcentralus region.
        # If you use a free trial subscription key, you shouldn't need to change
        # this region.
        face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

        image_data = img #open(image_path, "rb")

        headers = {'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
            'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
        }

        response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
        response.raise_for_status()
        faces = response.json() 
        if len(faces)!=1:
            return False
        # import pdb; pdb.set_trace()
        emotion_map=faces[0]['faceAttributes']['emotion']
        max,emotion=0,''
        
        for key,val in emotion_map.items():
            if val>max:
                max=val
                emotion=key
        if emotion=='fear' or emotion=='sadness' or emotion=='surprise':
            return False
        return True
# obj=Emotion_Detector()
# image=open("D:\\codefundo\\Webapp\\static\\PurpleAdmin-Free-Admin-Template-master\\images\\fear.jpg",'rb')
# print(obj.detect(image))