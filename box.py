class Box:
    def __init__(self, topleftPoint, bottomRightPoint):
        self.topleftPoint = topleftPoint
        self.bottomRightPoint = bottomRightPoint

    def getBox(self):
        return self.topleftPoint + self.bottomRightPoint
    
    def isPoint(self):
        resolution = self.getResolution()
        
        return resolution[0] == 0 and resolution[1] == 0
    
    def getResolution(self):
        x = self.bottomRightPoint[0] - self.topleftPoint[0]
        y = self.bottomRightPoint[1] - self.topleftPoint[1]
        return (x, y)