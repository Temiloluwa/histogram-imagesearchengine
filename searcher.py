from featuredescriptor import ColorDescriptor 
import numpy as np
import argparse
import csv
import cv2

#construct argument parser for command line
args = argparse.ArgumentParser()
args.add_argument('-b','--bins', required = True, help = 'supply comma seperated values to indicate number of bins per channel')
args.add_argument('-d','--dataset', required = True, help = 'enter the path to the dataset containing images')
args.add_argument('-i','--img', required = True, help = 'path to image to be described with feature vectors')
args.add_argument('-f','--feat', required = True, help = 'enter the filename (ending in .csv) for storing feature vectors')
args = vars(args.parse_args())

class Searcher:
    def __init__(self,featVecPath,queryFeatVec,limit = 7):
        self.featVecPath = featVecPath
        self.queryFeatVec = queryFeatVec
        self.limit = limit
        
    def search(self):
        results = {}
        with open(self.featVecPath) as f:
            reader = csv.reader(f)
            for row in reader:
                feat = [float(x) for x in row[1:]]
                results[row[0]] = self.chi2Dis(self.queryFeatVec,feat)    
        f.close()
        result = sorted([(a,b) for (b,a) in results.items()])
        return result[:self.limit]
    
    def chi2Dis(self,histA,histB):
        return 0.5 * np.sum([self.chi2Opn(a,b) for (a,b) in zip(histA,histB)])
    
    def chi2Opn(self,a,b,eps=10-4):
        return ((a-b)**2/ (a + b + eps))
     

#create an instance of oject Color Descriptor
cd = ColorDescriptor(args['bins'],args['feat'],args['dataset'])
#Generate feature vectors and store in csv file
cd.featVecGen()
#return results of search performed
sh = Searcher(args['feat'], cd.describe(args['img']))
result = sh.search()
#initialize a variable for displaying the order in which the images appear
order = 0
for (a,b) in result:
    im = cv2.imread(b)
    #get dimensions of image
    (h,w) = im.shape[:2]
    h = int(h*0.1)
    w = int(w*0.1)
    #resize image
    im = cv2.resize(im,(w,h),interpolation = cv2.INTER_AREA)
    order += 1 
    b = 'Picture '+ str(order) + ': ' + b[(b.rfind('\\') + 1):]
    cv2.imshow(b,im)
cv2.waitKey(0)
cv2.destroyAllWindows()
    
    
