import cv2
import numpy as np
from enum import Enum
import os

from snipTool import SnipToolFactory
from screenRecorder import ScreenRecorder
from keyBoard import KeyBoardBindings
from dialogService import DialogService

class App:    
    class AppState(Enum):
        PAUSE = 1
        EXIT = 2
        RUNNING = 3
    
    def __init__(self):
        self.recorder = ScreenRecorder('Live')
        self.snipToolFactory = SnipToolFactory()
        self.keyBoardBindings = KeyBoardBindings('bindings.json')
        self.dialogService = DialogService()
        
        self.state = self.AppState.RUNNING
        self.threshold = 6.0
        self.prevFrame = None
        self.baseFilePath = "./../images"
    
    def start(self):
        box = self.getNewBoxFromSnipTool()
        self.recorder.setBox(box)
        self.recorder.initializeWindow()
        
        while self.state != self.AppState.EXIT:                
            self.mainLoop()
        
        self.onClose()
    
    def mainLoop(self):
        wasAppPaused = self.isApplicationPaused()
        
        key = self.getKeyPressed()
        self.handleKeyActions(key)            
        
        if self.state == self.AppState.EXIT:
            return
        
        #when prev state was PAUSE we force in our application to campture a new frame
        #so we will skip that cycle probably didnt change that much
        if wasAppPaused or self.isApplicationPaused():
            return
        
        self.preRefreshAction()
        
        self.updateScreen()
        
        self.postRefreshAction()
    
    def preRefreshAction(self):
        self.prevFrame = self.getCurrentFrame()

    def postRefreshAction(self):
        if not self.hasGreatDiff(self.prevFrame, self.getCurrentFrame()):
            return
        
        self.state = self.AppState.PAUSE
        self.prevFrame = None

    def hasGreatDiff(self, prevFrame, currentFrame):
        if prevFrame is None:
            return False
        
        prevGray = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)
        currentGray = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)
        
        frameDiff = cv2.absdiff(prevGray, currentGray)
        
        hist = cv2.calcHist([frameDiff], [0], None, [256], [0, 256])
        hist = hist / np.sum(hist)
        
        entropy = -np.sum(hist * np.log2(hist + (hist == 0)))
        
        return entropy > self.threshold

    def handleKeyActions(self, key: int):
        if not self.recorder.isWindowOpen():
            self.state = self.AppState.EXIT
            return
        
        #255 when nothing is pressed
        if key == 255:
            return
        
        if self.keyBoardBindings.isKey(key, self.keyBoardBindings.Binding.PAUSE):
            self.handlePauseAction()
            return
            
        if self.keyBoardBindings.isKey(key, self.keyBoardBindings.Binding.NEWBOX):
            self.handleChangeBoxAction()
            return
        
        if self.keyBoardBindings.isKey(key, self.keyBoardBindings.Binding.SAVE) and self.recorder.frame is not None:
            self.handleSaveFrameAction()
            return        
        
        if self.keyBoardBindings.isKey(key, self.keyBoardBindings.Binding.NEWTHRESHOLD):
            self.handleThresholdChoiceAction()
            return
        
        if self.keyBoardBindings.isKey(key, self.keyBoardBindings.Binding.QUIT):
            self.state = self.AppState.EXIT
            return
    
    def handleSaveFrameAction(self):
        success, fileName = self.dialogService.getFileNameFromDialog()    
            
        if not success:
            return
        
        basePath = self.baseFilePath
        path = f"{basePath}/{fileName}"
        
        if not os.path.exists(basePath):
            os.mkdir(basePath)
        
        if not os.path.exists(path):
            self.recorder.saveFrameToFile(path)
            return
        
        users_response = self.dialogService.askFoundDuplicateFile()
        if users_response == 'no':
            return
        
        self.recorder.saveFrameToFile(path)
            
    
    def handlePauseAction(self):
        if self.state == self.AppState.RUNNING:
            self.state = self.AppState.PAUSE
            return
        
        self.updateScreen()
        self.state = self.AppState.RUNNING
        
    def handleThresholdChoiceAction(self):
        success, user_response = self.dialogService.chooseThresholdFromDialog(self.threshold)
        
        if not success:
            return
        
        self.threshold = user_response
    
    def getNewBoxFromSnipTool(self):
        return self.snipToolFactory.createNewSnip()
        
    def handleChangeBoxAction(self):
        box = self.getNewBoxFromSnipTool()
        self.recorder.updatePointOfInterest(box)
    
    def getKeyPressed(self):
        return cv2.waitKey(1) & 0xFF
    
    def updateScreen(self):     
        self.recorder.captureNewFrame()
    
    def onClose(self):
        self.recorder.release()
        
    def isApplicationPaused(self):
        return self.state == self.AppState.PAUSE
    
    def getCurrentFrame(self):
        return self.recorder.frame

def main():    
    app = App()
    app.start()
        
        
if __name__ == '__main__':
    main()