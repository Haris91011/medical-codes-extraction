import streamlit as st
import re
# Custom function to display success messages with black text
def subheader_func(message):
    st.markdown(
        f"""
        <div style="color: black; background-color: #DFF2BF; border: 0.5px solid #4CAF50; padding: 5px; border-radius: 5px;">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )

def warning_message(message):
    st.markdown(
        f"""
        <div style="color: white; background-color: #FF0000; border: 0.5px solid #4CAF50; padding: 5px; border-radius: 5px;">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )
    
def output_message(message):
    color = "#EF4444" if "Irrelevant" in message else "black"  # Red for Irrelevant, black for others
    st.markdown(
        f"""
        <div style="color: {color}; padding: 5px; border-radius: 5px; font-size: 25px;">
            <b>{message}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

def output_final(message):
    st.markdown(
        f"""
        <div style="color: black; padding: 5px; border-radius: 5px; font-size: 15px;">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )

def reformat_bullet_points(text):
    reformatted = re.sub(r"- (\d+)", r"\n- \1", text.strip())
    reformatted = re.sub(r"\s*\.\s*$", "", reformatted)
    return reformatted