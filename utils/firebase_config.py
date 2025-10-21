# firebase_config.py
import streamlit as st
import pyrebase

def initialize_firebase():
    """
    Initializes and returns the Pyrebase app object.
    """
    config = {
        "apiKey": st.secrets["firebase_config"]["apiKey"],
        "authDomain": st.secrets["firebase_config"]["authDomain"],
        "projectId": st.secrets["firebase_config"]["projectId"],
        "storageBucket": st.secrets["firebase_config"]["storageBucket"],
        "messagingSenderId": st.secrets["firebase_config"]["messagingSenderId"],
        "appId": st.secrets["firebase_config"]["appId"],
        "databaseURL": st.secrets["firebase_config"]["databaseURL"],
    }

    try:
        firebase = pyrebase.initialize_app(config)
        print("Firebase Initialized Successfully.")
        return firebase
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        st.error("Failed to initialize Firebase connection.")
        return None