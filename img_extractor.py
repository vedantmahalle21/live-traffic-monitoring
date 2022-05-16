from time import time
from bs4 import BeautifulSoup
import requests
import os
import shutil
import errno
import json


class ImgExtractor:
    def __init__(self):
        self.area_data_path = "areas.json"
        self.areas_dict = self.read_json(self.area_data_path)
        self.areas = list(self.areas_dict.keys())
        self.img_path = "Images"
        self.img_data_path = "img_data.json"

    def read_json(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data

    def download_images(self, image_url, img_name, area):
        file_path = os.path.join(self.img_path, area, img_name)
        response = requests.get(image_url, stream=True)

        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    def get_img_list(self, area):
        html_page = requests.get(f"https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/{area}.html#trafficCameras")
        soup = BeautifulSoup(html_page.content, features="html.parser")

        images = []
        img_box = soup.find('div', class_="snapshots")
        timestamp_div =  img_box.find('div', class_="timestamp")
        timestamp = timestamp_div.find('span', class_="left").contents[0]

        for img in img_box.find_all('img'):
            images.append(("https:" + img.get('src'), area, img.get('alt'), timestamp))
        return images

    def extract_images_in_area(self, area):
        try:
            images_data = []
            if os.path.exists(os.path.dirname(os.path.join(self.img_path, area, ""))):
                shutil.rmtree(os.path.join(self.img_path, area, ""))
            
            print(f"Extracting image data from area {self.areas_dict[area]}")
            images_data = self.get_img_list(area)
            
            img_metadata = self.read_json(self.img_data_path)
            img_metadata[area] = {}
            img_metadata[area]['images'] = {}
            print("Downloading images")
            for image in images_data:
                img_filename = image[0].split("/")[-1]
                if img_filename != "nocamera.jpg":
                    img_metadata[image[1]]['images'][img_filename] = {}
                    img_metadata[image[1]]['images'][img_filename]['area'] = self.areas_dict[image[1]]
                    img_metadata[image[1]]['images'][img_filename]['view'] = image[2].replace("View from ", "")
                    img_metadata[image[1]]['images'][img_filename]['img_file_path'] = os.path.join(self.img_path, image[1], img_filename)
                    img_metadata[image[1]]['images'][img_filename]['timestamp'] = image[3]
                    self.download_images(image[0], img_filename, image[1])
            with open("img_data.json", "w") as f:
                json.dump(img_metadata, f)
        except Exception as ex:
            raise(ex)

    def extract_images(self):
        try:
            images_data = []
            
            for area in self.areas:
                if os.path.exists(os.path.dirname(os.path.join(self.img_path, area, ""))):
                    shutil.rmtree(os.path.join(self.img_path, area, ""))
                print(f"Extracting image data from area {self.areas_dict[area]}")
                images = self.get_img_list(area)
                images_data += images
            
            img_metadata = {}
            for area in self.areas:
                img_metadata[area] = {}
                img_metadata[area]['images'] = {}
            print("Downloading images")
            for image in images_data:
                img_name = image[0].split("/")[-1]
                if img_name != "nocamera.jpg":
                    img_metadata[image[1]]['images'][img_name] = {}
                    img_metadata[image[1]]['images'][img_name]['area'] = self.areas_dict[image[1]]
                    img_metadata[image[1]]['images'][img_name]['view'] = image[2].replace("View from ", "")
                    img_metadata[image[1]]['images'][img_name]['img_file_path'] = os.path.join(self.img_path, image[1], img_name)
                    img_metadata[image[1]]['images'][img_name]['timestamp'] = image[3]
                    self.download_images(image[0], img_name, image[1])
            with open("img_data.json", "w") as f:
                json.dump(img_metadata, f)
        except Exception as ex:
            raise(ex)
    
