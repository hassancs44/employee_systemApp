from pathlib import Path
import os
import streamlit as st
import pandas as pd

# --------------------------------------------
# 1) حدد BASE_DIR → يصل إلى مجلّد employee_system/
# --------------------------------------------
BASE_DIR     = Path(__file__).resolve().parent.parent.parent
REPORTS_XLS  = BASE_DIR / "reports_data.xlsx"
REPATT_DIR   = BASE_DIR / "reports_attachments"

# 2) تأكد من وجود مجلّد مرفقات البلاغات المشترك
REPATT_DIR.mkdir(parents=True, exist_ok=True)

# إعداد صفحة عرض البلاغات
st.set_page_config(page_title="قسم تقنية المعلومات - البلاغات", layout="wide")
st.markdown("<h1 style='color:#006db3;'>قسم تقنية المعلومات - البلاغات الواردة</h1>", unsafe_allow_html=True)
st.markdown("---")

# عرض البلاغات من ملف Excel المشترك
if not REPORTS_XLS.exists():
    st.info("لا توجد بلاغات في الوقت الحالي.")
else:
    df = pd.read_excel(REPORTS_XLS)
    if df.empty:
        st.info("لا توجد بلاغات في الوقت الحالي.")
    else:
        for idx, row in df.iterrows():
            with st.expander(f"{row['timestamp']} - {row['hospital']} - {row['department']}"):
                st.markdown(f"**المستشفى:** {row['hospital']}")
                st.markdown(f"**القسم:** {row['department']}")
                st.markdown(f"**الوقت:** {row['timestamp']}")
                st.markdown(f"**التفاصيل:** {row['description']}")
                attachment = row.get('attachment', '')
                if pd.notnull(attachment) and attachment:
                    file_path = REPATT_DIR / str(attachment)
                    if file_path.exists():
                        with open(file_path, 'rb') as f:
                            st.download_button(
                                label="📥 تحميل المرفق",
                                data=f,
                                file_name=str(attachment),
                                mime="application/octet-stream"
                            )
                    else:
                        st.write("المرفق غير موجود.")
                # زر لإتمام وحذف البلاغ
                if st.button("إتمام المشكلة", key=f"resolve_{idx}"):
                    df = df.drop(idx)
                    df.to_excel(REPORTS_XLS, index=False)
                    st.success("تم إتمام البلاغ وحذفه.")
                    st.experimental_rerun()
