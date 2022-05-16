import cv2
import cvlib as cv
import os
import errno
import json
import shutil
from detect_car_yolo import DetectCarYolo

class DetectCar:
    def __init__(self):
        self.img_path = "Images"
        self.final_img_path = "Boxed_Images"
        self.areas_path = "areas.json"
        self.areas_dict = self.read_json(self.areas_path)
        self.areas = list(self.areas_dict.keys())
        self.img_data = self.read_json("img_data.json")
        self.final_img_data_path = "final_img_data.json"

    def read_json(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data

    def detect_car_in_area(self, area):
        if os.path.exists(os.path.dirname(os.path.join(self.final_img_path, area, ""))):
                shutil.rmtree(os.path.join(self.final_img_path, area, ""))
        print(f"Running detection in area {self.areas_dict[area]}")
        img_data = self.read_json(self.final_img_data_path)
        img_data[area] = {}
        img_data[area]['images'] = {}
        num_cars = 0
        loc_img_path = os.path.join(self.img_path, area)
        loc_final_img_path = os.path.join(self.final_img_path, area)
        for filename in os.listdir(loc_img_path):
            img_data[area]['images'][filename] = {}
            img_data[area]['images'][filename]['area'] = self.areas_dict[area]
            img_data[area]['images'][filename]['view'] = self.img_data[area]['images'][filename]['view']
            img_data[area]['images'][filename]['img_file_path'] = self.img_data[area]['images'][filename]['img_file_path']
            img_data[area]['images'][filename]['timestamp'] = self.img_data[area]['images'][filename]['timestamp']
            yolo_detecter = DetectCarYolo()
            output_image, car_count = yolo_detecter.detect_car(os.path.join(loc_img_path, filename))  
            num_cars += car_count
            img_data[area]['images'][filename]['car_count'] = car_count
            if not os.path.exists(os.path.dirname(os.path.join(loc_final_img_path, filename))):
                try:
                    os.makedirs(os.path.dirname(os.path.join(loc_final_img_path, filename)))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            cv2.imwrite(os.path.join(self.final_img_path, area, filename), output_image)
            print(f'Number of cars at location {img_data[area]["images"][filename]["view"]} is '+ str(car_count))
            img_data[area]['images'][filename]['boxed_img_file_path'] = os.path.join(self.final_img_path, area, filename)
            
        img_data[area]['area_car_count'] = num_cars
        print(f'----- Number of cars in area {self.areas_dict[area]} is --- : '+ str(num_cars))
        with open(self.final_img_data_path, "w") as f:
            json.dump(img_data, f)


    def detect_car(self):
        for area in self.areas:
            if os.path.exists(os.path.dirname(os.path.join(self.final_img_path, area, ""))):
                shutil.rmtree(os.path.join(self.final_img_path, area, ""))
            print(f"Running detection in area {self.areas_dict[area]}")
            num_cars = 0
            loc_img_path = os.path.join(self.img_path, area)
            loc_final_img_path = os.path.join(self.final_img_path, area)
            for filename in os.listdir(loc_img_path):
                yolo_detecter = DetectCarYolo()
                output_image, car_count = yolo_detecter.detect_car(os.path.join(loc_img_path, filename))  
                num_cars += car_count
                self.img_data[area]['images'][filename]['car_count'] = car_count
                if not os.path.exists(os.path.dirname(os.path.join(loc_final_img_path, filename))):
                    try:
                        os.makedirs(os.path.dirname(os.path.join(loc_final_img_path, filename)))
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                cv2.imwrite(os.path.join(self.final_img_path, area, filename), output_image)
                print(f'Number of cars at location {self.img_data[area]["images"][filename]["view"]} is '+ str(car_count))
                self.img_data[area]['images'][filename]['boxed_img_file_path'] = os.path.join(self.final_img_path, area, filename)
            self.img_data[area]['area_car_count'] = num_cars
            print(f' <----- Number of cars in area {self.areas_dict[area]} is -->'+ str(num_cars))
            with open(self.final_img_data_path, "w") as f:
                json.dump(self.img_data, f)


