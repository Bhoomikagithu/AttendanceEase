import streamlit as st
import os
import pandas as pd
import time
import subprocess
# Import backend functions
from Attendance_Backend import markAttendance

# --- Streamlit Config ---
st.set_page_config(page_title="Face Recognition Attendance", layout="wide")

# --- Custom CSS for full-height sidebar and always-visible expander content ---
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #181829;
        color: #fff;
    }
    .stSidebar {
        background-color: #23233b !important;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 20px;
        box-shadow: 2px 0 12px #ff69b4;
        min-width: 320px;
        max-width: 350px;
        transition: left 0.3s;
        padding-right: 0.5rem !important;
        height: 100vh !important;
        min-height: 100vh !important;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .sidebar-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
    }
    .sidebar-logo img {
        border-radius: 50%;
        border: 3px solid #ff69b4;
        width: 80px;
        height: 80px;
        margin-right: 0.5rem;
        box-shadow: 0 0 10px #ff69b4;
    }
    .sidebar-title {
        color: #ff69b4;
        font-size: 1.7rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1.2rem;
        letter-spacing: 1px;
    }
    .sidebar-section-label {
        color: #ff69b4;
        font-size: 1.15rem;
        font-weight: bold;
        margin: 1.1em 0 0.2em 0.2em;
        letter-spacing: 0.5px;
    }
    .stExpander {
        border-radius: 12px !important;
        border: 2px solid #ff69b4 !important;
        margin-bottom: 1.2rem !important;
        background: #292944 !important;
        padding: 0.5rem 0.7rem 0.7rem 0.7rem !important;
    }
    .stExpanderHeader {
        color: #ff69b4 !important;
        font-weight: bold !important;
        font-size: 1.25rem !important;
        letter-spacing: 0.5px;
        padding: 0.4em 0.7em 0.4em 0.7em !important;
        background: #23233b !important;
        border-radius: 8px !important;
        margin-bottom: 0.2em !important;
        border: 1.5px solid #ff69b4 !important;
        box-shadow: 0 0 8px #ff69b4;
        opacity: 1 !important;
    }
    /* Expander content always visible and readable */
    .stExpanderContent {
        background: #23233b !important;
        color: #fff !important;
        border-radius: 8px !important;
        padding: 0.7em 0.7em 0.7em 0.7em !important;
        font-size: 1.08rem;
    }
    .stButton>button, .stTextInput>div>input, .stFileUploader>div>div {
        border-color: #ff69b4;
        color: #ff69b4;
        border-radius: 8px;
        font-size: 1.1rem;
    }
    .stButton>button {
        background-color: #2c2c3a;
        transition: background 0.2s, color 0.2s;
        font-size: 1.1rem;
        padding: 0.6em 1.2em;
    }
    .stButton>button:hover {
        background-color: #ff69b4;
        color: #fff;
        box-shadow: 0 0 8px #ff69b4;
    }
    .stDataFrame, .stTable {
        background-color: #23233b !important;
        border-radius: 12px;
        border: 2px solid #ff69b4;
        box-shadow: 0 0 10px #ff69b4;
        font-size: 1.1rem;
    }
    .main-card {
        background: #23233b;
        border-radius: 18px;
        box-shadow: 0 0 18px #ff69b4;
        padding: 2rem 2.5rem 2rem 2.5rem;
        margin-bottom: 2rem;
    }
    .webcam-status {
        color: #ff69b4;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar Toggle ---
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = False

with st.container():
    if st.button("☰ Menu", key="open_sidebar", help="Open sidebar"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open

# --- Sidebar Content ---
if st.session_state.sidebar_open:
    with st.sidebar:
        st.markdown('<div class="sidebar-logo"><img src="https://img.icons8.com/color/96/000000/face-id.png" alt="logo"/><span class="sidebar-title">Smart Attendance</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-label">📤 Add / Upload New Student</div>', unsafe_allow_html=True)
        with st.expander("Add Student", expanded=True):
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="upload")
            student_name = st.text_input("Enter Student Name", key="student")
            if st.button("Add Student", key="add_student"):
                if uploaded_file is not None and student_name.strip() != "":
                    file_path = os.path.join('Students', f"{student_name.strip().upper()}.jpg")
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.read())
                    st.success(f"✅ {student_name} added successfully! Please refresh to update.")
                else:
                    st.warning("⚠️ Please provide both image and name.")
        st.markdown('<div class="sidebar-section-label">📄 View Attendance</div>', unsafe_allow_html=True)
        with st.expander("View Attendance", expanded=False):
            if os.path.exists("Attendance.csv"):
                df = pd.read_csv("Attendance.csv")
                if not df.empty:
                    st.dataframe(df.style.set_properties(**{
                        'background-color': '#1e1e1e',
                        'color': 'white',
                        'border-color': '#ff69b4'
                    }))
                else:
                    st.info("No attendance data yet.")
            else:
                st.info("No attendance data yet.")
        st.markdown('<div class="sidebar-section-label">👤 Manually Mark Attendance</div>', unsafe_allow_html=True)
        with st.expander("Mark Manually", expanded=False):
            manual_name = st.text_input("Enter Name to Mark Attendance", key="manual")
            if st.button("Mark Manually", key="mark_manual"):
                if manual_name.strip() != "":
                    markAttendance(manual_name.strip().upper())
                    st.success(f"{manual_name} marked successfully!")
                else:
                    st.warning("Enter a valid name!")

# --- Main Area ---
st.markdown("<h1 style='color:#ff69b4; text-align:center; margin-bottom:0.5em;'>📸 Face Recognition Attendance System</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#ff69b4;'>Webcam Controls</h2>", unsafe_allow_html=True)
if "webcam_process" not in st.session_state:
    st.session_state.webcam_process = None
if "cam_active" not in st.session_state:
    st.session_state.cam_active = False

col1, col2 = st.columns([1,1])
with col1:
    start = st.button("▶️ Start Webcam", key="start_webcam")
with col2:
    stop = st.button("⏹ Stop Webcam", key="stop_webcam")

if start and st.session_state.webcam_process is None:
    proc = subprocess.Popen([
        "python", "-c", "from Attendance_Backend import run_webcam_recognition; run_webcam_recognition()"
    ])
    st.session_state.webcam_process = proc
    st.session_state.cam_active = True
    st.markdown("<div class='webcam-status'>Webcam started. Please check the separate webcam window.</div>", unsafe_allow_html=True)

if stop and st.session_state.webcam_process is not None:
    st.session_state.webcam_process.terminate()
    st.session_state.webcam_process = None
    st.session_state.cam_active = False
    st.markdown("<div class='webcam-status'>✅ Webcam stopped.</div>", unsafe_allow_html=True)

if st.session_state.cam_active:
    st.markdown("<div class='webcam-status'>Webcam and face recognition are handled by the backend. Please check the separate webcam window.</div>", unsafe_allow_html=True)
    time.sleep(1)
st.markdown("</div>", unsafe_allow_html=True) 