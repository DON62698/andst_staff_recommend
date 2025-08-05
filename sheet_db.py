import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 設定授權範圍
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

# 連接 Google Sheets
sheet = client.open_by_url(st.secrets["sheet_url"]).sheet1

def read_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def upsert_row(date, data_dict):
    df = read_data()
    if date in df["date"].values:
        idx = df.index[df["date"] == date][0] + 2  # +2 是因為 Google Sheets 的 index 從第 2 列開始（第 1 是欄位名）
        sheet.update(f"A{idx}:D{idx}", [[date] + list(data_dict.values())])
    else:
        sheet.append_row([date] + list(data_dict.values()))


