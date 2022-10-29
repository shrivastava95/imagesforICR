import os
import requests
import json
import base64
import config
from restful_api_image_subclass import RESTfulAPIImageSubclass
        
def main():
    try:
        restful_api_image_subclass = RESTfulAPIImageSubclass()
#         get image path and name
        project_directory_path = os.path.dirname(os.path.realpath(__file__))                
        image_path_name = os.path.join(project_directory_path, config.IMAGE_TYPE_1)
#         get image base64 encode from file path and name
        with open(image_path_name, "rb") as image_file_read:
            image_bytes_string = image_file_read.read()
#        base64 byte encoding
        image_base64_encode = base64.encodebytes(image_bytes_string)                        
        image_file_read.close()        
#         post http request                
        url = config.URL_IMAGE_CLASSIFICATION_BASE64_ENCODING
        headers = {"content-type":config.HEADERS_IMAGE_TIF}
#         get and print request for testing
        request = requests.post(url, data=image_base64_encode, headers=headers) 
        result = request.json()   
        print(request, result)         
    except:
        restful_api_image_subclass.print_exception_message()
          
if __name__ == '__main__':
    main()