import pymysql
import streamlit as st

# PyMySQL이 MySQLdb인 것처럼 동작하도록 설정
pymysql.install_as_MySQLdb()
import MySQLdb


@st.cache_resource
def get_db():
    return MySQLdb.connect(
        host='175.196.76.209',
        user='play',
        passwd='123',
        db='team2',
        autocommit=True
    )
