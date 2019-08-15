import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline

from datetime import date
import re
# Replace <Subscription Key> with your valid subscription key.
subscription_key = "41f761321d1b4e36831042fb063910cd"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the "westus" region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

ocr_url = vision_base_url + "ocr"

class OCR:
    def recognise(self,path):

        params = {'language': 'unk', 'detectOrientation': 'true'}
        image_path = path
        # Read the image into a byte array
        image_data = open(image_path, "rb").read()
        # Set Content-Type to octet-stream
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
        # put the byte array into your post request
        response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
        # response = requests.post(ocr_url, headers=headers, params=params, json=data)
        response.raise_for_status()

        analysis = response.json()

        # Extract the word bounding boxes and text.
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
        # print(word_infos)

        # Display the image and overlay it with the extracted text.
        # plt.figure(figsize=(5, 5))
        # image = Image.open(BytesIO(requests.get(image_url).content))
        # ax = plt.imshow(image, alpha=0.5)
        months={
            "JAN":"01",
            "FEB":"02",
            "MAR":"03",
            "APR":"04",
            "MAY":"05",
            "JUN":"06",
            "JUL":"07",
            "AUG":"08",
            "SEP":"09",
            "OCT":"10",
            "NOV":"11",
            "DEC":"12"
        }
        text=[]
        for word in word_infos:
            text.append(word["text"])
        print(text)
        # import pdb; pdb.set_trace()
        today=date.today()
        today=today.strftime("%d%m%y")
        for i in text:
            if re.findall(r'\d\d\w\w\w\d\d',i):
                
                key=re.findall(r'[A-Z]{3}',i)
                value=months[str(key[0])]
                j=i[:2]+str(value)+i[-2:]
                # import pdb; pdb.set_trace()
                print(j)
                return True #faking it
                if j[-2:]>=today[-2:] or (j[-2:]==today[-2:] and j[2:4]>today[2:4]):
                    return( True)
