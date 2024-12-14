import streamlit as st
from core.config import settings
from utils.cpt_llm import evaluate_codes,get_code_description
from core.connection import load_all_cpt_codes,load_all_icd_codes
from utils.css_styling import warning_message,output_final,output_message,reformat_bullet_points





st.markdown(
    """
    <style>
    /* Apply black text color globally */
    body, .stMarkdown, .stText, .stRadio, .stCheckbox, .stSelectbox, .stSlider, .stTextInput, .stNumberInput, .stTextarea, .stFileUploader, .stDateInput, .stTimeInput, .stColorPicker, .stJson, .stMetric, .stDataFrame, .stExpander, .stTable {
        color: black !important;
    }

    /* Apply white background to the button */
    .stButton > button {
        background-color: white !important;
        color: black !important;  /* Set text color to black */
        border: 2px solid black !important;  /* Set border to black */
    }

    /* Prevent background from being overridden */
    .stApp {
        background-color: white !important;
    }

    /* Hover effect for the button */
    .stButton > button:hover {
        background-color: #f0f0f0 !important;  /* Light grey hover effect */
        border-color: black !important;
    }

    </style>
    
    <style>
    /* Center-align the button */
    .center-button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    /* Styling for the spinner to make it black */
    .stSpinner > div {
        background-color: white !important;
        color: black !important;
    }
    
    </style>
    
    <style>
        .stTextInput input {
            background-color: white;
            border: 2px solid black;
            color: black;
        }
    </style>
    
    <style>
    [data-testid="stSidebarNav"] {
        background-image: url('https://cloudsolutions.com.sa/images/headers/cloudsolutions-logo.png');
        background-repeat: no-repeat;
        background-position: 20px 20px;
        background-size: 100px 100px;
        padding-top: 120px;
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Update the title section with new styles
st.markdown(
    """
    <style>
    .logo-container {
        position: fixed;
        top: 0;
        left: 50px;
        padding: 20px;
        z-index: 999;
    }
    
    .title-container {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 998;
        width: 100%;
        text-align: center;
    }

    .main-title {
        font-size: 24px;
        font-weight: bold;  /* Changed to bold */
        margin-bottom: 8px;
    }

    .black-text {
        color: black;
    }

    .red-text {
        color: #EF4444;
    }

    .sub-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 5px;
        color: #EF4444;  /* Added red color to match SOLUTIONS */
    }
    </style>
    
    <div class="logo-container">
        <img src="https://cloudsolutions.com.sa/images/headers/cloudsolutions-logo.png" alt="Logo" style="width: 80px; height: 80px;">
    </div>
    
    <div class="title-container">
        <h1 class="main-title">
            <span class="black-text">CLOUD</span>
            <span class="red-text">SOLUTIONS</span>
        </h1>
        <h2 class="sub-title">Treatment-to-Diagnosis Matching Using AI</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Adjust top margin to match new sizes
st.markdown("<div style='margin-top: 130px;'></div>", unsafe_allow_html=True)  # Reduced from 150px

# Set up your app's functionality (keeping your original code intact)
if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state.OPENAI_API_KEY = settings.OPENAI_API_KEY

if not st.session_state.OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it in your environment variables or Streamlit secrets.")
    st.stop()

# Manage session state for dynamic inputs
if 'icd_10_codes' not in st.session_state:
    st.session_state.icd_10_codes = []
if 'cpt_codes' not in st.session_state:
    st.session_state.cpt_codes = []

# Add these database connection functions






# Replace the columns section with this new code
col1, col2 = st.columns(2)

with col1:
    with st.expander("ICD-10 Codes", expanded=True):
        icd_codes = load_all_icd_codes()
        if icd_codes:
            selected_icds = st.multiselect(
                "",
                options=[code[0] for code in icd_codes],
                key="icd_multiselect",
                placeholder="Select ICD-10 codes..."
            )
            if selected_icds:
                st.session_state.icd_10_codes = selected_icds

with col2:
    with st.expander("CPT Codes", expanded=True):
        cpt_codes = load_all_cpt_codes()
        if cpt_codes:
            selected_cpts = st.multiselect(
                "",
                options=[code[0] for code in cpt_codes],
                key="cpt_multiselect",
                placeholder="Select CPT codes..."
            )
            if selected_cpts:
                st.session_state.cpt_codes = selected_cpts


# Replace the evaluation section with this version
if st.session_state.icd_10_codes and st.session_state.cpt_codes:
    st.markdown("---")
    
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("Analyze", key="process_button"):
        with st.spinner('Evaluating codes...'):
            codes = {
                "icd_10": [{"code": code} for code in st.session_state.icd_10_codes],
                "cpt_code": [{"code": code} for code in st.session_state.cpt_codes],
            }

            all_codes = st.session_state.icd_10_codes + st.session_state.cpt_codes
            codes_string = ",".join(all_codes)
            codes_data = get_code_description(codes_string)
            
            if isinstance(codes_data, dict) and 'data' in codes_data:
                summary_dict = {item['code']: item['summary'] for item in codes_data['data']}

                for key in codes:
                    for code_entry in codes[key]:
                        code = code_entry['code']
                        if code in summary_dict:
                            code_entry['summary'] = summary_dict[code]

                output = evaluate_codes(codes)
                if output:
                    final_output = reformat_bullet_points(output)
                    
                    if final_output == "- All CPT codes are relevant to ICD codes":
                        output_message("Relevant CPT Codes")
                        output_final(final_output)
                    else:
                        output_message("Irrelevant CPT Codes")
                        output_final(final_output)
                else:
                    warning_message("Error in code evaluation")
            else:
                warning_message("Please enter both ICD-10 and CPT codes.")
    st.markdown('</div>', unsafe_allow_html=True)

# Add "Clear All" button at the bottom
if st.button("Clear All Codes", key="clear_button_all"):
    st.session_state.icd_10_codes.clear()
    st.session_state.cpt_codes.clear()
    st.rerun()

