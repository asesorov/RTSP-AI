import streamlit as st
from stream_manager import StreamManager
from settings import SettingsManager


class RTSPStreamViewer:
    def __init__(self):
        self.stream_manager = StreamManager()
        self.settings_manager = SettingsManager(self.stream_manager)

    def run(self):
        st.set_page_config(page_title="RTSP Stream Viewer", layout="wide")
        st.title("RTSP Stream Viewer")

        with st.sidebar:
            self.settings_manager.show_settings()
        self.stream_manager.display_streams()

if __name__ == "__main__":
    app = RTSPStreamViewer()
    app.run()
