import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe
from datetime import datetime
import os

# —————————————————————————————————————————
# 1) مصادقة Google Sheets API عبر Streamlit Secrets
# —————————————————————————————————————————
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)
gc = gspread.authorize(creds)

SPREADSHEET_ID = st.secrets["gcp_service_account"]["spreadsheet_id"]
sh             = gc.open_by_key(SPREADSHEET_ID)
ws_requests    = sh.worksheet("Requests")   # ورقة طلبات الموظفين

# —————————————————————————————————————————
# 2) تجهيز مجلّد المرفقات محليًا (اختياري)
# —————————————————————————————————————————
ATTACH_DIR = "attachments"
os.makedirs(ATTACH_DIR, exist_ok=True)

# —————————————————————————————————————————
# 3) إعداد واجهة Streamlit
# —————————————————————————————————————————
st.set_page_config(page_title="نموذج موظف جديد", layout="centered")
st.markdown("<h2 style='color:#006db3;'>نموذج تسجيل موظف جديد</h2>", unsafe_allow_html=True)
st.markdown("---")

# —————————————————————————————————————————
# 4) نموذج الإدخال
# —————————————————————————————————————————
with st.form("employee_form"):
    name          = st.text_input("الاسم")
    id_number     = st.text_input("رقم الهوية")
    nationality   = st.text_input("الجنسية")
    uploaded_file = st.file_uploader(
        "أرفق النموذج الورقي (PDF أو صورة)", type=["pdf", "png", "jpg", "jpeg"]
    )
    submitted     = st.form_submit_button("إرسال")

    if submitted:
        # التحقق من تعبئة جميع الحقول
        if not (name and id_number and nationality and uploaded_file):
            st.error("🛑 يرجى تعبئة جميع الحقول وإرفاق الملف.")
        else:
            # حفظ المرفق محليًا
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename  = f"{id_number}_{timestamp}_{uploaded_file.name}"
            file_path = os.path.join(ATTACH_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # إضافة السطر الجديد إلى ورقة Requests
            ws_requests.append_row([
                name,
                id_number,
                nationality,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                filename,
                "بانتظار المعالجة"
            ], value_input_option="USER_ENTERED")

            st.success("✅ تم إرسال البيانات بنجاح.")
