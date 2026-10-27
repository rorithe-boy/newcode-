from pathlib import Path
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Khwezi Mining • Better Mining | Group 25", page_icon="⛏️", layout="wide")


# Load datasets

workers = pd.read_csv(r"Workers.csv")
equipment = pd.read_csv(r"Equipment.csv")
incidents = pd.read_csv(r"Incidents.csv")

# Bright Khwezi Mining design (no extra Python libraries needed)
st.markdown("""
<style>
.stApp {background:linear-gradient(145deg,#f0f8ff 0%,#f8fbff 50%,#fffaf0 100%);color:#172c45}
[data-testid="stHeader"] {background:rgba(240,248,255,.90)}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#10395d,#145c78)}
[data-testid="stSidebar"] * {color:#fff!important}
[data-testid="stSidebar"] [data-baseweb="radio"] label {padding:7px;border-radius:8px}
[data-testid="stSidebar"] [data-baseweb="radio"] label:hover {background:#287b98}
[data-testid="stMetric"] {background:white;border:1px solid #d9e8f4;border-radius:16px;padding:16px;box-shadow:0 5px 18px rgba(17,67,105,.08)}
[data-testid="stMetricLabel"] {color:#4d6481!important}
[data-testid="stMetricValue"] {color:#0d4c73!important}
h1,h2,h3 {color:#153e61!important}
.stButton button, .stDownloadButton button {background:#116fa1;color:white;border-radius:10px;border:0;font-weight:700}
.stButton button:hover, .stDownloadButton button:hover {background:#0b547c;color:white}
[data-testid="stDataFrame"] {border-radius:12px;overflow:hidden}
.khwezi-hero {background:linear-gradient(110deg,#126e9c,#1a91a9 60%,#f0b64b 150%);border-radius:22px;padding:30px 34px;margin:5px 0 25px;box-shadow:0 10px 30px rgba(18,110,156,.17)}
.khwezi-eyebrow {color:#d8f4ff;font-size:12px;letter-spacing:2px;font-weight:800}
.khwezi-title {color:white!important;font-size:clamp(32px,4vw,52px)!important;font-weight:900!important;margin:7px 0!important}
.khwezi-title span {color:#ffe08a}
.khwezi-subtitle {color:white;font-size:17px}
.khwezi-chip {display:inline-block;background:rgba(255,255,255,.18);color:white;border:1px solid #b9e9f4;border-radius:30px;padding:7px 15px;margin-top:14px;font-weight:700;font-size:12px}
.khwezi-footer {border-top:1px solid #c9dcea;margin-top:35px;padding-top:14px;text-align:center;color:#62788e;font-size:12px}
</style>
<div class="khwezi-hero">
 <div class="khwezi-eyebrow">⛏ KHWEZI MINING · DIGITAL OPERATIONS</div>
 <div class="khwezi-title">BETTER <span>MINING</span></div>
 <div class="khwezi-subtitle">Bright ideas for safer operations and smarter equipment decisions.</div>
 <div class="khwezi-chip">GROUP 25 · MINING SAFETY &amp; EQUIPMENT MONITORING</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("**⛏ KHWEZI MINING**  \nBETTER MINING · GROUP 25")

# User database 

users = {
    "admin": {"password": "Rorisang@8", "role": "Administrator"},
    "safety": {"password": "Tsaki@7", "role": "Safety Officer"},
    "engineer": {"password": "Fortune@5", "role": "Mining Engineer"},
    "maint": {"password": "Group25", "role": "Maintenance Engineer"},
    "manager": {"password": "Oluga@10", "role": "Manager"}
}

roles = {
    "Administrator": ["Dashboard", "Workers", "Incidents", "Equipment", "Risk Assessment", "Maintenance", "Analysis", "Reports"],
    "Safety Officer": ["Dashboard", "Workers", "Incidents", "Risk Assessment", "Reports"],
    "Mining Engineer": ["Dashboard", "Workers", "Incidents", "Equipment", "Risk Assessment", "Analysis", "Reports"],
    "Maintenance Engineer": ["Dashboard", "Equipment", "Maintenance", "Reports"],
    "Manager": ["Dashboard", "Workers", "Incidents", "Equipment", "Risk Assessment", "Analysis", "Reports"]
}


# Login Portal

st.sidebar.header("Login Portal")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

if login_button:
    if username in users and users[username]["password"] == password:
        st.session_state["role"] = users[username]["role"]
        st.sidebar.success(f"Welcome, {username}!")
    else:
        st.sidebar.error("Invalid username or password")

if "role" not in st.session_state:
    st.warning("Please log in to access the dashboard.")
    st.stop()

role = st.session_state["role"]
permissions = roles[role]

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.success("You have been logged out successfully.")
    st.stop()

# Sidebar Navigation

st.sidebar.title("Navigation")
menu_choice = st.sidebar.radio("Go to:", permissions)


#Calculations

total_workers = len(workers)
total_incidents = len(incidents)
near_misses = len(incidents[incidents["Type"] == "Near Miss"])
high_risk_obs = len(incidents[incidents["Severity"].isin(["High", "Critical"])])
ppe_compliance = (workers["PPE"].value_counts().get("Yes", 0) / total_workers) * 100 if total_workers else 0
total_equipment = len(equipment)
equipment_available = len(equipment[equipment["TruckStatus"] == "Available"])
equipment_maintenance = len(equipment[equipment["MaintenanceStatus"] == "Maintenance"])
equipment_alerts = len(equipment[equipment["Vibration"] > 8])
avg_availability = (equipment["OperatingHours"] / (equipment["OperatingHours"] + equipment["Downtime"])).mean() * 100
critical_alerts = len(equipment[equipment["Temperature"] > 100])

# Dashboard

if menu_choice == "Dashboard":
    st.header("Khwezi Mining | Operations Dashboard")
    st.subheader("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Workers", total_workers)
    col1.metric("Total Safety Incidents", total_incidents)
    col1.metric("Near Misses", near_misses)

    col2.metric("High-Risk Observations", high_risk_obs)
    col2.metric("PPE Compliance (%)", f"{ppe_compliance:.1f}")
    col2.metric("Total Equipment", total_equipment)

    col3.metric("Equipment Available", equipment_available)
    col3.metric("Under Maintenance", equipment_maintenance)
    col3.metric("Equipment Alerts", equipment_alerts)

    
    st.markdown("### 📊 Live mining overview")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Incidents by severity")
        if not incidents.empty:
            st.bar_chart(incidents["Severity"].value_counts(), color="#ec8b55")
        else:
            st.info("No incidents recorded")
        st.markdown("#### Worker PPE compliance")
        if not workers.empty:
            st.bar_chart(workers["PPE"].value_counts(), color="#20a8a1")
    with right:
        st.markdown("#### Equipment maintenance status")
        if not equipment.empty:
            st.bar_chart(equipment["MaintenanceStatus"].value_counts(), color="#318ad1")
        st.markdown("#### Incidents by department")
        if not incidents.empty:
            st.bar_chart(incidents["Department"].value_counts(), color="#e5b04a")


# Worker Safety

elif menu_choice == "Workers":
    st.header("Khwezi Mining | Worker Safety")
    st.dataframe(workers)
    unsafe = workers[(workers["PPE"] == "No") | (workers["Fatigue"] >= 4)]
    if not unsafe.empty:
        st.warning(f"Unsafe workers detected: {len(unsafe)}")
    st.dataframe(unsafe)
    st.markdown("### 📊 Worker safety graphics")
    left, right = st.columns(2)
    with left:
        if not workers.empty:
            st.bar_chart(workers["PPE"].value_counts(), color="#1da9a1")
    with right:
        if not workers.empty:
            st.bar_chart(workers["Fatigue"].value_counts().sort_index(), color="#e9a64c")




# Safety Incident Database

elif menu_choice == "Incidents":
    st.header("Khwezi Mining | Incident Register")
    st.subheader("Central repository for recording and analyzing safety incidents")

    
    st.dataframe(incidents)

    # --- Add new incident ---
    st.markdown("###  Add New Incident")
    with st.form("add_incident_form"):
        incident_id = st.text_input("Incident ID")
        date = st.date_input("Date")
        time = st.time_input("Time")
        shift = st.selectbox("Shift", ["Day", "Night"])
        location = st.text_input("Location")
        department = st.selectbox("Department", ["Drilling", "Hauling", "Maintenance", "Processing", "Exploration"])
        incident_type = st.selectbox("Incident Type", ["Near Miss", "Slip/Trip", "Fire", "Explosion", "Vehicle Collision", "Equipment Failure", "Mechanical Failure", "Chemical Spill"])
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        injury_status = st.selectbox("Injury Status", ["None", "Minor", "Major"])
        lost_time = st.selectbox("Lost-Time Injury", ["No", "Yes"])
        cause = st.text_input("Cause")
        corrective_action = st.text_input("Corrective Action")
        status = st.selectbox("Incident Status", ["Open", "Closed"])
        submitted = st.form_submit_button("Add Incident")

        if submitted:
            new_row = {
                "IncidentID": incident_id,
                "Date": date,
                "Time": time,
                "Shift": shift,
                "Location": location,
                "Department": department,
                "Type": incident_type,
                "Severity": severity,
                "InjuryStatus": injury_status,
                "LostTimeInjury": lost_time,
                "Cause": cause,
                "CorrectiveAction": corrective_action,
                "Status": status
            }
            incidents = pd.concat([incidents, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Incident {incident_id} added successfully!")

    # Search and Filter
    st.markdown("###  Search and Filter Incidents")
    search_term = st.text_input("Search by Incident ID, Type, or Department")
    severity_filter = st.multiselect("Filter by Severity", incidents["Severity"].unique())
    status_filter = st.multiselect("Filter by Status", incidents["Status"].unique())

    filtered = incidents.copy()
    if search_term:
        filtered = filtered[
            filtered.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)
        ]
    if severity_filter:
        filtered = filtered[filtered["Severity"].isin(severity_filter)]
    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]

    st.dataframe(filtered)

    # Categorize and Count 
    st.markdown("Incident Summary")
    total_incidents = len(incidents)
    open_incidents = len(incidents[incidents["Status"] == "Open"])
    closed_incidents = len(incidents[incidents["Status"] == "Closed"])
    critical_incidents = len(incidents[incidents["Severity"] == "Critical"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", total_incidents)
    col2.metric("Open Incidents", open_incidents)
    col3.metric("Closed Incidents", closed_incidents)
    col4.metric("Critical Incidents", critical_incidents)
    st.markdown("### 📊 Incident insights")
    left, right = st.columns(2)
    with left:
        if not incidents.empty:
            st.bar_chart(incidents["Type"].value_counts(), color="#298ed1")
    with right:
        if not incidents.empty:
            st.bar_chart(incidents["Severity"].value_counts(), color="#f1a356")


    
# Equipment Monitoring

elif menu_choice == "Equipment":
    st.header("Khwezi Mining | Equipment Monitoring")
    st.dataframe(equipment)

    def check_condition(row):
        if row["Temperature"] > 100 or row["Vibration"] > 8:
            return "CRITICAL"
        elif row["Temperature"] > 80 or row["Vibration"] > 5:
            return "WARNING"
        else:
            return "NORMAL"

    equipment["Status"] = equipment.apply(check_condition, axis=1)
    st.dataframe(equipment[["EquipID", "Type", "Temperature", "Vibration", "Status"]])
    st.markdown("### 📈 Equipment condition charts")
    a, b = st.columns(2)
    with a:
        st.markdown("#### Temperature (°C)")
        st.bar_chart(equipment.set_index("EquipID")["Temperature"], color="#f39c62")
    with b:
        st.markdown("#### Vibration (mm/s)")
        st.bar_chart(equipment.set_index("EquipID")["Vibration"], color="#2d91cf")
    st.markdown("#### Equipment condition summary")
    st.bar_chart(equipment["Status"].value_counts(), color="#23b2a0")



# Risk Assessment
elif menu_choice == "Risk Assessment":
    st.header("Khwezi Mining | Risk Assessment")
    likelihood = st.slider("Likelihood (1-5)", 1, 5, 3)
    consequence = st.slider("Consequence (1-5)", 1, 5, 3)
    risk_score = likelihood * consequence

    if risk_score <= 4:
        st.success(f"Risk Score: {risk_score} → LOW")
    elif risk_score <= 9:
        st.warning(f"Risk Score: {risk_score} → MEDIUM")
    elif risk_score <= 16:
        st.error(f"Risk Score: {risk_score} → HIGH")
    else:
        st.error(f"Risk Score: {risk_score} → CRITICAL ")


# Maintenance

elif menu_choice == "Maintenance":
    st.header("Khwezi Mining | Maintenance")
    equipment["Availability"] = (equipment["OperatingHours"] / (equipment["OperatingHours"] + equipment["Downtime"])) * 100
    st.dataframe(equipment[["EquipID", "Type", "Availability"]])
    low_avail = equipment[equipment["Availability"] < 80]
    if not low_avail.empty:
        st.warning(f"Equipment with low availability: {len(low_avail)}")
    
    due_maintenance = equipment[equipment["MaintenanceStatus"].isin(["Due", "Maintenance"])]
    overdue_equipment = equipment[equipment["MaintenanceStatus"] == "Critical"]
    excessive_downtime = equipment[equipment["Downtime"] > 200]
    low_availability = equipment[equipment["Availability"] < 85]
    repeated_alerts = equipment[equipment["Vibration"] > 8]

    
    st.markdown("Maintenance Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Due for Maintenance", len(due_maintenance))
    col2.metric("Overdue Equipment", len(overdue_equipment))
    col3.metric("Under Maintenance", len(equipment[equipment["MaintenanceStatus"] == "Maintenance"]))
    col4.metric("Excessive Downtime", len(excessive_downtime))
    col5.metric("Low Availability", len(low_availability))
    st.markdown("### 📊 Maintenance performance")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Equipment availability (%)")
        st.bar_chart(equipment.set_index("EquipID")["Availability"], color="#21a9a1")
    with right:
        st.markdown("#### Downtime by equipment")
        st.bar_chart(equipment.set_index("EquipID")["Downtime"], color="#efab53")


# Interactive Analysis

elif menu_choice == "Analysis":
    st.header("Khwezi Mining | Operational Analysis")
    analysis_option = st.selectbox(
        "Select a business question:",
        [
            "Which department has the highest number of incidents?",
            "Which shift records the most incidents?",
            "What percentage of workers comply with PPE requirements?",
            "Which equipment has the highest downtime?",
            "Which equipment has the lowest availability?",
            "Which equipment requires maintenance?",
            "Which incident types occur most frequently?",
            "How many incidents are classified as high or critical?",
        ]
    )

    if analysis_option == "Which department has the highest number of incidents?":
        dept_counts = incidents["Department"].value_counts()
        st.bar_chart(dept_counts)
        st.write("Department with highest incidents:", dept_counts.idxmax())

    elif analysis_option == "Which shift records the most incidents?":
        shift_counts = incidents["Shift"].value_counts()
        st.bar_chart(shift_counts)
        st.write("Shift with most incidents:", shift_counts.idxmax())

    elif analysis_option == "What percentage of workers comply with PPE requirements?":
        ppe_compliance = (workers["PPE"].value_counts().get("Yes", 0) / len(workers)) * 100 if len(workers) else 0
        st.metric("PPE Compliance (%)", f"{ppe_compliance:.1f}%")

    elif analysis_option == "Which equipment has the highest downtime?":
        max_downtime = equipment.loc[equipment["Downtime"].idxmax()]
        st.write("Equipment with highest downtime:", max_downtime["EquipID"], "-", max_downtime["Type"])

    elif analysis_option == "Which equipment has the lowest availability?":
        equipment["Availability"] = (equipment["OperatingHours"] / (equipment["OperatingHours"] + equipment["Downtime"])) * 100
        min_avail = equipment.loc[equipment["Availability"].idxmin()]
        st.write("Lowest availability:", min_avail["EquipID"], "-", min_avail["Type"], f"({min_avail['Availability']:.1f}%)")

    elif analysis_option == "Which equipment requires maintenance?":
        maintenance_eq = equipment[equipment["MaintenanceStatus"] == "Maintenance"]
        st.dataframe(maintenance_eq)

    elif analysis_option == "Which incident types occur most frequently?":
        type_counts = incidents["Type"].value_counts()
        st.bar_chart(type_counts)
        st.write("Most frequent incident type:", type_counts.idxmax())

    elif analysis_option == "How many incidents are classified as high or critical?":
        critical_incidents = incidents[incidents["Severity"].isin(["High", "Critical"])]
        st.metric("High/Critical Incidents", len(critical_incidents))

# Reports

elif menu_choice == "Reports":
    st.header("Khwezi Mining | Summary Reports")

    
    
    summary = pd.DataFrame({
        "Indicator": [
            "Total Workers",
            "Total Incidents",
            "Near Misses",
            "High/Critical Incidents",
            "PPE Compliance (%)",
            "Total Equipment",
            "Available Equipment",
            "Under Maintenance",
            "Equipment Alerts (Vibration > 8)",
            "Average Availability (%)",
            "Critical Temperature Alerts (>100°C)"
        ],
        "Value": [
            total_workers,
            total_incidents,
            near_misses,
            high_risk_obs,
            round(ppe_compliance, 1),
            total_equipment,
            equipment_available,
            equipment_maintenance,
            equipment_alerts,
            round(avg_availability, 1),
            critical_alerts
        ]
    })

    st.dataframe(summary, use_container_width=True)

    # --- Export Option ---
    csv = summary.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Summary Report (CSV)",
        data=csv,
        file_name="mining_monitoring_summary.csv",
        mime="text/csv"
    )

# Project identity footer
st.markdown("""<div class="khwezi-footer">KHWEZI MINING &nbsp;•&nbsp; BETTER MINING &nbsp;•&nbsp; GROUP 25<br>Mining Safety and Equipment Monitoring System | Student Project Prototype</div>""", unsafe_allow_html=True)
