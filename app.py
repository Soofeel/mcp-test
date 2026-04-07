from aprism_identifier import index_text
import streamlit as st
import tempfile
import os
import re

st.set_page_config(layout="wide", page_title="Aprism Identifier")

import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

@st.cache_resource
def load_identifier():
    from aprism_identifier import Aprism_Identifier
    return Aprism_Identifier()

identifier = load_identifier()
col1, col2 = st.columns(2)

with col1:
    st.header("📝 입력")

    prompt_text = st.text_area("텍스트를 입력하세요", height=300)

    uploaded_file = st.file_uploader("또는 PDF 파일을 업로드하세요", type=["pdf"])

    run_button = st.button("🔍 분석 실행")
with col2:
    st.header("📄 분석 결과")

    if run_button:
        file_path = None

        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                file_path = tmp_file.name

        try:
            result = identifier(prompt_text, file_path=file_path)
            result_text = index_text(result['content'], 'abstracted_text')

            st.text_area("출력 결과", value=result_text, height=500)
            st.success("분석 완료 ✅")

            st.caption(f"⏱️ duration {result['duration']:.5f}s")

        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")
