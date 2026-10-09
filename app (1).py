import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="SwasthyaSetu",
    page_icon="🏥",
    layout="wide"
)

# -----------------------------
# SAMPLE HOSPITAL DATABASE
# -----------------------------
hospitals = pd.DataFrame([
    {
        "Hospital": "District Government Hospital",
        "District": "Belagavi",
        "Distance": 18,
        "Type": "Government",
        "Services": "Dialysis, Cardiology, General Medicine, X-Ray, Blood Test",
        "Specialists": "Nephrologist, Cardiologist",
        "Timing": "24 Hours",
        "Emergency": "Yes"
    },
    {
        "Hospital": "Rural Government Hospital",
        "District": "Belagavi",
        "Distance": 27,
        "Type": "Government",
        "Services": "Dialysis, General Medicine, Blood Test",
        "Specialists": "Nephrologist",
        "Timing": "8 AM - 6 PM",
        "Emergency": "Yes"
    },
    {
        "Hospital": "Primary Health Centre",
        "District": "Belagavi",
        "Distance": 6,
        "Type": "Government",
        "Services": "General Medicine, Blood Test, First Aid",
        "Specialists": "General Physician",
        "Timing": "9 AM - 4 PM",
        "Emergency": "No"
    },
    {
        "Hospital": "Taluk Government Hospital",
        "District": "Belagavi",
        "Distance": 12,
        "Type": "Government",
        "Services": "General Medicine, Cardiology, X-Ray, Blood Test",
        "Specialists": "Cardiologist, General Physician",
        "Timing": "9 AM - 5 PM",
        "Emergency": "Yes"
    }
])

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "search" not in st.session_state:
    st.session_state.search = ""

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("🏥SwasthyaSetu")

    st.caption("Rural Healthcare Access Platform")

    st.divider()

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

    if st.button("🔎 Find Hospital", use_container_width=True):
        st.session_state.page = "Find Hospital"

    if st.button("👨‍⚕️ Find Specialist", use_container_width=True):
        st.session_state.page = "Find Specialist"

    if st.button("📅 Appointments", use_container_width=True):
        st.session_state.page = "Appointments"

    if st.button("📋 My Health Record", use_container_width=True):
        st.session_state.page = "Health Record"

    if st.button("🔄 Referral Status", use_container_width=True):
        st.session_state.page = "Referral"

    st.divider()

    st.subheader("📡 Connectivity")

    st.success("Online")

    st.caption("Offline mode can be added for low-network areas.")

    st.divider()

    language = st.selectbox(
        "🌐 Language",
        ["English", "Kannada", "Hindi", "Marathi"]
    )


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    st.title("👋 Welcome to SwasthyaSetu")

    st.subheader(
        "Find the right healthcare service at the right time."
    )

    st.write(
        "Healthcare access designed for rural and underserved communities."
    )

    st.divider()

    # Search
    st.subheader("🔎 What healthcare service do you need?")

    search = st.text_input(
        "Describe your requirement",
        placeholder='Example: "I need dialysis"',
        label_visibility="collapsed"
    )

    if st.button("🔍 Search Healthcare", type="primary"):

        if search.strip():

            st.session_state.search = search
            st.session_state.page = "Find Hospital"
            st.rerun()

        else:
            st.warning("Please enter your healthcare requirement.")

    st.divider()

    # Quick services
    st.subheader("⚡ Quick Services")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏥\nFind Hospital", use_container_width=True):
            st.session_state.page = "Find Hospital"
            st.rerun()

    with col2:
        if st.button("👨‍⚕️\nFind Specialist", use_container_width=True):
            st.session_state.page = "Find Specialist"
            st.rerun()

    with col3:
        if st.button("📅\nBook Appointment", use_container_width=True):
            st.session_state.page = "Appointments"
            st.rerun()

    with col4:
        if st.button("📋\nHealth Record", use_container_width=True):
            st.session_state.page = "Health Record"
            st.rerun()

    st.divider()

    # Emergency
    st.error("🚑 Emergency?")

    st.write(
        "If you are experiencing a serious or life-threatening emergency, "
        "contact your local emergency service immediately."
    )

    if st.button("🚨 Emergency Help", type="primary"):
        st.warning(
            "Emergency escalation activated. "
            "In the real system this would connect to the appropriate "
            "emergency service / healthcare facility."
        )


# =========================================================
# FIND HOSPITAL
# =========================================================

