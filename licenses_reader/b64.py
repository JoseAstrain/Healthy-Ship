from PIL import Image
from io import BytesIO
import re
import time
import base64
import os.path
from licenses_reader.prueba2 import recognize_text
import cv2
import logging
import uuid



OUTPUT_FOLDER = "D:\\Hackaton 2020\\Healthy-Ship\\licenses_reader\\licenses"

class Converter:


    def getPNGFromBase64(codec, image_path=os.path.join(OUTPUT_FOLDER)):
        """Function that converts a string to image and send it to the CNN model 

            Parameters:
            codec (string): image coded on base64
            image_path (string): directory from image file

            Returns:
            string: string reconized by the model
            print(getPNGFromBase64.doc)
        """
        imageId = str(uuid.uuid1()) + ".png";
        text_cap = "N/A"
        if(codec != ""):
            base64_data = re.sub('^data:image/.+;base64,', '', codec)
            byte_data = base64.b64decode(base64_data.replace(" ", "+"))
            image_data = BytesIO(byte_data)
            img = Image.open(image_data)
            img.save(os.path.join(OUTPUT_FOLDER, imageId))
            if(os.path.isfile(os.path.join(OUTPUT_FOLDER, imageId))):
                text_cap = recognize_text(os.path.join(OUTPUT_FOLDER, imageId))
                logging.info('Imagen descifrada exitosamente')
        else:
            logging.warning('El string de la imagen es incorrecto')
        return text_cap