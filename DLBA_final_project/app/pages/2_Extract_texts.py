#!/usr/bin/env python
# coding: utf-8

import os
import io
import datetime
import pytesseract
import pandas as pd
import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes
from transformers import pipeline

# You will need to download a model
# to implement summarization from 
# HugginFace Hub.
#
# You may want to use following models:
# https://huggingface.co/Falconsai/text_summarization
# https://huggingface.co/knkarthick/MEETING_SUMMARY
# ...or any other you like, but think of 
# the size of the model (<1GB recommended)
#
####################################

# page headers and info text
st.set_page_config(
    page_title='Extract texts', 
    page_icon=':microscope:'
)
st.sidebar.header('Read text from an image')
st.header('Read text from an image', 
          divider='rainbow')

st.markdown(
    f"""
    Upload a photo and the application will give you the text in it
    as well as its summarization.
    """
)
st.divider()

def ocr_text(img, lang='eng'):
    """
    Takes the text from image.
    
    :lang: language is `eng` by default,
           use `eng+rus` for two languages in document

    """
    text = str(pytesseract.image_to_string(
        img,
        lang=lang
    ))
    return text

with st.spinner('Please wait, application is initializing...'):
    MODEL_SUM_NAME = 'Falconsai/text_summarization'
    SUMMARIZATOR = pipeline("summarization", model=MODEL_SUM_NAME)

st.write('#### Upload you image')
uploaded_file = st.file_uploader('Select an image file (JPEG format)')
if uploaded_file is not None:
    file_name = uploaded_file.name
    if '.jpg' in file_name:
        with st.spinner('Please wait...'):
            bytes_data = uploaded_file.read()
            img = Image.open(io.BytesIO(bytes_data))
            st.write('##### Your image uploaded')
            st.image(img)
            st.divider()
            
            # OCR
            text = ocr_text(img)
            st.write('#### Text extracted')
            st.write(text)
            st.divider()
            
            # summarization
            summary = SUMMARIZATOR(text, 
                                   max_length=1000, 
                                   min_length=30, 
                                   do_sample=False
                                  )[0]['summary_text']
            st.write('#### Text summary')
            st.write(summary)

            # logging
            msg = '{} - file "{}"\n'.format(
                datetime.datetime.now(),
                file_name
            )
            with open('history.log', 'a') as file:
                file.write(msg)
        
        # OCR
        
    else:
        st.error('File read error', icon='⚠️')

# Use example from the class with
# OCR model for text extracting from 
# the image or PDF file.
#
# Do not forget to add text summarization 
# model and display the output to the OCR 
# application's page  
####################################