elif st.session_state.page == "Find Hospital":

    st.title("🏥 Find Healthcare Services")

    default_value = st.session_state.search

    search = st.text_input(
        "What service do you need?",
        value=default_value,
        placeholder="Example: dialysis, cardiology, blood test..."
    )

    col1, col2 = st.columns(2)

    with col1:
        district = st.selectbox(
            "📍 District",
            ["Belagavi"]
        )

    with col2:
        max_distance = st.slider(
            "📏 Maximum distance (km)",
            1,
            100,
            50
        )

    if st.button("🔍 Search", type="primary"):

        if not search.strip():

            st.warning("Please enter a healthcare service.")

        else:

            query = search.lower()

            results = hospitals[
                (hospitals["District"] == district) &
                (hospitals["Distance"] <= max_distance)
            ]

            # Simple service matching
            results = results[
                results["Services"].str.lower().str.contains(
                    query,
                    na=False
                )
                |
                results["Specialists"].str.lower().str.contains(
                    query,
                    na=False
                )
            ]

            st.divider()

            if len(results) == 0:

                st.warning(
                    f"No registered facility found for **{search}**."
                )

                st.info(
                    "The real HealthBridge system could suggest nearby "
                    "alternative services or initiate a referral."
                )

            else:

                st.success(
                    f"{len(results)} healthcare facilities found."
                )

                for _, hospital in results.sort_values(
                    "Distance"
                ).iterrows():

                    with st.container(border=True):

                        st.subheader(
                            f"🏥 {hospital['Hospital']}"
                        )

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            st.write(
                                f"📍 **{hospital['Distance']} km**"
                            )
                            st.write(
                                f"🏛️ {hospital['Type']}"
                            )

                        with c2:
                            st.write(
                                f"🩺 **Services**"
                            )
                            st.write(
                                hospital["Services"]
                            )

                        with c3:
                            st.write(
                                f"👨‍⚕️ **Specialists**"
                            )
                            st.write(
                                hospital["Specialists"]
                            )

                        st.write(
                            f"🕐 **Timing:** {hospital['Timing']}"
                        )

                        if hospital["Emergency"] == "Yes":
                            st.success(
                                "🚑 Emergency service available"
                            )

                        colA, colB, colC = st.columns(3)

                        with colA:
                            if st.button(
                                "📅 Book Appointment",
                                key=f"book_{hospital['Hospital']}"
                            ):
                                st.session_state.page = "Appointments"
                                st.success(
                                    "Appointment page opened."
                                )

                        with colB:
                            if st.button(
                                "🔄 Request Referral",
                                key=f"ref_{hospital['Hospital']}"
                            ):
                                st.session_state.page = "Referral"
                                st.success(
                                    "Referral request started."
                                )

                        with colC:
                            if st.button(
                                "ℹ️ View Details",
                                key=f"details_{hospital['Hospital']}"
                            ):
                                st.info(
                                    f"{hospital['Hospital']} provides "
                                    f"{hospital['Services']}."
                                )


# =========================================================
# FIND SPECIALIST
# =========================================================

elif st.session_state.page == "Find Specialist":

    st.title("👨‍⚕️ Find a Specialist")

    specialist = st.selectbox(
        "Select specialist",
        [
            "Nephrologist",
            "Cardiologist",
            "General Physician"
        ]
    )

    district = st.selectbox(
        "📍 Select district",
        ["Belagavi"]
    )

    results = hospitals[
        (hospitals["District"] == district) &
        (hospitals["Specialists"].str.contains(
            specialist,
            case=False,
            na=False
        ))
    ]

    st.divider()

    if len(results) == 0:

        st.warning("No specialist found.")

    else:

        st.success(
            f"{len(results)} facilities have {specialist}."
        )

        for _, hospital in results.iterrows():

            with st.container(border=True):

                st.subheader(
                    f"🏥 {hospital['Hospital']}"
                )

                st.write(
                    f"📍 {hospital['Distance']} km away"
                )

                st.write(
                    f"👨‍⚕️ {hospital['Specialists']}"
                )

                if st.button(
                    "📅 Book Consultation",
                    key=f"specialist_{hospital['Hospital']}"
                ):
                    st.session_state.page = "Appointments"
                    st.success("Appointment page opened.")


# =========================================================
# APPOINTMENTS
# =========================================================

elif st.session_state.page == "Appointments":

    st.title("📅 Appointments")

    hospital = st.selectbox(
        "🏥 Select Hospital",
        hospitals["Hospital"].tolist()
    )

    doctor = st.selectbox(
        "👨‍⚕️ Select Specialist",
        [
            "General Physician",
            "Nephrologist",
            "Cardiologist"
        ]
    )

    date = st.date_input(
        "📅 Select Date"
    )

    time = st.selectbox(
        "🕐 Available Time",
        [
            "09:00 AM",
            "10:30 AM",
            "12:00 PM",
            "02:30 PM",
            "04:00 PM"
        ]
    )

    if st.button(
        "✅ Confirm Appointment",
        type="primary"
    ):

        st.success("Appointment successfully requested!")

        st.info(
            f"""
            **Hospital:** {hospital}

            **Specialist:** {doctor}

            **Date:** {date}

            **Time:** {time}
            """
        )


# =========================================================
# HEALTH RECORD
# =========================================================

elif st.session_state.page == "Health Record":

    st.title("📋 My Health Record")

    st.info(
        "Demo patient record. In production, this section "
        "would use authorized and consent-based health records."
    )

    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Name:** Demo Patient")
        st.write("**Age:** 52")

    with col2:
        st.write("**Location:** Belagavi")
        st.write("**Blood Group:** O+")

    st.divider()

    st.subheader("🩺 Previous Visits")

    records = pd.DataFrame([
        {
            "Date": "2026-08-20",
            "Hospital": "Rural Government Hospital",
            "Department": "General Medicine",
            "Status": "Completed"
        },
        {
            "Date": "2026-08-28",
            "Hospital": "District Government Hospital",
            "Department": "Nephrology",
            "Status": "Completed"
        }
    ])

    st.dataframe(
        records,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# REFERRAL
# =========================================================

elif st.session_state.page == "Referral":

    st.title("🔄 Referral Status")

    st.subheader("Current Referral")

    with st.container(border=True):

        st.write("👤 **Patient:** Demo Patient")

        st.write(
            "🏥 **Referred From:** Rural Government Hospital"
        )

        st.write(
            "🏥 **Referred To:** District Government Hospital"
        )

        st.write(
            "🩺 **Department:** Nephrology"
        )

        st.write(
            "📅 **Referral Date:** 08 September 2026"
        )

        st.success("✅ Referral Accepted")

    st.divider()

    st.subheader("Journey")

    st.write("✅ PHC / Rural Hospital")
    st.write("↓")
    st.write("✅ Referral Created")
    st.write("↓")
    st.write("✅ District Hospital")
    st.write("↓")
    st.write("⏳ Specialist Consultation")
    st.write("↓")
    st.write("⏳ Follow-up")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🏥 HealthBridge | SIH26133 Prototype | "
    "AI-assisted rural healthcare access"
)