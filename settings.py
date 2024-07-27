import streamlit as st


class SettingsManager:
    def __init__(self, stream_manager):
        self.stream_manager = stream_manager
        if 'show_settings' not in st.session_state:
            st.session_state.show_settings = False
        if 'temp_stream_url' not in st.session_state:
            st.session_state.temp_stream_url = ""
        if 'temp_stream_name' not in st.session_state:
            st.session_state.temp_stream_name = ""

    def show_settings(self):
        if st.button("Toggle Settings"):
            st.session_state.show_settings = not st.session_state.show_settings
            st.rerun()

        if st.session_state.show_settings:
            st.subheader("Stream Settings")

            st.write("Add new stream:")
            input_method = st.radio("Input method", ("Parameters", "Full URL"))

            stream_name = st.text_input("Stream Name")

            if input_method == "Parameters":
                with st.form(key='add_stream_params'):
                    ip = st.text_input("IP")
                    port = st.text_input("Port")
                    path = st.text_input("Path")
                    username = st.text_input("Username (optional)")
                    password = st.text_input("Password (optional)", type="password")
                    submit_button = st.form_submit_button(label='Add Stream')

                if submit_button:
                    url = f"rtsp://{username}:{password}@{ip}:{port}{path}" if username and password else f"rtsp://{ip}:{port}{path}"
                    st.session_state.temp_stream_url = url
                    st.session_state.temp_stream_name = stream_name
            else:
                with st.form(key='add_stream_url'):
                    url = st.text_input("Full RTSP URL")
                    submit_button = st.form_submit_button(label='Add Stream')

                if submit_button:
                    st.session_state.temp_stream_url = url
                    st.session_state.temp_stream_name = stream_name

            if st.session_state.temp_stream_url and st.session_state.temp_stream_name:
                self.stream_manager.add_stream(st.session_state.temp_stream_url, st.session_state.temp_stream_name)
                st.success(f"Stream added: {st.session_state.temp_stream_name} ({st.session_state.temp_stream_url})")
                st.session_state.temp_stream_url = ""
                st.session_state.temp_stream_name = ""

            st.write("Remove existing streams:")
            for stream in st.session_state.streams:
                col1, col2 = st.columns([3, 1])
                col1.write(f"{st.session_state.stream_names.get(stream, 'Unnamed Stream')} ({stream})")
                if col2.button(f"Remove", key=f"remove_{stream}"):
                    self.stream_manager.remove_stream(stream)
                    st.success(f"Stream removed: {st.session_state.stream_names.get(stream, 'Unnamed Stream')}")
                    st.rerun()
