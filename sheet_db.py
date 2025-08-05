import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 驗證與連接 Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 
"https://www.googleapis.com/auth/drive"]
creds = 
ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], 
scope)
client = gspread.authorize(creds)

# 打開工作表
sheet = client.open_by_url(st.secrets["sheet_url"]).sheet1

# 讀取資料為 DataFrame
def read_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# 寫入或更新某一天的資料（以 date 為 key）
def upsert_row(date, app_new, app_exist, line, mode="app"):
    df = read_data()

    date_str = date.strftime("%Y-%m-%d")

    # 如果已存在該日期 → 更新
    if date_str in df["date"].values:
        idx = df[df["date"] == date_str].index[0]
        sheet.update_cell(idx + 2, 2, app_new)
        sheet.update_cell(idx + 2, 3, app_exist)
        sheet.update_cell(idx + 2, 4, line)
    else:
        sheet.append_row([date_str, app_new, app_exist, line])

