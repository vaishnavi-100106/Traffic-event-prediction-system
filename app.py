import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import folium
from datetime import datetime, date

from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from weather import get_weather

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Gridlock AI Command Center",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# PROFESSIONAL CSS — DESIGN SYSTEM
# =====================================
# Palette:
#   Background : #0B1220 -> #060A14 (deep navy/near-black gradient)
#   Surface    : rgba(255,255,255,0.04) glass panels
#   Accent     : #3B82F6 (blue) / #22D3EE (cyan) for highlights
#   Text       : #E5E9F0 primary, #8B93A7 secondary
#   Status     : red #EF4444, amber #F59E0B, green #10B981

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

html, body, [class*="css"]  {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp{
    background:
        radial-gradient(circle at 15% 0%, rgba(59,130,246,0.08), transparent 35%),
        radial-gradient(circle at 85% 100%, rgba(34,211,238,0.06), transparent 40%),
        linear-gradient(180deg, #0B1220 0%, #070B14 55%, #04060B 100%);
}

/* ---------- Header band ---------- */
.app-header{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 18px 28px;
    margin-bottom: 6px;
    border-radius: 16px;
    background: linear-gradient(120deg, rgba(59,130,246,0.10), rgba(34,211,238,0.04));
    border: 1px solid rgba(255,255,255,0.07);
}

.brand-row{
    display:flex;
    align-items:center;
    gap:14px;
}

.brand-icon{
    width:46px;height:46px;
    border-radius:12px;
    background:linear-gradient(135deg,#3B82F6,#22D3EE);
    display:flex;align-items:center;justify-content:center;
    font-size:24px;
    box-shadow:0 8px 24px rgba(59,130,246,0.35);
}

.main-title{
    font-size:26px;
    font-weight:800;
    color:#F1F5F9;
    letter-spacing:0.3px;
    margin:0;
}

.sub-title{
    color:#8B93A7;
    font-size:13px;
    margin-top:2px;
    letter-spacing:0.4px;
}

.status-pill{
    display:flex;
    align-items:center;
    gap:8px;
    background:rgba(16,185,129,0.12);
    border:1px solid rgba(16,185,129,0.35);
    color:#34D399;
    font-size:12.5px;
    font-weight:600;
    padding:8px 14px;
    border-radius:999px;
}

.status-dot{
    width:8px;height:8px;border-radius:50%;
    background:#34D399;
    box-shadow:0 0 8px #34D399;
}

/* ---------- Glass / metric cards ---------- */
.glass{
    background: rgba(255,255,255,0.035);
    backdrop-filter: blur(18px);
    border:1px solid rgba(255,255,255,0.07);
    border-radius:18px;
    padding:22px;
}

.section-label{
    color:#8B93A7;
    font-size:12px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:1.4px;
    margin-bottom:10px;
}

.metric-card{
    background: rgba(255,255,255,0.035);
    backdrop-filter: blur(20px);
    border-radius:16px;
    padding:22px 18px;
    border:1px solid rgba(255,255,255,0.07);
    transition: all 0.2s ease;
    position:relative;
    overflow:hidden;
}

.metric-card:hover{
    border-color: rgba(59,130,246,0.4);
    transform: translateY(-2px);
}

.metric-card .icon{
    font-size:20px;
    opacity:0.85;
    margin-bottom:10px;
}

.metric-card h1{
    color:#F8FAFC;
    margin:0;
    font-size:30px;
    font-weight:800;
    letter-spacing:-0.5px;
}

.metric-card p{
    color:#8B93A7;
    margin:4px 0 0 0;
    font-size:12.5px;
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:0.8px;
}

.metric-accent-blue{ border-left:3px solid #3B82F6; }
.metric-accent-cyan{ border-left:3px solid #22D3EE; }
.metric-accent-amber{ border-left:3px solid #F59E0B; }
.metric-accent-red{ border-left:3px solid #EF4444; }

/* ---------- Result banners ---------- */
.result-high{
    background:linear-gradient(120deg,#7F1D1D,#450A0A);
    border:1px solid rgba(239,68,68,0.4);
    padding:20px;
    border-radius:16px;
    text-align:center;
    font-size:26px;
    font-weight:800;
    color:#FECACA;
    letter-spacing:0.5px;
}

.result-medium{
    background:linear-gradient(120deg,#78350F,#451A03);
    border:1px solid rgba(245,158,11,0.4);
    padding:20px;
    border-radius:16px;
    text-align:center;
    font-size:26px;
    font-weight:800;
    color:#FDE68A;
    letter-spacing:0.5px;
}

.result-low{
    background:linear-gradient(120deg,#064E3B,#022C22);
    border:1px solid rgba(16,185,129,0.4);
    padding:20px;
    border-radius:16px;
    text-align:center;
    font-size:26px;
    font-weight:800;
    color:#A7F3D0;
    letter-spacing:0.5px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{
    background:#070B14;
    border-right:1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] h2{
    color:#F1F5F9 !important;
    font-size:17px;
}

/* ---------- Buttons ---------- */
.stButton button{
    width:100%;
    height:52px;
    border-radius:12px;
    font-size:16px;
    font-weight:700;
    background:linear-gradient(120deg,#3B82F6,#2563EB);
    border:none;
    color:white;
    letter-spacing:0.3px;
    box-shadow:0 6px 18px rgba(37,99,235,0.35);
    transition: all 0.2s ease;
}

.stButton button:hover{
    transform:translateY(-1px);
    box-shadow:0 10px 24px rgba(37,99,235,0.45);
}

/* ---------- Inputs ---------- */
.stTextInput input, .stNumberInput input, .stSelectbox > div, .stDateInput input{
    background:rgba(255,255,255,0.04) !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    color:#E5E9F0 !important;
    border-radius:10px !important;
}

/* ---------- Divider ---------- */
.section-divider{
    height:1px;
    background:linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    margin: 28px 0;
    border:none;
}

/* ---------- Forecast result card ---------- */
.forecast-card{
    background: rgba(255,255,255,0.035);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:18px;
    padding:26px;
}

.forecast-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px 0;
    border-bottom:1px dashed rgba(255,255,255,0.08);
}

.forecast-row:last-child{ border-bottom:none; }

.forecast-label{ color:#8B93A7; font-size:13.5px; font-weight:600; }
.forecast-value{ color:#F1F5F9; font-size:15px; font-weight:700; }

/* ---------- About page ---------- */
.about-hero{
    background: linear-gradient(120deg, rgba(59,130,246,0.10), rgba(34,211,238,0.04));
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    padding:36px 32px;
    margin-bottom:28px;
}

.about-hero-eyebrow{
    color:#60A5FA;
    font-size:12px;
    font-weight:700;
    letter-spacing:1.6px;
    text-transform:uppercase;
    margin-bottom:10px;
}

.about-hero h1{
    color:#F8FAFC;
    font-size:34px;
    font-weight:800;
    margin:0 0 10px 0;
    letter-spacing:-0.5px;
}

.about-hero p{
    color:#94A3B8;
    font-size:15px;
    max-width:680px;
    line-height:1.6;
    margin:0;
}

.about-stat-strip{
    display:flex;
    gap:14px;
    margin-top:22px;
    flex-wrap:wrap;
}

.about-stat{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;
    padding:12px 18px;
}

.about-stat .num{
    color:#F1F5F9;
    font-size:20px;
    font-weight:800;
}

.about-stat .lbl{
    color:#8B93A7;
    font-size:11.5px;
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:0.6px;
}

.about-block-title{
    color:#F1F5F9;
    font-size:18px;
    font-weight:700;
    margin: 6px 0 16px 2px;
    display:flex;
    align-items:center;
    gap:10px;
}

.about-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit, minmax(190px, 1fr));
    gap:14px;
    margin-bottom:34px;
}

.about-card{
    background:rgba(255,255,255,0.035);
    border:1px solid rgba(255,255,255,0.07);
    border-radius:14px;
    padding:18px 16px;
    transition: all 0.2s ease;
}

.about-card:hover{
    border-color: rgba(59,130,246,0.4);
    transform: translateY(-2px);
}

.about-card .a-icon{
    width:34px;height:34px;
    border-radius:9px;
    background:rgba(59,130,246,0.14);
    display:flex;align-items:center;justify-content:center;
    font-size:16px;
    margin-bottom:10px;
}

.about-card .a-title{
    color:#E5E9F0;
    font-size:13.5px;
    font-weight:600;
    line-height:1.4;
}

.tier-card{
    background:rgba(255,255,255,0.035);
    border:1px solid rgba(255,255,255,0.07);
    border-radius:14px;
    padding:20px;
}

.tier-high{ border-top:3px solid #EF4444; }
.tier-medium{ border-top:3px solid #F59E0B; }
.tier-low{ border-top:3px solid #10B981; }

.tier-name{
    font-size:13px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.8px;
    margin-bottom:14px;
}

.tier-high .tier-name{ color:#F87171; }
.tier-medium .tier-name{ color:#FBBF24; }
.tier-low .tier-name{ color:#34D399; }

.tier-item{
    display:flex;
    justify-content:space-between;
    color:#CBD5E1;
    font-size:13.5px;
    padding:7px 0;
    border-bottom:1px solid rgba(255,255,255,0.05);
}

.tier-item:last-child{ border-bottom:none; }
.tier-item span:last-child{ color:#F1F5F9; font-weight:700; }

.about-footer-card{
    background:linear-gradient(120deg, rgba(59,130,246,0.12), rgba(34,211,238,0.06));
    border:1px solid rgba(255,255,255,0.1);
    border-radius:16px;
    padding:26px 30px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:16px;
}

.about-footer-card h3{
    color:#F8FAFC;
    margin:0 0 4px 0;
    font-size:18px;
    font-weight:800;
}

.about-footer-card p{
    color:#94A3B8;
    margin:0;
    font-size:13.5px;
}

.about-footer-badge{
    background:rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.14);
    color:#E5E9F0;
    font-size:12.5px;
    font-weight:700;
    padding:8px 16px;
    border-radius:999px;
    white-space:nowrap;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD MODEL
# =====================================

@st.cache_resource
def load_model():
    model = joblib.load("gridlock2_model.pkl")
    encoder = joblib.load("label_encoder.pkl")
    return model, encoder


@st.cache_data
def load_data():
    data = pd.read_csv("dataset.csv")
    return data


model, encoder = load_model()
df = load_data()
weather = get_weather()

# =====================================
# HEADER
# =====================================

st.markdown(f"""
<div class="app-header">
    <div class="brand-row">
        <div class="brand-icon">🚦</div>
        <div>
            <p class="main-title">GRIDLOCK AI COMMAND CENTER</p>
            <p class="sub-title">REAL-TIME TRAFFIC INTELLIGENCE · EVENT FORECASTING · RESOURCE PLANNING</p>
        </div>
    </div>
    <div class="status-pill">
        <div class="status-dot"></div>
        SYSTEM ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# NAVIGATION
# =====================================

selected = option_menu(
    menu_title=None,
    options=[
        "Command Center",
        "Forecast",
        "Analytics",
        "Heatmap",
        "About"
    ],
    icons=[
        "speedometer2",
        "calendar-event",
        "graph-up",
        "geo-alt",
        "info-circle"
    ],
    orientation="horizontal",
    styles={
        "container": {"padding": "6px", "background-color": "rgba(255,255,255,0.035)",
                       "border": "1px solid rgba(255,255,255,0.07)", "border-radius": "14px"},
        "icon": {"color": "#8B93A7", "font-size": "15px"},
        "nav-link": {"font-size": "14px", "font-weight": "600", "color": "#CBD5E1",
                      "text-align": "center", "margin": "0px", "border-radius": "10px"},
        "nav-link-selected": {"background-color": "#2563EB", "color": "white"},
    }
)

# =====================================
# KPI CARDS
# =====================================

high_events = len(df[df["priority"] == "High"])

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card metric-accent-blue">
        <div class="icon">📋</div>
        <h1>{len(df):,}</h1>
        <p>Total Incidents</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card metric-accent-cyan">
        <div class="icon">🗺</div>
        <h1>{df['zone'].nunique()}</h1>
        <p>Zones Covered</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card metric-accent-blue">
        <div class="icon">🏢</div>
        <h1>{df['police_station'].nunique()}</h1>
        <p>Police Stations</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card metric-accent-red">
        <div class="icon">🔥</div>
        <h1>{high_events:,}</h1>
        <p>High Priority Events</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# COMMAND CENTER
# =====================================

if selected == "Command Center":

    # =====================================
    # WEATHER + RISK BAR
    # =====================================

    st.markdown('<p class="section-label">LIVE CITY STATUS</p>', unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)

    with w1:
        st.metric("🌡 Temperature", f"{weather['temperature']} °C")

    with w2:
        st.metric("💧 Humidity", f"{weather['humidity']}%")

    with w3:
        st.metric("☁ Condition", weather["condition"])

    risk_score = 40

    if weather["condition"] == "Rain":
        risk_score += 25
    elif weather["condition"] == "Thunderstorm":
        risk_score += 40
    elif weather["condition"] == "Clouds":
        risk_score += 10
    elif weather["condition"] == "Mist":
        risk_score += 15

    risk_score = min(risk_score, 100)

    with w4:
        st.metric("🚦 Risk Score", f"{risk_score}/100")

    st.progress(risk_score)

    if risk_score >= 80:
        st.error("🔴 High Congestion Risk")
    elif risk_score >= 60:
        st.warning("🟡 Moderate Congestion Risk")
    else:
        st.success("🟢 Low Congestion Risk")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # =====================================
    # SIDEBAR SIMULATOR
    # =====================================

    with st.sidebar:

        st.header("🎯 Event Simulator")

        with st.expander("Event Configuration", expanded=True):

            event_type = st.selectbox("Event Type", ["planned", "unplanned"])

            event_cause = st.selectbox(
                "Event Cause",
                ["vehicle_breakdown", "accident", "water_logging",
                 "tree_fall", "public_event", "others"]
            )

            requires_road_closure = st.selectbox("Road Closure", ["TRUE", "FALSE"])

            priority = st.selectbox("Priority", ["High", "Low"])

            corridor = st.text_input("Corridor", "ORR East 1")

            zone = st.text_input("Zone", "North Zone 1")

            junction = st.text_input("Junction", "HebbalFlyoverJunc")

            police_station = st.text_input("Police Station", "Hebbala")

            hour = st.slider("Hour", 0, 23, 12)

            day_of_week = st.slider("Day", 0, 6, 1)

            month = st.slider("Month", 1, 12, 1)

            crowd_size = st.number_input("Expected Crowd Size", min_value=0, value=1000)

        predict_btn = st.button("🚀 Predict Severity")

    # =====================================
    # MAIN DASHBOARD
    # =====================================

    left, right = st.columns([3, 1])

    with left:

        st.markdown('<p class="section-label">BENGALURU TRAFFIC INTELLIGENCE MAP</p>', unsafe_allow_html=True)

        map_df = df.dropna(subset=["latitude", "longitude"])

        m = folium.Map(location=[12.97, 77.59], zoom_start=11, tiles="CartoDB Voyager")

        HeatMap(map_df[["latitude", "longitude"]].values.tolist(), radius=15, blur=10).add_to(m)

        sample = map_df.sample(min(300, len(map_df)), random_state=42)

        for _, row in sample.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=3,
                popup=str(row["event_cause"]),
                fill=True
            ).add_to(m)

        st_folium(m, width=None, height=750)

    with right:

        st.markdown('<p class="section-label">LIVE INCIDENT FEED</p>', unsafe_allow_html=True)

        recent = df["event_cause"].dropna().astype(str).head(10)

        for item in recent:
            st.info(f"Incident: {item}")

    # =====================================
    # PREDICTION ENGINE
    # =====================================

    if predict_btn:

        is_weekend = 1 if day_of_week >= 5 else 0

        input_df = pd.DataFrame([{
            "event_type": event_type,
            "event_cause": event_cause,
            "requires_road_closure": requires_road_closure,
            "corridor": corridor,
            "priority": priority,
            "zone": zone,
            "junction": junction,
            "police_station": police_station,
            "status": "active",
            "hour": hour,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": is_weekend
        }])

        pred = model.predict(input_df)
        severity = encoder.inverse_transform(pred)[0]

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">AI ASSESSMENT</p>', unsafe_allow_html=True)

        if severity == "High":
            st.markdown("<div class='result-high'>🚨 HIGH SEVERITY</div>", unsafe_allow_html=True)
            officers, barricades, diversion = 5, 8, "Required"

        elif severity == "Medium":
            st.markdown("<div class='result-medium'>⚠️ MEDIUM SEVERITY</div>", unsafe_allow_html=True)
            officers, barricades, diversion = 3, 4, "Optional"

        else:
            st.markdown("<div class='result-low'>✅ LOW SEVERITY</div>", unsafe_allow_html=True)
            officers, barricades, diversion = 1, 1, "Not Required"

        # ---- Resource recommendation ----
        if crowd_size > 10000:
            officers += 2
            barricades += 3
            st.warning("👥 Large Crowd Detected - Additional Resources Recommended")

        if weather["condition"] in ["Rain", "Thunderstorm"]:
            officers += 1
            st.warning("🌧 Weather Impact Detected")

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("🚔 Officers Required", officers)
        with c2:
            st.metric("🚧 Barricades Required", barricades)
        with c3:
            st.metric("↩ Diversion Plan", diversion)

        # ---- Final AI risk score ----
        final_risk = 40

        if severity == "High":
            final_risk += 40
        elif severity == "Medium":
            final_risk += 20

        if weather["condition"] in ["Rain", "Thunderstorm"]:
            final_risk += 20

        if crowd_size > 10000:
            final_risk += 15

        final_risk = min(final_risk, 100)

        st.markdown('<p class="section-label">AI RISK ASSESSMENT</p>', unsafe_allow_html=True)
        st.progress(final_risk)

        if final_risk >= 80:
            st.error(f"🔴 CRITICAL RISK ({final_risk}/100)")
        elif final_risk >= 60:
            st.warning(f"🟡 MODERATE RISK ({final_risk}/100)")
        else:
            st.success(f"🟢 LOW RISK ({final_risk}/100)")

# =====================================
# FORECAST PAGE (NEW)
# =====================================

elif selected == "Forecast":

    st.markdown('<p class="section-label">EVENT-DRIVEN CONGESTION FORECAST</p>', unsafe_allow_html=True)
    st.markdown("Forecast congestion severity and resource needs for a specific **date** and **zone**, "
                "using historical patterns combined with the AI severity model.")

    st.markdown("<br>", unsafe_allow_html=True)

    fcol1, fcol2 = st.columns([1, 1])

    with fcol1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">FORECAST INPUTS</p>', unsafe_allow_html=True)

        zone_list = sorted(df["zone"].dropna().unique().tolist())
        forecast_zone = st.selectbox("Select Zone", zone_list)

        forecast_date = st.date_input("Select Date", value=date.today())

        forecast_event_cause = st.selectbox(
            "Likely Event Cause",
            ["vehicle_breakdown", "accident", "water_logging",
             "tree_fall", "public_event", "others"]
        )

        forecast_event_type = st.selectbox("Event Type", ["planned", "unplanned"])

        forecast_crowd = st.number_input("Expected Crowd Size", min_value=0, value=2000)

        run_forecast = st.button("📅 Generate Forecast")
        st.markdown('</div>', unsafe_allow_html=True)

    with fcol2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">HISTORICAL ZONE SNAPSHOT</p>', unsafe_allow_html=True)

        zone_hist = df[df["zone"] == forecast_zone]

        if len(zone_hist) > 0:
            hist_high_pct = round(
                (zone_hist["priority"] == "High").mean() * 100, 1
            )
            top_cause = (
                zone_hist["event_cause"].value_counts().idxmax()
                if zone_hist["event_cause"].notna().any() else "N/A"
            )
            top_station = (
                zone_hist["police_station"].value_counts().idxmax()
                if zone_hist["police_station"].notna().any() else "N/A"
            )

            st.markdown(f"""
            <div class="forecast-row">
                <span class="forecast-label">Historical Incidents in Zone</span>
                <span class="forecast-value">{len(zone_hist)}</span>
            </div>
            <div class="forecast-row">
                <span class="forecast-label">High Priority Share</span>
                <span class="forecast-value">{hist_high_pct}%</span>
            </div>
            <div class="forecast-row">
                <span class="forecast-label">Most Common Cause</span>
                <span class="forecast-value">{top_cause}</span>
            </div>
            <div class="forecast-row">
                <span class="forecast-label">Nearest Police Station</span>
                <span class="forecast-value">{top_station}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No historical data available for this zone yet.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if run_forecast:

        # Derive temporal features from the selected date
        dt = datetime.combine(forecast_date, datetime.min.time())
        f_hour = 12  # default representative hour for a day-level forecast
        f_day_of_week = dt.weekday()
        f_month = dt.month
        f_is_weekend = 1 if f_day_of_week >= 5 else 0

        # Pull representative corridor/junction/police_station from zone history (mode), fallback defaults
        if len(zone_hist) > 0:
            f_corridor = (
                zone_hist["corridor"].value_counts().idxmax()
                if "corridor" in zone_hist.columns and zone_hist["corridor"].notna().any()
                else "Unknown Corridor"
            )
            f_junction = (
                zone_hist["junction"].value_counts().idxmax()
                if "junction" in zone_hist.columns and zone_hist["junction"].notna().any()
                else "Unknown Junction"
            )
            f_police_station = (
                zone_hist["police_station"].value_counts().idxmax()
                if zone_hist["police_station"].notna().any()
                else "Unknown Station"
            )
        else:
            f_corridor, f_junction, f_police_station = "Unknown Corridor", "Unknown Junction", "Unknown Station"

        forecast_input = pd.DataFrame([{
            "event_type": forecast_event_type,
            "event_cause": forecast_event_cause,
            "requires_road_closure": "FALSE",
            "corridor": f_corridor,
            "priority": "High" if forecast_crowd > 10000 else "Low",
            "zone": forecast_zone,
            "junction": f_junction,
            "police_station": f_police_station,
            "status": "active",
            "hour": f_hour,
            "day_of_week": f_day_of_week,
            "month": f_month,
            "is_weekend": f_is_weekend
        }])

        pred = model.predict(forecast_input)
        severity = encoder.inverse_transform(pred)[0]

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">FORECAST RESULT</p>', unsafe_allow_html=True)

        if severity == "High":
            st.markdown("<div class='result-high'>🚨 HIGH CONGESTION FORECAST</div>", unsafe_allow_html=True)
            officers, barricades, diversion = 5, 8, "Required"
        elif severity == "Medium":
            st.markdown("<div class='result-medium'>⚠️ MEDIUM CONGESTION FORECAST</div>", unsafe_allow_html=True)
            officers, barricades, diversion = 3, 4, "Optional"
        else:
            st.markdown("<div class='result-low'>✅ LOW CONGESTION FORECAST</div>", unsafe_allow_html=True)
            officers, barricades, diversion = 1, 1, "Not Required"

        if forecast_crowd > 10000:
            officers += 2
            barricades += 3
            st.warning("👥 Large Crowd Detected - Additional Resources Recommended")

        if weather["condition"] in ["Rain", "Thunderstorm"]:
            officers += 1
            st.warning("🌧 Current Weather Conditions May Compound Forecast Risk")

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("📅 Forecast Date", forecast_date.strftime("%d %b %Y"))
        with c2:
            st.metric("🗺 Zone", forecast_zone)
        with c3:
            st.metric("🚔 Officers Suggested", officers)
        with c4:
            st.metric("🚧 Barricades Suggested", barricades)

        st.markdown("<br>", unsafe_allow_html=True)

        # Forecast risk score blending model output + historical zone risk
        base_risk = 40
        if severity == "High":
            base_risk += 40
        elif severity == "Medium":
            base_risk += 20

        if len(zone_hist) > 0:
            base_risk += int(hist_high_pct / 5)  # historical high-priority share nudges risk

        if forecast_crowd > 10000:
            base_risk += 15

        if weather["condition"] in ["Rain", "Thunderstorm"]:
            base_risk += 10

        if f_is_weekend:
            base_risk += 5

        forecast_risk = min(base_risk, 100)

        st.markdown('<p class="section-label">FORECASTED RISK SCORE</p>', unsafe_allow_html=True)
        st.progress(forecast_risk)

        if forecast_risk >= 80:
            st.error(f"🔴 CRITICAL FORECAST RISK ({forecast_risk}/100) — Recommend pre-positioning resources")
        elif forecast_risk >= 60:
            st.warning(f"🟡 MODERATE FORECAST RISK ({forecast_risk}/100) — Monitor closely")
        else:
            st.success(f"🟢 LOW FORECAST RISK ({forecast_risk}/100)")

        st.markdown(f"""
        <div class="forecast-card">
            <div class="forecast-row">
                <span class="forecast-label">Diversion Plan</span>
                <span class="forecast-value">{diversion}</span>
            </div>
            <div class="forecast-row">
                <span class="forecast-label">Predicted Severity</span>
                <span class="forecast-value">{severity}</span>
            </div>
            <div class="forecast-row">
                <span class="forecast-label">Day Type</span>
                <span class="forecast-value">{"Weekend" if f_is_weekend else "Weekday"}</span>
            </div>
            <div class="forecast-row">
                <span class="forecast-label">Reference Police Station</span>
                <span class="forecast-value">{f_police_station}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =====================================
# ANALYTICS PAGE
# =====================================

elif selected == "Analytics":

    st.markdown('<p class="section-label">TRAFFIC ANALYTICS</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Causes", "Zones", "Distribution"])

    plotly_template = "plotly_dark"

    with tab1:
        cause_counts = df["event_cause"].value_counts()
        fig = px.bar(x=cause_counts.index, y=cause_counts.values,
                     title="Top Incident Causes", template=plotly_template,
                     color_discrete_sequence=["#3B82F6"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        zone_counts = df["zone"].value_counts().head(10)
        fig2 = px.bar(x=zone_counts.index, y=zone_counts.values,
                      title="Top 10 Zones", template=plotly_template,
                      color_discrete_sequence=["#22D3EE"])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        fig3 = px.pie(
            values=df["event_type"].value_counts().values,
            names=df["event_type"].value_counts().index,
            title="Planned vs Unplanned",
            template=plotly_template,
            color_discrete_sequence=["#3B82F6", "#F59E0B"]
        )
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True)

# =====================================
# HEATMAP PAGE
# =====================================

elif selected == "Heatmap":

    st.markdown('<p class="section-label">BENGALURU INCIDENT HEATMAP</p>', unsafe_allow_html=True)

    map_df = df.dropna(subset=["latitude", "longitude"])

    st.metric("Mapped Incidents", len(map_df))

    m = folium.Map(location=[12.97, 77.59], zoom_start=11, tiles="CartoDB dark_matter")

    HeatMap(map_df[["latitude", "longitude"]].values.tolist(), radius=15, blur=10).add_to(m)

    st_folium(m, width=None, height=850)

# =====================================
# ABOUT PAGE
# =====================================

else:

    st.markdown('<p class="section-label">ABOUT GRIDLOCK AI</p>', unsafe_allow_html=True)

    # ---- Hero ----
    st.markdown("""
    <div class="about-hero">
        <div class="about-hero-eyebrow">GRIDLOCK 2.0 · TRAFFIC INTELLIGENCE PLATFORM</div>
        <h1>🚦 Gridlock AI Command Center</h1>
        <p>An intelligent congestion forecasting platform built for event-driven traffic
        management — combining historical incident data, live weather signals, and
        machine learning to predict severity and recommend resource deployment before
        congestion happens.</p>
        <div class="about-stat-strip">
            <div class="about-stat"><div class="num">8,000+</div><div class="lbl">Incidents Logged</div></div>
            <div class="about-stat"><div class="num">10</div><div class="lbl">Zones Covered</div></div>
            <div class="about-stat"><div class="num">54</div><div class="lbl">Police Stations</div></div>
            <div class="about-stat"><div class="num">7</div><div class="lbl">AI Capabilities</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Problem Solved ----
    st.markdown('<div class="about-block-title">🎯 Problem Solved</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-grid">
        <div class="about-card"><div class="a-icon">🪧</div><div class="a-title">Political Rallies</div></div>
        <div class="about-card"><div class="a-icon">🎉</div><div class="a-title">Festivals</div></div>
        <div class="about-card"><div class="a-icon">🏟</div><div class="a-title">Sports Events</div></div>
        <div class="about-card"><div class="a-icon">🚧</div><div class="a-title">Construction Activities</div></div>
        <div class="about-card"><div class="a-icon">🌧</div><div class="a-title">Water Logging</div></div>
        <div class="about-card"><div class="a-icon">🚗</div><div class="a-title">Vehicle Breakdowns</div></div>
        <div class="about-card"><div class="a-icon">⚠️</div><div class="a-title">Accidents</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ---- AI Capabilities ----
    st.markdown('<div class="about-block-title">🤖 AI Capabilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-grid">
        <div class="about-card"><div class="a-icon">📈</div><div class="a-title">Congestion Severity Prediction</div></div>
        <div class="about-card"><div class="a-icon">📅</div><div class="a-title">Date & Zone Based Forecasting</div></div>
        <div class="about-card"><div class="a-icon">🚔</div><div class="a-title">Resource Recommendation</div></div>
        <div class="about-card"><div class="a-icon">🎚</div><div class="a-title">Dynamic Risk Assessment</div></div>
        <div class="about-card"><div class="a-icon">🧪</div><div class="a-title">Event Simulation</div></div>
        <div class="about-card"><div class="a-icon">🗺</div><div class="a-title">Traffic Heatmap Intelligence</div></div>
        <div class="about-card"><div class="a-icon">☁️</div><div class="a-title">Weather Aware Forecasting</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Resource Planning Engine ----
    st.markdown('<div class="about-block-title">🚧 Resource Planning Engine</div>', unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)

    with t1:
        st.markdown("""
        <div class="tier-card tier-high">
            <div class="tier-name">🔴 High Severity</div>
            <div class="tier-item"><span>Officers</span><span>5+</span></div>
            <div class="tier-item"><span>Barricades</span><span>8+</span></div>
            <div class="tier-item"><span>Diversion</span><span>Required</span></div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div class="tier-card tier-medium">
            <div class="tier-name">🟡 Medium Severity</div>
            <div class="tier-item"><span>Officers</span><span>3</span></div>
            <div class="tier-item"><span>Barricades</span><span>4</span></div>
            <div class="tier-item"><span>Diversion</span><span>Optional</span></div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div class="tier-card tier-low">
            <div class="tier-name">🟢 Low Severity</div>
            <div class="tier-item"><span>Officers</span><span>1</span></div>
            <div class="tier-item"><span>Barricades</span><span>1</span></div>
            <div class="tier-item"><span>Diversion</span><span>Not Required</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Data Used ----
    st.markdown('<div class="about-block-title">📊 Data Used</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-grid">
        <div class="about-card"><div class="a-icon">📋</div><div class="a-title">8,000+ Historical Incidents</div></div>
        <div class="about-card"><div class="a-icon">🗺</div><div class="a-title">Multiple Zones</div></div>
        <div class="about-card"><div class="a-icon">🏢</div><div class="a-title">Police Station Data</div></div>
        <div class="about-card"><div class="a-icon">🏷</div><div class="a-title">Event Categories</div></div>
        <div class="about-card"><div class="a-icon">🚫</div><div class="a-title">Road Closure Information</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Footer card ----
    st.markdown("""
    <div class="about-footer-card">
        <div>
            <h3>🏆 Gridlock 2.0</h3>
            <p>AI-Powered Event Congestion Forecasting & Resource Deployment Platform</p>
        </div>
        <div class="about-footer-badge">Built with Streamlit · XGBoost</div>
    </div>
    """, unsafe_allow_html=True)



# =====================================
# FOOTER
# =====================================

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.caption("Gridlock AI Command Center • Built with Streamlit, XGBoost & Real-Time Weather Data")