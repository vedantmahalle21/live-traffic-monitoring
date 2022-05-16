from img_extractor import ImgExtractor
from car_detection import DetectCar
from traffic_monitor import TrafficMonitor

if __name__=="__main__":
    try:
        traffic_monitor = TrafficMonitor()
        traffic_monitor.traffic_monitoring_process()
        print("Traffic Detection")
        # img_ext = ImgExtractor()
        # img_ext.extract_images()
        # det = DetectCar()
        # det.detect_car()

    except Exception as e:
        raise(e)