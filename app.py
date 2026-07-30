#======LOAD MODULES===========================
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt   #ocr
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np



st.set_page_config(layout="wide")

#to give title
st.title("AI RESUME GENRATION")
st.write("""this app helps user to build customized professional
resume with latest job apply links""")

st.image("bg.png")

st.sidebar.title("Fill Important Data")
st.sidebar.image("bg.png")

GOOGLE_API_KEY = st.sidebar.text_input("Gemini-API",type = "password")
GROQ_API_KEY = st.sidebar.text_input("Groq-API",type = "password")
TAVILY_API_KEY = st.sidebar.text_input("Tavily-API",type = "password")

all_API = [GOOGLE_API_KEY,GROQ_API_KEY,TAVILY_API_KEY ]
if not all(all_API):
    st.error("Must give API keys")
    st.stop()
elif all(all_API):
    st.success("API KEYS LOADED SUCCESSFULLY")
else:
    st.info("PASS ALL API-KEYS")

# MULTISELECT OPTION
options = ["Delhi", "Mumbai",
           "Pune", "Banglore", 
           "Gurugram/Gurgaon"]
location = st.sidebar.multiselect("Select Location",
                                  options = options)

profile_op = ["Data Analysts", "AI Engineer", 
            "Gen AI Developer", "Full-Stack Dev", 
            "Data Scientist"]
profile = st.sidebar.multiselect("Select Job Profile",
                                options = profile_op)

model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)

st.markdown("""###Get User Info""")
user_info = st.text_area("""Write your Resume description: """)

# response = model.invoke("Hello Buddy!")
# response.content[-1]['text']

def search_latest_news_jobs(query):
  """This function helps to fetch latest
  news or jobs related article using
  tavily"""
  client = TavilyClient(
      api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response

  agent = create_agent(
    model = model,
    tools = [
        search_latest_news_jobs])
# agent

def main_agent(agent, query):
    """This is main agent, or leader agent
    orchestrate sub agents"""

    # Giving prompt to create detailed prompt
    # for code generation
    prompt = """You are AI assistant and
    below given is a prompt, your
    task is to give detailed prompt for
    this.
    You are a professional Resume generator
    where user will give their personal info,
    you have to create detailed Resume
    for students or professional one,
    it must be with dynamic UI and UX and,
    with advanced CSS Professional Designing
    Make sure to give output in HTML format only
    no markdowns allowed
     """

    response = agent.invoke({
        'messages': [{'role': 'user','content': prompt}]})

    detailed_prompt = response['messages'][-1].content[-1]['text']

    # SAVE PROMPT using File Handling
    with open('prompt.txt', 'w') as f:
        f.write(detailed_prompt)

    user_details = f"""Below Given is a user details
    generate Resume based on that, if not
    given keep: Default Resume: Python Developer
    user details: {query}"""

    final_prompt = prompt + detailed_prompt + user_details

    # CODE GENERATION
    response = agent.invoke({
        'messages': [{'role': 'user','content': final_prompt}]})
    code = response['messages'][-1].content[-1]['text']

    return code

    # code = main_agent(agent, "Laki, GEN AI EXPERT")
    # from IPython import display as DISPLAY
    # DISPLAY.HTML(code)

def get_jobs(
    agent,
    Location="Noida, Delhi",
    Profile="Data Analyst, AI Engineer"
):
    # Job search prompt
    prompt = f"""
    Based on the user-given job profile, fetch the latest job openings
    from Naukri, LinkedIn, Indeed, or other popular job portals.

    Requirements:
    - Job Profile: {Profile}
    - Location: {Location}
    - Show only relevant jobs.
    - Include:
        * Job Profile Name
        * Company Name
        * Location
        * Salary (if available)
        * Job Description (short)
        * Direct Apply Link
    - Display at least 10-20 results.
    - Generate the output in professional HTML format.
    - Use dynamic Naukri-style cards with modern CSS.
    - No Markdown.
    """

    # Invoke AI agent
    response = agent.invoke({
        'messages': [{'role': 'user','content': prompt}]})

    detailed_prompt = response['messages'][-1].content[-1]['text']

    return code


# Example Usage
# code = get_jobs(agent)
# from IPython.display import HTML, display
# display(HTML(code))


if st.button("Generate Resume"):
    with st.spinner("Agent Running"):
        code = main_agent(agent, user_info)
        st.html(code,width="stretch",
                unsafe_allow_javascript=True)

        st.divider()  # to give horizontal div

        job_code = get_jobs(agent, location, profile)
        st.html(jobe_code,width="stretch",
                unsafe_allow_javascript=True)
