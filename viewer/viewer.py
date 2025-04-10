import streamlit as st
import time

from google.cloud import storage

storage_client = storage.Client()

GCS_BUCKET="lw-steam-night-images"

prev_file = ""

with st.empty():
    while True:
        files = []
        for blob in storage_client.list_blobs(GCS_BUCKET):
            if blob.name.startswith("2025-") and blob.name.endswith("jpg"):
                files.append(blob.name)
        new_file = max(files)
        if new_file == prev_file:
            print(f"Same file! {new_file}")
            time.sleep(5)
            continue
        print(f"new file! {new_file}")
        prev_file = new_file
        prompt = storage_client.bucket(GCS_BUCKET).blob(new_file.split(".")[0] + ".txt").download_as_string()
        with st.spinner("Loading a new creation!"):
            time.sleep(2)
        st.image(f"https://storage.googleapis.com/{GCS_BUCKET}/{new_file}", caption=prompt.decode())

print(files)