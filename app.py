import time

import streamlit as st
from langchain_community.llms import Tongyi
from streamlit_markmap import markmap

from inference.chain import (
    gen_job_techtree_v2,
    gen_job_task,
    gen_job_intro,
    gen_job_promotion,
    gen_job_faq,
)
from inference.utils import build_joblist_markmap


def render_job_intro(job_name):
    ret = gen_job_intro(job_name)
    st.write("## 岗位职责")
    st.write(ret)


def render_job_task(job_name):
    ret = gen_job_task(job_name)
    st.write("## 岗位任务")
    st.write(ret)


def render_job_techtree(job_name):
    job_list = gen_job_techtree_v2(job_name)
    job_markmap = build_joblist_markmap(job_list)
    st.write("## 岗位技能树")
    markmap(job_markmap)


def render_job_promotion(job_name):
    ret = gen_job_promotion(job_name)
    st.write("## 岗位晋升路线")
    st.write(ret)


def render_job_faq(job_name):
    ret = gen_job_faq(job_name)
    st.write("## 岗位常见问题")
    st.write(ret)


llm = Tongyi()

st.title("职业路线图助手")

job_name = st.text_input(
    "请输入职业名称", key="job_name", type="default", placeholder="服务端开发工程师"
)

bar = st.progress(0, text="未开始")

if not job_name:
    st.warning("职业名称不能为空！")
    st.stop()
else:
    bar.progress(0, text="正在生成岗位介绍...")
    render_job_intro(job_name)
    bar.progress(10, text="正在生成岗位任务描述...")
    render_job_task(job_name)
    bar.progress(30, text="正在生成岗位技能树...")
    render_job_techtree(job_name)
    bar.progress(70, text="正在生成岗位晋升路线...")
    render_job_promotion(job_name)
    bar.progress(90, text="正在生成岗位常见问题...")
    render_job_faq(job_name)
    bar.progress(100, text="已完成")
