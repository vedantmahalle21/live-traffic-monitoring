import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import os
import errno
import json
import shutil

class DetectCar:
    def __init__(self):
        self.img_path = "Images"
        self.final_img_path = "Boxed_Images"
        self.areas_path = "areas.json"
        self.areas_dict = self.read_json(self.areas_path)
        self.areas = list(self.areas_dict.keys())
        self.img_data = self.read_json("img_data.json")

    def read_json(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data


    def detect_car_in_area(self, area):
        if os.path.exists(os.path.dirname(f'{self.final_img_path}/{area}/')):
                shutil.rmtree(f'{self.final_img_path}/{area}/')
        print(f"Running detection in area {self.areas_dict[area]}")
        num_cars = 0
        img_data_area = self.read_json(f"img_data_{area}.json")
        print(img_data_area)
        loc_img_path = os.path.join(self.img_path, area)
        loc_final_img_path = os.path.join(self.final_img_path, area)
        for filename in os.listdir(loc_img_path):
            img = cv2.imread(os.path.join(loc_img_path, filename))
            bbox, label, conf = cv.detect_common_objects(img)
            output_image = draw_bbox(img, bbox, label, conf)
            car_count = label.count('car')
            img_data_area['images'][filename]['car_count'] = car_count
            num_cars += car_count
            if not os.path.exists(os.path.dirname(os.path.join(loc_final_img_path, filename))):
                try:
                    os.makedirs(os.path.dirname(os.path.join(loc_final_img_path, filename)))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            cv2.imwrite(os.path.join(self.final_img_path, area, filename), output_image)
            print(f'Number of cars at location {img_data_area["images"][filename]["view"]} is '+ str(car_count))
            img_data_area['images'][filename]['boxed_img_file_path'] = os.path.join(self.final_img_path, area, filename)
        img_data_area['area_car_count'] = num_cars
        print(f' <----- Number of cars in area {self.areas_dict[area]} is -->'+ str(num_cars))
        with open(f"final_img_data_{area}.json", "w") as f:
            json.dump(img_data_area, f)


    def detect_car(self):
        if os.path.exists(os.path.dirname(f'{self.final_img_path}/')):
                shutil.rmtree(f'{self.final_img_path}/')
        for area in self.areas:
            print(f"Running detection in area {self.areas_dict[area]}")
            num_cars = 0
            loc_img_path = os.path.join(self.img_path, area)
            loc_final_img_path = os.path.join(self.final_img_path, area)
            for filename in os.listdir(loc_img_path):
                img = cv2.imread(os.path.join(loc_img_path, filename))
                bbox, label, conf = cv.detect_common_objects(img)
                output_image = draw_bbox(img, bbox, label, conf)
                car_count = label.count('car')
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
        with open("final_img_data.json", "w") as f:
            json.dump(self.img_data, f)


