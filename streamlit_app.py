import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Temperature Converter Pro",
    page_icon="🌡",
    layout="centered"
)

# Custom CSS (UI สไตล์การ์ด + Responsive)
st.markdown("""
<style>
/* Center main container */
.main {
    padding-top: 1.5rem;
}

/* Glass card */
.card {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Mobile adjustments */
@media (max-width: 640px) {
    .card {
        padding: 14px;
    }
}

/* Big output number */
.output-number {
    font-size: 38px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Conversion functions
# -----------------------------
def to_kelvin(v, unit):
    if unit == 'C': return v + 273.15
    if unit == 'F': return (v - 32) * 5/9 + 273.15
    if unit == 'K': return v
    if unit == 'R': return v * 5/9

def from_kelvin(k, unit):
    if unit == 'C': return k - 273.15
    if unit == 'F': return (k - 273.15) * 9/5 + 32
    if unit == 'K': return k
    if unit == 'R': return k * 9/5

def fmt(x):
    return f"{x:.6g}"

units = {
    "Celsius (°C)": "C",
    "Fahrenheit (°F)": "F",
    "Kelvin (K)": "K",
    "Rankine (°R)": "R",
}

# -----------------------------
# Title
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("🌡 Temperature Converter Pro")
st.caption("UI แบบสวย • รองรับมือถือ • พร้อมกราฟเปรียบเทียบค่าอุณหภูมิ")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Input Card
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    val = st.number_input("ค่าอุณหภูมิ", value=25.0, step=0.1)

with col2:
    from_unit = st.selectbox("จากหน่วย", list(units.keys()))

to_unit = st.selectbox("เป็นหน่วย", list(units.keys()))

convert_btn = st.button("🔁 แปลงค่า", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Calculate
# -----------------------------
if convert_btn:
    k = to_kelvin(val, units[from_unit])
    out = from_kelvin(k, units[to_unit])

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("ผลลัพธ์")
    st.markdown(f"<div class='output-number'>{fmt(out)} {to_unit.split()[-1]}</div>", unsafe_allow_html=True)
    st.write(f"แปลงจาก {fmt(val)} {from_unit} → {fmt(out)} {to_unit}")

    # Save history
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.insert(
        0,
        f"{datetime.now().strftime('%H:%M:%S')} — {fmt(val)} {from_unit} → {fmt(out)} {to_unit}"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # GRAPH SECTION (NEW!)
    # -----------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 กราฟเปรียบเทียบอุณหภูมิในทุกหน่วย")

    # Convert to all 4 units
    temp_data = {
        "Unit": ["°C", "°F", "K", "°R"],
        "Value": [
            from_kelvin(k, "C"),
            from_kelvin(k, "F"),
            from_kelvin(k, "K"),
            from_kelvin(k, "R"),
        ]
    }

    df = pd.DataFrame(temp_data)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("Unit", title="หน่วย"),
            y=alt.Y("Value", title="ค่าอุณหภูมิ"),
            tooltip=["Unit", "Value"]
        )
        .properties(height=300)
    )

    st.altair_chart(chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# History
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📜 ประวัติการแปลง")

if "history" in st.session_state and len(st.session_state.history) > 0:
    for item in st.session_state.history[:10]:
        st.write("- " + item)
else:
    st.info("ยังไม่มีประวัติการแปลง")

if st.button("🗑 ล้างประวัติ", use_container_width=True):
    st.session_state.history = []
    st.warning("ล้างประวัติแล้ว!")

st.markdown("</div>", unsafe_allow_html=True)
