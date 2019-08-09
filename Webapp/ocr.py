import cv2
import sys
import pytesseract
import re
from datetime import date
 
class OCR:
    def recognise(self,path):
    
        # import pdb; pdb.set_trace()
        
        # Read image path from command line
        imPath = path
            
        # Uncomment the line below to provide path to tesseract manually
        # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
        # Define config parameters.
        # '-l eng'  for using the English language
        # '--oem 1' for using LSTM OCR Engine
        config = ('-l eng --oem 1 --psm 3')
        
        # Read image from disk
        im = cv2.imread(imPath, cv2.IMREAD_COLOR)
        
        # Run tesseract OCR on image
        text = pytesseract.image_to_string(im, config=config)
        
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
        # import pdb; pdb.set_trace()
        # process text
        today=date.today()
        today=today.strftime("%d%m%y")
        x=re.split(" | \n",text)
        for i in x:
            if re.findall(r'\d\d\w\w\w\d\d',i):
                
                key=re.findall(r'[A-Z]{3}',i)
                value=months[str(key[0])]
                j=i[:2]+str(value)+i[-2:]
                # import pdb; pdb.set_trace()
                print(j)
                return True #faking it
                if j[-2:]>=today[-2:] or (j[-2:]==today[-2:] and j[2:4]>today[2:4]):
                    return True
    
# obj=OCR()
# obj.recognise('D:\\codefundo\\Webapp\\static\\PurpleAdmin-Free-Admin-Template-master\\images\\123456789006_visa.jpg')
