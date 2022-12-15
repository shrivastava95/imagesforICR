from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for

import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt


import json
import sys
import torch, torchvision
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms

from utils import ICRclassifier, timeit


save_path = "model_state_dict.pt"

# # save
# model_scripted = torch.jit.script(model) # Export to TorchScript
# model_scripted.save(save_path) # Save

# load
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# load model from state dict
print('model loading...')
model = ICRclassifier()
model.load_state_dict(torch.load(save_path), strict=False)
model = model.to(device)
print('model loaded.')
# model.eval()

img_size = 32
print('loading image transforms...')
tfms = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Resize([img_size, img_size]),
    # transforms.Normalize()
])
print('loaded image transforms...')

@timeit
def classify_b64(image_b64):
    image_bytes = base64.b64decode(image_b64)   # im_bytes is a binary image
    image_file = BytesIO(image_bytes)  # convert image to file-like object
    image_PIL = Image.open(image_file)   # img is now PIL Image object

    image = tfms(image_PIL)
    image = image.unsqueeze(0)
    image = image.to(device)
    scores = model(image)
    preds = scores.argmax(dim=1)
    return preds


@timeit
def classify_PIL(image_PIL):
    image = tfms(image_PIL)
    image = image.unsqueeze(0)
    image = image.to(device)
    scores = model(image)
    preds = scores.argmax(dim=1)
    return preds

@timeit
def b64_to_PIL(image_b64):
    image_bytes = base64.b64decode(image_b64)   # im_bytes is a binary image
    image_file = BytesIO(image_bytes)  # convert image to file-like object
    image_PIL = Image.open(image_file)   # img is now PIL Image object
    return image_PIL

app = Flask(__name__)

@app.route("/api/v1.0/process_img", methods=["POST"])
def process_img_post():
    
    global model
    try:  
        request_json = request.get_json() 

        # for debugging - remove later
        with open('request_test.json', 'w') as out_file:
            json.dump(request_json, out_file)

        ############

        # read the image from payload
        image_b64 = request_json['content']

        # # convert image to PIL and classify
        image_PIL = b64_to_PIL(image_b64)
        image_pred = classify_PIL(image_PIL)
        # image_pred = classify_b64(image_b64)

        # add predictions to response JSON object
        print('preds:', image_pred)
        pred_list = [f'{i}' for i in image_pred]
        request_json['message'] = ''.join(pred_list)
        request_json['content'] = ''
        print(request_json)

        # # do something....
        # plt.imshow(image)
        # plt.show()

        

        
        ############
        # convert to response json object 
        response = jsonify(request_json)

        # get request object
        response.status_code = 200  

    except:
        exception_message = sys.exc_info()[1]
        response = json.dumps({"content":exception_message})
        response.status_code = 400

    return response


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
