import streamlit as st
import fetchcommits as ft
from datetime import datetime, timedelta

prstate = st.sidebar.radio("PR state :",("open","closed","WIP"))
repoowner = st.sidebar.text_input("Repo Owner :")
reponame = st.sidebar.text_input("Repo Name :")
timeframe = st.sidebar.number_input("Number of Days :")

if st.sidebar.button("Fetch Details"):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    lastweek = today - timedelta(days=int(timeframe))
    gf = ft.GitFetch()
    inputdict={"GITHUB_HOST":"https://github.com/","OWNER":repoowner,"REPO_NAME":reponame,"ACCESS_TOKEN":""}
    gf.readinputs(False,inputdict)
    if prstate != "WIP":
        op = gf.fetchpullreqs(prstate,lastweek)
    else:
        op = gf.fetchpullreqs(prstate,lastweek,True)
    st.text(str(op))



