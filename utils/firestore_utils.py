# utils/firestore_utils.py
import streamlit as st
from .firebase_config import initialize_firebase
from datetime import datetime
from collections import Counter

firebase = initialize_firebase()
db = firebase.database()

def save_report_to_history(user_id, id_token, report_data):
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_data['timestamp'] = timestamp
        db.child("users").child(user_id).child("history").push(report_data, token=id_token)
        return True
    except Exception as e:
        st.error(f"Error saving report: {e}")
        return False

def get_user_history(user_id, id_token, is_pro: bool = False):
    try:
        history = db.child("users").child(user_id).child("history").get(token=id_token).val()
        if not history:
            return []
        
        # Create a list of reports, but add the unique key to each one
        history_list = []
        for unique_key, report_data in history.items():
            report_data['unique_id'] = unique_key
            history_list.append(report_data)
        
        # Sort by the timestamp field, descending
        sorted_history = sorted(history_list, key=lambda x: x['timestamp'], reverse=True)

        if not is_pro:
            return sorted_history[:5]
        
        return sorted_history
    
    except Exception as e:
        st.error(f"Error fetching history: {e}")
        return []

def delete_history_item(user_id, id_token, unique_report_key):
    try:
        db.child("users").child(user_id).child("history").child(unique_report_key).remove(token=id_token)
        st.success("History item deleted.")
        return True
    except Exception as e:
        st.error(f"Error deleting item: {e}")
        return False

def get_user_profile(user_id, id_token):
    try:
        return db.child("users").child(user_id).get(token=id_token).val()
    except Exception as e:
        st.error(f"Error fetching user profile: {e}")
        return {}

def update_user_profile(user_id, id_token, data):
    try:
        db.child("users").child(user_id).update(data, token=id_token)
        return True
    except Exception as e:
        st.error(f"Failed to update profile: {e}")
        return False
    
def analyze_history_trends(history_list: list):
    """
    Analyzes a user's report history to find trends.
    Returns both a list of text insights and a dictionary of symptom counts.
    """
    if not history_list or len(history_list) < 2:
        # Return empty data for both insights and chart
        return ["Not enough history to generate trends."], None

    all_symptoms = []
    for report in history_list:
        symptoms_str = report.get("Identified Symptoms", "")
        symptoms = [s.strip() for s in symptoms_str.split(',') if s.strip() and s.strip() != "unspecified symptom"]
        all_symptoms.extend(symptoms)

    if not all_symptoms:
        return ["No specific symptoms were identified in your recent history."], None

    # Count the occurrences of each symptom
    symptom_counts = Counter(all_symptoms)
    
    # Generate text insights
    insights = []
    total_reports = len(history_list)
    most_common = symptom_counts.most_common(1)[0]
    insights.append(
        f"Your most frequently reported symptom is **'{most_common[0]}'**, appearing in **{most_common[1]}** of your last {total_reports} reports."
    )
    
    return insights, symptom_counts