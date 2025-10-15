# 🩺 Symptom Checker – Agent-Based Health Assistant

An intelligent health assistant powered by a multi-agent system built with Crew AI and Streamlit. This application analyzes user-described symptoms, identifies potential conditions, and provides structured, AI-generated advice in a clean, user-friendly interface.

------

## ☁️ Deployment

This application is deployed and publicly accessible via Streamlit Community Cloud.

[Live App Link ](https://symptom-checker-agents-6ydzmaxdrayxq5d9czlf6n.streamlit.app/)
-----


## ✨ Features

  * **Multi-Agent System**: Utilizes a sophisticated backend with specialized AI agents for symptom classification, condition matching, advice generation, and reporting.
  * **Intuitive UI**: A clean and elegant interface built with Streamlit, designed for ease of use.
  * **Dynamic Analysis**: Get instant analysis by describing your symptoms in natural language.
  * **Polished Reports**: View the results in beautifully styled summary cards.
  * **PDF Export**: Download a professional, well-formatted PDF of your health report for your records.

-----

## 🔧 Tech Stack & Architecture

This project leverages a modern stack to create an agent-based system.

  * **Backend**: Python, Crew AI
  * **Frontend**: Streamlit
  * **PDF Generation**: FPDF2
  * **Agents**:
      * **Symptom Classifier Agent**: Parses user input to identify key medical symptoms.
      * **Condition Matcher Agent**: Maps the identified symptoms to a database of potential health conditions.
      * **Advice Agent**: Generates contextual advice and detailed analysis based on the user's input.
      * **Report Agent**: Aggregates the findings from other agents and formats the final, user-facing report.

-----

## 🚀 How to Run Locally

To get this project running on your local machine, follow these steps.

1. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit App:**

    ```bash
    streamlit run streamlit_app.py
    ```

-----

## 🎯 Project Goals

This project was developed to practice and master several key concepts:

  * Orchestrating a multi-agent system using Crew AI.
  * Building a polished, interactive web application with Streamlit.
  * Integrating multiple components into a cohesive, end-to-end application.
  * Applying modern UI/UX principles to data-driven applications.
