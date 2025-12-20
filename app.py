import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

# --- 1. PAGE SETTINGS ---
st.set_page_config(page_title="Heart AI Pro", layout="wide", page_icon="🏥")

# --- 2. PREMIUM CUSTOM CSS ---
st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0f172a;
    color: #1e293b;
}

.main {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f1628 100%);
    padding: 0 !important;
}

/* Premium Header */
.premium-header {
    background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 50%, #0284c7 100%);
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 20px 60px rgba(6, 182, 212, 0.3);
    border-bottom: 3px solid rgba(6, 182, 212, 0.5);
}

.premium-header h1 {
    font-size: 3.5em;
    color: white;
    font-weight: 900;
    margin: 0;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    letter-spacing: -1px;
}

.premium-header p {
    font-size: 1.3em;
    color: rgba(255, 255, 255, 0.95);
    margin-top: 15px;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* Main Container */
.main-container {
    max-width: 1600px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Input Card - Left Column */
.input-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    border: 2px solid rgba(6, 182, 212, 0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.input-card:hover {
    box-shadow: 0 30px 80px rgba(6, 182, 212, 0.2);
    transform: translateY(-5px);
}

.input-card h2 {
    color: #0284c7;
    font-size: 1.8em;
    font-weight: 800;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.input-card .subtitle {
    color: #64748b;
    font-size: 0.95em;
    margin-bottom: 30px;
    font-weight: 500;
}

/* Section Divider */
.input-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #0ea5e9, transparent);
    margin: 30px 0;
    border-radius: 10px;
}

/* Results Card - Right Column */
.results-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    border: 2px solid rgba(6, 182, 212, 0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.results-card:hover {
    box-shadow: 0 30px 80px rgba(6, 182, 212, 0.2);
}

.results-card h2 {
    color: #0284c7;
    font-size: 1.8em;
    font-weight: 800;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.results-card .subtitle {
    color: #64748b;
    font-size: 0.95em;
    margin-bottom: 30px;
    font-weight: 500;
}

/* Button Styling */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 50%, #0284c7 100%) !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 1.1em !important;
    height: 60px !important;
    border-radius: 16px !important;
    border: none !important;
    box-shadow: 0 10px 30px rgba(6, 182, 212, 0.4) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 45px rgba(6, 182, 212, 0.6) !important;
}

.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* Risk Status Badges */
.risk-high {
    background: linear-gradient(135deg, #fca5a5 0%, #f87171 100%);
    color: white;
    padding: 25px;
    border-radius: 16px;
    font-size: 1.4em;
    font-weight: 800;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(244, 63, 94, 0.3);
    border-left: 6px solid #dc2626;
}

.risk-moderate {
    background: linear-gradient(135deg, #fdba74 0%, #fb923c 100%);
    color: white;
    padding: 25px;
    border-radius: 16px;
    font-size: 1.4em;
    font-weight: 800;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(249, 115, 22, 0.3);
    border-left: 6px solid #f97316;
}

.risk-low {
    background: linear-gradient(135deg, #86efac 0%, #4ade80 100%);
    color: white;
    padding: 25px;
    border-radius: 16px;
    font-size: 1.4em;
    font-weight: 800;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(34, 197, 94, 0.3);
    border-left: 6px solid #16a34a;
}

/* Insight Boxes */
.insight-box {
    background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
    color: white;
    padding: 30px;
    border-radius: 16px;
    margin: 20px 0;
    box-shadow: 0 15px 40px rgba(6, 182, 212, 0.3);
    border: 2px solid rgba(6, 182, 212, 0.5);
    transition: all 0.3s ease;
}

.insight-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(6, 182, 212, 0.4);
}

.insight-box h4 {
    color: white;
    font-size: 1.2em;
    margin-bottom: 12px;
    font-weight: 800;
}

.insight-box p {
    font-size: 1.05em;
    line-height: 1.6;
    margin: 0;
}

.insight-box-green {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

/* Alert Messages */
.stInfo {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(3, 139, 180, 0.1) 100%) !important;
    border-left: 5px solid #0ea5e9 !important;
    border-radius: 12px !important;
    padding: 18px 24px !important;
    color: #0c4a6e !important;
    font-weight: 600 !important;
}

.stSuccess {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(21, 128, 61, 0.1) 100%) !important;
    border-left: 5px solid #22c55e !important;
    border-radius: 12px !important;
    padding: 18px 24px !important;
    color: #166534 !important;
    font-weight: 600 !important;
}

.stWarning {
    background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, rgba(234, 88, 12, 0.1) 100%) !important;
    border-left: 5px solid #f97316 !important;
    border-radius: 12px !important;
    padding: 18px 24px !important;
    color: #92400e !important;
    font-weight: 600 !important;
}

.stError {
    background: linear-gradient(135deg, rgba(244, 63, 94, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%) !important;
    border-left: 5px solid #f43f5e !important;
    border-radius: 12px !important;
    padding: 18px 24px !important;
    color: #7f1d1d !important;
    font-weight: 600 !important;
}

/* Input Elements */
.stNumberInput > div > div > input,
.stSlider > div > div > div > input,
.stSelectbox > div > div > select {
    border: 2px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 1em !important;
    transition: all 0.3s ease !important;
    background: white !important;
}

.stNumberInput > div > div > input:focus,
.stSlider > div > div > div > input:focus,
.stSelectbox > div > div > select:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.1) !important;
    outline: none !important;
}

/* Sidebar */
.stSidebar {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border-right: 2px solid rgba(6, 182, 212, 0.1);
}

.stSidebar [data-testid="stSidebarNav"] {
    background: linear-gradient(180deg, #f0f9ff 0%, #f0f4f8 100%);
}

.stSidebar h2 {
    color: #0284c7 !important;
    font-size: 1.3em !important;
    font-weight: 800 !important;
    margin-top: 25px !important;
}

/* Expander */
.stExpander {
    border: 2px solid rgba(6, 182, 212, 0.2) !important;
    border-radius: 12px !important;
    background: white !important;
}

.stExpander > details > summary {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(3, 139, 180, 0.05) 100%) !important;
    border-radius: 10px !important;
    padding: 16px !important;
    font-weight: 700 !important;
    color: #0284c7 !important;
}

/* Download Button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    width: 100% !important;
    border-radius: 16px !important;
    font-weight: 800 !important;
    font-size: 1.05em !important;
    height: 55px !important;
    box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4) !important;
    border: none !important;
    transition: all 0.3s ease !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 45px rgba(16, 185, 129, 0.6) !important;
}

/* Divider */
.stDivider {
    border-color: rgba(6, 182, 212, 0.2) !important;
    margin: 40px 0 !important;
}

/* Labels */
.stNumberInput label,
.stSlider label,
.stSelectbox label {
    font-weight: 700 !important;
    color: #1e293b !important;
    font-size: 1em !important;
}

/* Responsive */
@media (max-width: 768px) {
    .premium-header h1 {
        font-size: 2.2em;
    }

    .premium-header {
        padding: 40px 20px;
    }

    .input-card, .results-card {
        padding: 25px;
    }
}
</style>
""", unsafe_allow_html=True)


# --- 3. LOAD MODEL & SHAP EXPLAINER ---
@st.cache_resource
def load_assets():
    pipeline = joblib.load('pipeline.pkl')
    explainer = joblib.load('shap_explainer.pkl')
    return pipeline, explainer


try:
    model, explainer = load_assets()
except Exception as e:
    st.error(f"❌ Error loading model/explainer: {e}")
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### 👨‍⚕️ Patient Information")
    st.info("📝 Fill the patient details in the main panel to get AI-based cardiac risk assessment.")

    st.markdown("---")
    st.markdown("### 💡 Health Tips")
    st.success("✅ Maintain a healthy, balanced diet")
    st.success("✅ Exercise regularly (30 mins daily)")
    st.success("✅ Monitor BP & cholesterol levels")
    st.success("✅ Avoid smoking & excessive alcohol")
    st.success("✅ Manage stress effectively")

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#64748b;font-size:0.85em;font-weight:600;'>🏆 Cardiac Risk Assessment v2.0<br>AI-Powered Diagnostic Support</p>",
        unsafe_allow_html=True)

# --- 5. PREMIUM HEADER ---
st.markdown("""
<div class='premium-header'>
    <h1>🏥 Cardiac Risk Assessment Dashboard</h1>
    <p>Advanced AI-Powered Diagnostic Support for Heart Health</p>
</div>
""", unsafe_allow_html=True)

# --- 6. INPUT SECTION ---
col1, col2 = st.columns([1.2, 1.8], gap="large")

with col1:
    st.markdown("""
    <div class='input-card'>
        <h2>📋 Patient Clinical Data</h2>
        <p class='subtitle'>Enter accurate patient details for best prediction accuracy</p>
    </div>
    """, unsafe_allow_html=True)

    # Numerical Inputs
    age = st.number_input("👤 Age (years)", 1, 120, 45, help="Patient age in years")
    rbp = st.slider("💓 Resting BP (mm Hg)", 80, 200, 120, help="Systolic blood pressure at rest")
    chol = st.slider("🩸 Serum Cholesterol (mg/dl)", 100, 600, 200, help="Total cholesterol level")
    thalach = st.slider("❤️ Max Heart Rate", 60, 220, 150, help="Peak heart rate achieved")
    oldpeak = st.number_input("📊 ST Depression", 0.0, 10.0, 0.0, step=0.1, help="ST segment depression value")

    st.markdown("<div class='input-divider'></div>", unsafe_allow_html=True)

    # Categorical Inputs
    gender = st.selectbox("⚧️ Gender", ["Male", "Female"])
    cp = st.selectbox("🫀 Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"])
    fbs = st.selectbox("🍬 Fasting Blood Sugar > 120", ["False", "True"])
    restecg = st.selectbox("📈 Resting ECG Results", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
    exang = st.selectbox("🏃 Exercise Induced Angina", ["No", "Yes"])
    slope = st.selectbox("📉 ST Slope", ["Upsloping", "Flat", "Downsloping"])

    # Prepare input DataFrame
    input_data = pd.DataFrame({
        'age': [age],
        'gender': [1 if gender == "Male" else 0],
        'chest_pain_type': [cp],
        'resting_blood_pressure': [rbp],
        'cholesterol': [chol],
        'fasting_blood_sugar': [1 if fbs == "True" else 0],
        'resting_ecg': [restecg],
        'max_heart_rate': [thalach],
        'exercise_induced_angina': [1 if exang == "Yes" else 0],
        'st_depression': [oldpeak],
        'st_slope': [slope],
        'num_major_vessels': [0],
        'thalassemia': ["Normal"]
    })

# --- 7. RESULTS SECTION ---
with col2:
    st.markdown("""
    <div class='results-card'>
        <h2>🔍 Diagnostic Analysis</h2>
        <p class='subtitle'>Click to generate comprehensive AI-powered diagnostic report</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Generate Diagnostic Report", use_container_width=True):
        preprocessor = model.named_steps['preprocessor']
        processed_input = preprocessor.transform(input_data)
        prob = model.predict_proba(input_data)[0][1]

        # --- Risk Gauge Chart ---
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=int(prob * 100),
            title={'text': "<b>Cardiac Risk Score</b>", 'font': {'size': 24, 'color': '#0284c7'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': '#64748b'},
                'bar': {'color': "#dc2626" if prob > 0.7 else "#f97316" if prob > 0.3 else "#16a34a", 'thickness': 0.7},
                'steps': [
                    {'range': [0, 30], 'color': "#f0fdf4"},
                    {'range': [30, 70], 'color': "#fffbeb"},
                    {'range': [70, 100], 'color': "#fef2f2"}
                ],
                'threshold': {
                    'line': {'color': "#dc2626", 'width': 5},
                    'thickness': 0.8,
                    'value': 70
                }
            },
            number={'font': {'size': 50, 'color': '#0284c7', 'family': 'Arial Black'}}
        ))
        fig.update_layout(
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(255,255,255,0)",
            font={'family': "Inter, sans-serif", 'color': "#1e293b", 'size': 14},
            height=420,
            margin=dict(l=20, r=20, t=80, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Status Badge ---
        if prob > 0.7:
            st.markdown(f"<div class='risk-high'>🛑 HIGH RISK - IMMEDIATE ACTION REQUIRED</div>", unsafe_allow_html=True)
            st.error(
                "⚠️ **URGENT:** Immediate consultation with a cardiologist is strongly recommended. Comprehensive cardiac evaluation needed.")
        elif prob > 0.3:
            st.markdown(f"<div class='risk-moderate'>⚠️ MODERATE RISK - CLOSE MONITORING NEEDED</div>",
                        unsafe_allow_html=True)
            st.warning("💡 Regular medical checkups and preventive lifestyle modifications are recommended.")
        else:
            st.markdown(f"<div class='risk-low'>✅ LOW RISK - GOOD HEALTH STATUS</div>", unsafe_allow_html=True)
            st.success(
                "🌟 Patient appears to be in good cardiac health. Maintain current lifestyle and periodic checkups.")

        # --- AI Insights ---
        st.markdown("---")
        st.markdown("## 📊 AI-Powered Insights")

        shap_result = explainer.shap_values(processed_input)
        s_val = shap_result[1][0] if isinstance(shap_result, list) else shap_result[0]
        if len(np.array(s_val).shape) > 1:
            s_val = s_val[:, 1]

        feature_names = preprocessor.get_feature_names_out()
        clean_names = [name.split('__')[-1] for name in feature_names]

        feature_impact = pd.Series(s_val, index=clean_names).sort_values(ascending=False)
        top_positive = feature_impact.index[0]
        top_negative = feature_impact.index[-1]

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(f"""
            <div class='insight-box'>
                <h4>🔴 Major Risk Factor</h4>
                <p><strong>{top_positive.replace('_', ' ').title()}</strong></p>
                <p style='font-size:0.9em; margin-top:10px; opacity:0.9;'>This factor significantly increases cardiac risk. Focus on monitoring and management.</p>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown(f"""
            <div class='insight-box insight-box-green'>
                <h4>🟢 Protective Factor</h4>
                <p><strong>{top_negative.replace('_', ' ').title()}</strong></p>
                <p style='font-size:0.9em; margin-top:10px; opacity:0.9;'>This factor helps reduce cardiac risk. Continue maintaining this aspect.</p>
            </div>
            """, unsafe_allow_html=True)

        # --- SHAP Analysis ---
        with st.expander("🔬 View Advanced SHAP Analysis", expanded=False):
            st.info(
                "📌 SHAP (SHapley Additive exPlanations) analysis shows how each feature contributes to the prediction.")

            fig, ax = plt.subplots(figsize=(12, 7))
            fig.patch.set_facecolor('#ffffff')
            ax.set_facecolor('#ffffff')

            base_val = float(explainer.expected_value[1]) if hasattr(explainer.expected_value, "__len__") else float(
                explainer.expected_value)
            shap.plots.waterfall(shap.Explanation(
                values=s_val,
                base_values=base_val,
                data=processed_input[0],
                feature_names=clean_names
            ), show=False)

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

        st.markdown("---")

        # --- Download Report ---
        report = input_data.copy()
        report['risk_score'] = int(prob * 100)
        report['risk_level'] = 'HIGH' if prob > 0.7 else 'MODERATE' if prob > 0.3 else 'LOW'

        csv_data = report.to_csv(index=False)
        st.download_button(
            label="📥 Download Diagnostic Report",
            data=csv_data,
            file_name="cardiac_diagnostic_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(3, 139, 180, 0.05) 100%); 
                    border: 2px dashed #0ea5e9; border-radius: 16px; padding: 40px; text-align: center;'>
            <h3 style='color: #0284c7; margin-bottom: 10px;'>👈 Ready for Analysis</h3>
            <p style='color: #64748b; font-size: 1.05em;'>Fill in the patient data on the left panel and click the "Generate Diagnostic Report" button to see detailed results and AI-powered insights.</p>
        </div>
        """, unsafe_allow_html=True)
