from enum import Enum
import json
import os

class KeyBoardBindings:
    class Binding(Enum):
        PAUSE="PAUSE"
        QUIT="QUIT"
        NEWBOX="NEWBOX"
        SAVE="SAVE"
        NEWTHRESHOLD="NEWTHRESHOLD"
    
    
    def __init__(self, filePath:str=None):
        self.keyBindings = self.loadKeyBindings(filePath)
        
        
    def loadKeyBindings(self, filePath:str=None):
        if filePath is None:
            return self.getDefaultKeyBindings()
        
        if not os.path.exists(filePath):
            print('file doesnt exist!\nLoading default bindings')
            return self.getDefaultKeyBindings()
        
        return self.loadKeyBindingsFromFile(filePath)
        
    def loadKeyBindingsFromFile(self, filePath:str):
        file = open(filePath)
        data = json.load(file)
        file.close()
        
        return data    
    
    def getDefaultKeyBindings(self):
        keyBindings = {}
        keyBindings[self.Binding.PAUSE.value] = 'p,P'
        keyBindings[self.Binding.QUIT.value] = 'q,Q'
        keyBindings[self.Binding.NEWBOX.value] = 'b,B'
        keyBindings[self.Binding.SAVE.value] = 's,S'
        keyBindings[self.Binding.NEWTHRESHOLD.value] = 't,T'
        return keyBindings
    
    def isKey(self, key: int, expected:Binding):
        binding = self.keyBindings.get(expected.value)
        
        if binding is None:
            return
        
        firstChar, secondChar = binding.split(',')
        
        if key == ord(firstChar):
            return True
        
        return key == ord(secondChar)
    
    
