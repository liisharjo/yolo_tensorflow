from PIL import Image
import os

location = 'SPIGa'

for file_name in os.listdir('/Users/liisharjo/Documents/' + location):
    if file_name.endswith('.JPG'):
        img = Image.open('/Users/liisharjo/Documents/' + location + '/' + file_name)
        img = img.resize((448, 448), Image.ANTIALIAS)
        img.save('/Users/liisharjo/Documents/s' + location + '/' + file_name)
