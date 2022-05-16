from traffic_monitor import TrafficMonitor

if __name__=="__main__":
    try:
        traffic_monitor = TrafficMonitor()
        traffic_monitor.traffic_monitoring_process()
        print("Traffic Detection")
    except Exception as e:
        raise(e)