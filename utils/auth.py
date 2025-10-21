# utils/auth.py
import streamlit as st
from .firebase_config import initialize_firebase # Corrected relative import

firebase = initialize_firebase()
auth = firebase.auth()
db = firebase.database()

def sign_up(email, password, name):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        st.success("Account created successfully! Please log in.")
        
        user_data = {
            "name": name,
            "email": email,
            "plan": "free",
            "scenarios_used": 0
        }
        db.child("users").child(user['localId']).set(user_data)
        return user
    except Exception as e:
        st.error(f"Error: Could not create account. {e}")
        return None

def sign_in(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        user_profile = db.child("users").child(user['localId']).get().val()

        # --- THIS IS THE FIX ---
        # Check if the user profile was found in the database
        if user_profile:
            st.session_state['user'] = {
                'uid': user['localId'],
                'email': user['email'],
                'idToken': user['idToken'],
                'name': user_profile.get('name', 'User')
            }
            st.success(f"Welcome back, {user_profile.get('name', 'User')}!")
            return True
        else:
            # If no profile exists, show an error
            st.error("Authentication successful, but could not find user profile in the database.")
            return False
        # -----------------------

    except Exception as e:
        st.error(f"Login failed. Please check your email and password.")
        return False