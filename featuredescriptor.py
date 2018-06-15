import numpy as np
import cv2
import glob


class ColorDescriptor:
    def __init__(self,bins,featVecPath,dataSetPath):
        #number of bins
        self.bins = tuple([int(b) for b in bins.split(',')])
        self.featVecPath = featVecPath
        self.dataSetPath = dataSetPath
        
    def describe(self,imgPath):
        #convert image to HSV color space
        #generate feature vector
        img = cv2.imread(imgPath)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        features = []
        
        #get image dimensions
        #compute the image center
        (h,w) = img.shape[:2]
        (cX,cY) = (int(w*0.5),int(h*0.5))
        
        #divide the image into rectanglar segments to create spatial localization
        segments = [(0,cX,0,cY),(cX,w,0,cY),(0,cX,cY,h),(cX,w,cY,h)]
        
        #construct and elliptical mask around image center
        (Xaxes,Yaxes) = (int(w*0.75)//2, int(h*0.75)//2)
        ellipMask = np.zeros(img.shape[:2], dtype = 'uint8')
        cv2.ellipse(ellipMask, (cX,cY), (Xaxes,Yaxes), 0,0,360, 255,-1)
        
        #loop over segments
        for (startX, endX, startY, endY) in segments:
            #construct mask for each segment
            #subtract elliptical mask from each segment mask
            cornerMask = np.zeros(img.shape[:2], dtype = 'uint8')
            cv2.rectangle(cornerMask,(startX,endX),(endX,endY),255,-1)
            cornerMask = cv2.subtract(cornerMask,ellipMask)
            
            #extract 3D color histogram
            #create feature vector with histogram
            hist = self.histogram(img,cornerMask)
            features.extend(hist)
        hist = self.histogram(img,ellipMask)
        features.extend(hist)    
        return features
    
    #compute 3D histogram
    #[0,180,0,256,0,256] ranges used because of HSV color model
    def histogram(self,img,mask):
        hist = cv2.calcHist([img],[0,1,2],mask,self.bins,[0,180,0,256,0,256])
        hist = cv2.normalize(hist,hist).flatten()
        return hist
    
    #open a file to write feature vectors
    #read every image in data set
    #write feature vectors to file
    def featVecGen(self):
        featVec = open(self.featVecPath,'w')
        imagePaths = glob.glob(self.dataSetPath + '\*.jpg')
        for imgPath in imagePaths:
            feat = self.describe(imgPath)
            feat = [str(f) for f in feat]
            featVec.write('{},{}\n'.format(imgPath,','.join(feat)))
        featVec.close()
        

            
            
            
            
         
            
            
            
            