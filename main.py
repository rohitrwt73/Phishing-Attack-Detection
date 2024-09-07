import threading
import requests
from flask import Flask, request, jsonify
import streamlit as st

app = Flask(__name__)

def check_phishing_url(url):
    return True 

@app.route('/check_url', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get("url")
    if url:
        is_legit = check_phishing_url(url)
        if is_legit:
            return jsonify({"status": "legit"})
        else:
            return jsonify({"status": "phishing"})
    return jsonify({"error": "No URL provided"}), 400

def run_flask():
    app.run(debug=False, use_reloader=False)

def run_streamlit():
    st.title("Phishing Attack Detection App")
    url = st.text_input("Enter a URL to check:")
    if st.button("Check URL"):
        if url:
            try:
                response = requests.post("http://127.0.0.1:5000/check_url", json={"url": url})
                result = response.json()
                if result["status"] == "legit":
                    st.success("✅ This URL is Legit!")
                else:
                    st.error("❌ This URL is Illegal (Phishing)!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_streamlit()