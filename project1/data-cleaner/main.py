import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter &cleaner", layout="wide")
st.title("📁File Converter & Cleaner")
st.write("Upload your CSV and Excel file to clean the data convert formats effortlessly")

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
            ext = files.split(".")[-1]
            df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

            st.subheader(f" {file.name} - preview")
            st.dataframe(df.head())

            if st.checkbox(f"fill Missing Values - {file.name}"):
                df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
                st.success("Missing values filled successfully")
                st.dataframe(df.head())

            selected_colums = st.multiselect(f"Select columns - {file.name}",df.columms, default=df.colums())
            df= df[selected_colums]
            st.dataframe(df.head())

            if st.checkbox(f"show chart - {file.name}") and not df.select_dtypes(include="number").empty:
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

                formate_choice = st.radio(f"convert {file.name} to:", ["CSV", "Excel"], key=file.name)

                if st.button(f"📥Download, {file.name} as {formate_choice}"):
                    output = BytesIO()
                    if formate_choice == "CSV":
                        df.to_csv(output, index=False)
                        mime = "text/csv"
                        new_name = file.name.replace(ext, ".csv")
                    else:
                        df.to_excel(output, index=False)
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        new_name = file.name.replace(ext, ".xlsx")
                    output.seek(0)
                    st.download_button("📥Download file", file_name=new_name, data=output, mime=mime)
                    st.success("processing complete")
