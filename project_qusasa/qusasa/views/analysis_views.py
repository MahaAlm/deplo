import streamlit as st 
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import os


openai_api_key = "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"


def chat_with_csv(df,prompt):
    llm = OpenAI(api_token=openai_api_key)
    df = SmartDataframe(df, config={"llm": llm})
    result = df.chat(prompt)
    print(result)
    return result