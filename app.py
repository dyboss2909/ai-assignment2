import contextlib
import io

import streamlit as st

from run_all_tasks import task1, task2, task3

st.title("Simple Intelligent Agents - Assignment 2")

TASKS = [
    ("Task 1: Reflex Delivery Agent", task1),
    ("Task 2: Reflex Cat-Agent", task2),
    ("Task 3: Cat-Agent vs Random Mouse-Agent", task3),
]

tabs = st.tabs([name for name, _ in TASKS])

for (name, run_task), tab in zip(TASKS, tabs):
    with tab:
        st.subheader(name)
        if st.button("Run", key=name):
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                run_task()
            st.code(buffer.getvalue())
