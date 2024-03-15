#!/bin/python
import speedtest

def run_speed_test():
    # Create speedtest object
    st = speedtest.Speedtest()
    # Get download speed in Mbps
    download_speed = st.download() / 1_000_000
    # Get upload speed in Mbps
    upload_speed = st.upload() / 1_000_000
    print(f"upload speed {upload_speed} and download speed is {download_speed}")
run_speed_test()