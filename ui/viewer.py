import streamlit as st


from services.markdown_renderer import render_markdown

def get_preview_html(content):
    return render_markdown(content)