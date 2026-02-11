import threading
import time

from mosaic_core import handlers
from mosaic_core import auto_configurer


class H1IMUStateDataChannel(handlers.data_channel.DataChannelSendable):
    def __init__(self, channel_name: str, h1_demo):
        super().__init__(channel_name)
        self.h1_demo = h1_demo
        self.running = True

        self.test_thread = threading.Thread(target=self._test_loop, daemon=True)
        self.test_thread.start()

    def _test_loop(self):
        while self.running:
            time.sleep(1)
            self.send_imu()

    def send_imu(self):
        if self.h1_demo is None:
            print("[H1 IMU State Channel] Warning: h1_demo is None, cannot send IMU data.")
            return
        imu_data = self.h1_demo.get_imu_data()
        if imu_data:
            self.send_json(imu_data)
            print(f"[H1 IMU State Channel] Sent IMU data: {imu_data}")
        else:
            print("[H1 IMU State Channel] Warning: No IMU data available to send.")


class H1IMUStateConnectorConfigurer(auto_configurer.ADCHandlerConfigurer):
    def __init__(self):
        super().__init__()
        self.h1_demo = None

    def set_h1_demo(self, h1_demo):
        self.h1_demo = h1_demo

    def get_connector_type(self) -> str:
        return "h1-imu-state"

    def configure(self):
        config = self.get_config()
        handler = H1IMUStateDataChannel(config.label, self.h1_demo)
        self.set_handler(handler)


class H1IMUStateConnectorConfigurerFactory(auto_configurer.IConfigurableConnectorFactory):
    def __init__(self):
        super().__init__()
        self.connector = None

    def create_connector(self):
        connector = H1IMUStateConnectorConfigurer()
        self.connector = connector
        return self.connector

    def get_connector_type(self) -> str:
        return "h1-imu-state"
