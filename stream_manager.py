import streamlit as st
import cv2


class StreamManager:
    def __init__(self):
        if 'streams' not in st.session_state:
            st.session_state.streams = []
        if 'stream_placeholders' not in st.session_state:
            st.session_state.stream_placeholders = {}
        if 'stream_names' not in st.session_state:
            st.session_state.stream_names = {}

    def add_stream(self, stream_url, stream_name):
        if stream_url not in st.session_state.streams:
            st.session_state.streams.append(stream_url)
            st.session_state.stream_names[stream_url] = stream_name
            st.session_state.stream_placeholders[stream_url] = st.empty()

    def remove_stream(self, stream_url):
        if stream_url in st.session_state.streams:
            st.session_state.streams.remove(stream_url)
            if stream_url in st.session_state.stream_names:
                del st.session_state.stream_names[stream_url]
            if stream_url in st.session_state.stream_placeholders:
                st.session_state.stream_placeholders[stream_url].empty()
                del st.session_state.stream_placeholders[stream_url]

    def display_streams(self):
        cols = st.columns(3)
        for i, stream_url in enumerate(st.session_state.streams):
            with cols[i % 3]:
                stream_name = st.session_state.stream_names.get(stream_url, "Unnamed Stream")
                st.subheader(f"{stream_name} ({stream_url})")
                if stream_url not in st.session_state.stream_placeholders:
                    st.session_state.stream_placeholders[stream_url] = st.empty()
                self._update_single_stream(stream_url)

    def _update_single_stream(self, stream_url):
        vid_cap = cv2.VideoCapture(stream_url)
        st_frame = st.empty()
        while vid_cap.isOpened():
            success, image = vid_cap.read()
            if success:
                image = cv2.resize(image, (720, int(720*(9/16))))
                st_frame.image(
                    image,
                    caption='Detected Video',
                    channels="BGR",
                    use_column_width=True
                )
            else:
                st_frame.warning("Failed to read from stream")
                vid_cap.release()
                break

        if not vid_cap.isOpened():
            st_frame.warning("Failed to connect to stream")
