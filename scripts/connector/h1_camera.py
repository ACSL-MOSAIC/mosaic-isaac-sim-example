import threading
import time

from mosaic_core import handlers
from mosaic_core import auto_configurer


class H1CameraMediaTrack(handlers.media_track.AMediaTrackHandler):
    def __init__(self, track_name: str, h1_demo):
        super().__init__(track_name, False)
        self.h1_demo = h1_demo
        self._thread = None

    def start(self):
        if self.is_running():
            print(f"[H1CameraMediaTrack] Channel {self.get_channel_name()} is already running.")
            return

        self.set_running(True)
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        if not self.is_running():
            print(f"[H1CameraMediaTrack] Channel {self.get_channel_name()} is not running.")
            return

        self.set_stop_flag(True)
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self.set_running(False)

    def _loop(self):
        """테스트용: 1초마다 handle_data 호출"""
        while self.get_stop_flag():
            time.sleep(0.1)  # 0.1 초 대기 (10Hz)
            image = self.h1_demo.get_camera_image()
            if image is not None:
                self.send_frame(image)


class H1CameraConnectorConfigurer(auto_configurer.AMTHandlerConfigurer):
    def __init__(self):
        super().__init__()
        self.h1_demo = None

    def set_h1_demo(self, h1_demo):
        self.h1_demo = h1_demo

    def get_connector_type(self) -> str:
        return "h1-camera"

    def configure(self):
        config = self.get_config()
        handler = H1CameraMediaTrack(config.label, self.h1_demo)
        self.set_handler(handler)


class H1CameraConnectorConfigurerFactory(auto_configurer.IConfigurableConnectorFactory):
    def __init__(self):
        super().__init__()
        self.connector = None

    def create_connector(self):
        connector = H1CameraConnectorConfigurer()
        self.connector = connector
        return self.connector

    def get_connector_type(self) -> str:
        return "h1-camera"
