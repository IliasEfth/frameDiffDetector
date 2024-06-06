# frameDiffDetector
 A python screen recorder app that can detect differencies between two frames. In order to decide if we found an acceptable difference between the last two frames, we use the entropy to calculate the randomnes.
# Install packages
pip install opencv-python\
pip install numpy\
pip install enum\
pip install tk\
pip install pillow\
pip install ctypes
# Usage
When the program starts it asks from the user to draw a rectangle in order to crop the screenshot in those coordinates.\
After that the program is checking those coordinates for rapid changes based on entropy. The threshold can be changed from the user with the properly key binding.\
Currently the default threshold is 6.0
# Keyboard bindings
The keyboard bindings can be found and altered from bindings.json file.\
User can choose for the first and secondary option with the format as shown bellow.
```
{
    "PAUSE": "p,P",
    "QUIT": "q,Q",
    "NEWBOX": "b,B",
    "SAVE": "s,S",
    "NEWTHRESHOLD": "t,T"
}
```
