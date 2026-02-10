import threading
import time

from mosaic_core import handlers
from mosaic_core import auto_configurer


class H1DirectionDataChannel(handlers.data_channel.DataChannelJsonReceivable):
    def __init__(self, channel_name: str, h1_demo):
        super().__init__(channel_name)
        self.h1_demo = h1_demo
        self.running = True

        # 테스트용: 백그라운드 스레드에서 1초마다 handle_data 호출
        print(f"[H1DirectionDataChannel] Starting test loop for channel: {channel_name}")
        # self.test_thread = threading.Thread(target=self._test_loop, daemon=True)
        # self.test_thread.start()

    def _test_loop(self):
        """테스트용: 1초마다 handle_data 호출"""
        counter = 0
        while self.running:
            time.sleep(1)
            counter += 1
            test_data = {
                "lin_vel_x": 1.0,
                "ang_vel_yaw": 1.0
            }
            print(f"[Test Loop #{counter}] Sending test data: {test_data}")
            self.handle_data(test_data)

    def handle_data(self, data: dict):
        # Process the received data
        print(f"[H1 Direction Channel] Received data: {data}")
        # Add your custom processing logic here
        if self.h1_demo:
            self.h1_demo.from_mosaic_direction(data)
        else:
            print("[H1 Direction Channel] Warning: h1_demo is None, skipping...")


class H1DirectionConnectorConfigurer(auto_configurer.ADCHandlerConfigurer):
    def __init__(self):
        super().__init__()
        self.h1_demo = None  # H1ConnectorConfigurer 기능 직접 구현

    def set_h1_demo(self, h1_demo):
        self.h1_demo = h1_demo

    def get_connector_type(self) -> str:
        return "h1-direction"

    def configure(self):
        config = self.get_config()
        handler = H1DirectionDataChannel(config.label, self.h1_demo)
        self.set_handler(handler)


class H1DirectionConnectorConfigurerFactory(auto_configurer.IConfigurableConnectorFactory):
    def __init__(self):
        super().__init__()
        self.connector = None

    def create_connector(self):
        connector = H1DirectionConnectorConfigurer()
        self.connector = connector
        return self.connector

    def get_connector_type(self) -> str:
        return "h1-direction"
