from PIL import ImageGrab
import cv2
import numpy as np
import ctypes
from box import Box

class ScreenRecorder:
    def __init__(self, windowName):
        
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        
        self.windowName = windowName
        self.frame = None
        self.box = Box((0,0), screensize)
        self.out = None
        
    def resizeWindow(self):        
        windowResolution = self.box.getResolution()
        cv2.resizeWindow(self.windowName, int(windowResolution[0]) , int(windowResolution[1]))
    
    def initializeWindow(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        self.resizeWindow()
        
    def captureScreenShot(self):
        if self.box is None:
            return ImageGrab.grab((), all_screens=True)
        
        return ImageGrab.grab(self.box.getBox(), all_screens=True)
    
    def captureNewFrame(self):     
        img = self.captureScreenShot()
        
        # Convert the screenshot to a numpy array
        frame = np.array(img)
        
        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Write it to the output file
        if self.out is not None:
            self.out.write(frame)
        
        cv2.imshow(self.windowName, frame)
        self.frame = frame
    
    def saveFrameToFile(self, filename):
        cv2.imwrite(filename, self.frame)

    def release(self):
        # Release the Video writer
        self.closeFileWriting()
        
        # Destroy all windows
        cv2.destroyAllWindows()
        
    def enableFileWriting(self, fileName: str):
        codec = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(fileName, codec, 60.0, self.box.getResolution())
    
    def closeFileWriting(self):
        if self.out is None:
            return
        
        self.out.release()
        self.out = None
            
    def isWindowOpen(self):
        return cv2.getWindowProperty(self.windowName, cv2.WND_PROP_VISIBLE) >= 1

    def setBox(self, box:Box):
        self.box = box
        
    def updatePointOfInterest(self, box:Box):
        self.setBox(box)
        self.resizeWindow()
        self.captureNewFrame()