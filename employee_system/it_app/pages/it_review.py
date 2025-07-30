import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe
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

# —————————————————————————————————————————
# 2) افتح ملف الـSpreadsheet والورقة “Requests”
# —————————————————————————————————————————
SPREADSHEET_ID = st.secrets["gcp_service_account"]["spreadsheet_id"]
sh = gc.open_by_key(SPREADSHEET_ID)
ws_requests = sh.worksheet("Requests")

# —————————————————————————————————————————
# 3) مجلّد المرفقات محليًا (أنشئ إذا لم يكن موجودًا)
# —————————————————————————————————————————
ATTACH_DIR = "attachments"
os.makedirs(ATTACH_DIR, exist_ok=True)

# —————————————————————————————————————————
# 4) إعداد واجهة Streamlit
# —————————————————————————————————————————
st.set_page_config(page_title="قسم IT - الطلبات الواردة", layout="wide")
st.markdown("<h2 style='color:#006db3;'>قسم تقنية المعلومات - الطلبات الواردة</h2>", unsafe_allow_html=True)
st.markdown("---")

# —————————————————————————————————————————
# 5) جلب البيانات من ورقة Requests وعرضها
# —————————————————————————————————————————
df = get_as_dataframe(ws_requests).dropna(how="all")

if df.empty:
    st.info("لا توجد طلبات حالياً.")
else:
    for idx, row in df.iterrows():
        with st.expander(f"🔹 {row['الاسم']} – {row['رقم الهوية']}"):
            st.write(f"**الجنسية:** {row['الجنسية']}")
            st.write(f"**تاريخ الإرسال:** {row['تاريخ الإرسال']}")
            st.write(f"**الحالة:** {row['الحالة']}")

            # زر تحميل المرفق إن وُجد
            fname = row.get("اسم الملف", "")
            if fname:
                path = os.path.join(ATTACH_DIR, fname)
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        st.download_button(
                            label="📥 تحميل النموذج المرفق",
                            data=f,
                            file_name=fname,
                            mime="application/octet-stream"
                        )
                else:
                    st.warning("❌ المرفق غير موجود.")
