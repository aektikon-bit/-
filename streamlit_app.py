import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="C/F Temperature Converter",
    page_icon="🌡",
    layout="centered"
)

# Custom CSS (UI สไตล์การ์ด + Responsive)
st.markdown("""
<style>
.card {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
}
.output-number {
    font-size: 38px;
    font-weight: 700;
}
@media (max-width: 640px) {
    .card {
        padding: 14px;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Conversion functions (C <-> F)
# -----------------------------
def c_to_f(c): return c * 9/5 + 32
def f_to_c(f): return (f - 32) * 5/9
def fmt(x): return f"{x:.6g}"

units = {
    "Celsius (°C)": "C",
    "Fahrenheit (°F)": "F"
}

# -----------------------------
# Title
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("🌡 C/F Temperature Converter")
st.caption("แปลงค่าอุณหภูมิระหว่าง °C ↔ °F พร้อมกราฟและประวัติ")
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
to_unit = "Fahrenheit (°F)" if from_unit.startswith("C") else "Celsius (°C) "
convert_btn = st.button("🔁 แปลงค่า", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Calculate
# -----------------------------
if convert_btn:
    if from_unit.startswith("C"):
        out = c_to_f(val)
    else:
        out = f_to_c(val)

    # Show result
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("ผลลัพธ์")
    st.markdown(f"<div class='output-number'>{fmt(out)} {to_unit.split()[-1]}</div>", unsafe_allow_html=True)
    st.write(f"{fmt(val)} {from_unit} → {fmt(out)} {to_unit}")

    # Save history
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.insert(
        0,
        f"{datetime.now().strftime('%H:%M:%S')} — {fmt(val)} {from_unit} → {fmt(out)} {to_unit}"
    )
    st.markdown("</div>", unsafe_allow_html=True)


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
