from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for

import json
import sys
import torch, torchvision
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms

app = Flask(__name__)

@app.route("/api/v1.0/process_img", methods=["POST"])
def csharp_python_restfulapi_json():
    """
    simple c# test to call python restful api web service
    """
    try:  
        # get request json object
        request_json = request.get_json()      
        
        # convert to response json object 
        response = jsonify(request_json)
        response.status_code = 200  
    except:
        exception_message = sys.exc_info()[1]
        response = json.dumps({"content":exception_message})
        response.status_code = 400
    return response


if __name__ == "__main__":
    app.run(debug=True)
