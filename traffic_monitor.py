from enum import Flag
import streamlit as st
import json
import pandas as pd
from traitlets import default

from img_extractor import ImgExtractor
from car_detection import DetectCar

class TrafficMonitor:
    def __init__(self):
        self.areas_path = "areas.json"
        self.areas_dict = self.read_json(self.areas_path)
        self.img_data_path = "final_img_data.json"
        
    def read_json(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data

    def run_monitoring_for_area(self):
        area = st.session_state.areas
        for key, value in self.areas_dict.items():
                if value == area:
                    area_value = key
        st.header('Wait live detection is running')
        print("Starting traffic monitoring system")
        img_extractor = ImgExtractor()
        print("Extracting traffic images")
        img_extractor.extract_images_in_area(area_value)
        print("Extraction complete")
        car_detector = DetectCar()
        print("Starting Traffic Detection")
        car_detector.detect_car_in_area(area_value)
        self.traffic_monitor_area(area_value)



    def traffic_monitoring_process(self):
        st.title('Live Traffic Monitoring System around Singapore')
        if st.button('Run Traffic Detection System'):
            st.header('Wait live detection is running')
            print("Starting traffic monitoring system")
            img_extractor = ImgExtractor()
            print("Extracting traffic images")
            img_extractor.extract_images()
            print("Extraction complete")
            car_detector = DetectCar()
            print("Starting Traffic Detection")
            car_detector.detect_car()
        # if st.button('Run Traffic Detection System in an Area'):
        #     options = list(self.areas_dict.values())
        #     options.insert(0, 'select')
        #     option = st.selectbox("Select area to run traffic detection system", key="areas", options=options, on_change=self.run_monitoring_for_area)
        #     st.write(f"Running Detection for {option}")  
        self.traffic_monitor()

    def traffic_monitor(self):
        img_data = self.read_json(self.img_data_path)
        df = pd.DataFrame(
            {
                "Area": [self.areas_dict[x] for x in img_data],
                "Car count":  [img_data[x]['area_car_count'] for x in img_data]
            })
        hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(df)
        option = st.selectbox("Select area to get detailed info",
                    options=self.areas_dict.values(), key="area")
        for key, value in self.areas_dict.items():
            if value == option:
                area_value = key
        df = pd.DataFrame(data=[img_data[area_value]['images'][x]['car_count'] for x in img_data[area_value]['images']], 
                                index=[img_data[area_value]['images'][x]['view'] for x in img_data[area_value]['images']],
                                columns=['No of cars'])
        

        for image in img_data[area_value]['images']:
            st.write(f"Timestamp: {img_data[area_value]['images'][image]['timestamp']}")
            cols = st.columns(3) 
            cols[0].text(img_data[area_value]['images'][image]['view'])
            cols[1].text(f"No of cars {img_data[area_value]['images'][image]['car_count']}")
            cols[2].image(img_data[area_value]['images'][image]['boxed_img_file_path'], use_column_width=True) 

    def traffic_monitor_area(self, area):
        img_data = self.read_json(self.img_data_path)
        st.write(f'No of cars in area {self.areas_dict[area]} is {img_data[area]["area_car_count"]}')

        for image in img_data[area]['images']:
            cols = st.columns(3)
            cols[0].text(img_data[area]['images'][image]['view'])
            cols[1].text(f"No of cars {img_data[area]['images'][image]['car_count']} <br> Timestamp: {img_data[area]['images'][image]['timestamp']}")
            cols[2].image(img_data[area]['images'][image]['boxed_img_file_path'], use_column_width=True) 
