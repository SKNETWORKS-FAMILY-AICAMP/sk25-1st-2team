import MySQLdb
import streamlit as st

@st.cache_resource
def get_db():
    return MySQLdb.connect(
        host='175.196.76.209',
        user='play',
        passwd='123',
        db='team2',
        autocommit=True
    )