import tkinter as tk
from tkinter import simpledialog, messagebox

class DialogService:
    def __init__(self):
        pass
    
    def chooseThresholdFromDialog(self, initialvalue:float=None):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        usersInput = simpledialog.askfloat("Change threshold", "threshold value:", initialvalue=initialvalue)
        root.destroy()
        
        if usersInput:
            return True, usersInput
        
        return False, usersInput
    
    def getFileNameFromDialog(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        usersInput = simpledialog.askstring("Save image as", "file name:", initialvalue='dog.png')
        root.destroy()
        
        if usersInput:
            return True, usersInput
        
        return False, usersInput
    
    def askFoundDuplicateFile(self):
        usersResponse = messagebox.askquestion("HOLD UP.. DONT MOVE", 'Found a path thats existing! Are you sure you want to continue with this action?', icon='warning')
        return usersResponse