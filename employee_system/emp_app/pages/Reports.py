import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
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
gc   = gspread.authorize(creds)

SPREADSHEET_ID = st.secrets["gcp_service_account"]["spreadsheet_id"]
sh             = gc.open_by_key(SPREADSHEET_ID)
ws_reports     = sh.worksheet("Reports")   # ورقة بلاغات الـIT

# —————————————————————————————————————————
# 2) تجهيز مجلّد المرفقات محليًا (اختياري)
# —————————————————————————————————————————
ATTACH_DIR = "reports_attachments"
os.makedirs(ATTACH_DIR, exist_ok=True)

# —————————————————————————————————————————
# 3) إعداد واجهة Streamlit
# —————————————————————————————————————————
st.set_page_config(page_title="إرسال بلاغ IT", layout="centered")
st.markdown(
    "<h1 style='text-align:center; color:#006db3;'>نموذج إرسال بلاغ لقسم تقنية المعلومات</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# قائمة المستشفيات
hospitals = [
    "مستشفى السلام",
    "مستشفى الحرم",
    "مركز باب جبريل",
    "مركز الصافية"
]

# مدخلات النموذج
hospital   = st.selectbox("اختر المستشفى", options=hospitals)
department = st.text_input("اسم القسم")
issue_desc = st.text_area("تفاصيل البلاغ")
attachment = st.file_uploader("إرفاق ملف (اختياري)", type=["png", "jpg", "pdf", "docx", "xlsx"])

# —————————————————————————————————————————
# 4) معالجة الإرسال
# —————————————————————————————————————————
if st.button("إرسال البلاغ"):
    if not (department and issue_desc):
        st.error("🛑 يرجى ملء جميع الحقول المطلوبة قبل الإرسال.")
    else:
        # حفظ المرفق محليًا إذا وُجد
        filename = ""
        if attachment:
            ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{ts}_{attachment.name}"
            with open(f"{ATTACH_DIR}/{filename}", "wb") as f:
                f.write(attachment.getbuffer())

        # إضافة الصف إلى ورقة Reports في Google Sheets
        ws_reports.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            hospital,
            department,
            issue_desc,
            filename
        ], value_input_option="USER_ENTERED")

        st.success("✅ تم إرسال البلاغ بنجاح.")
