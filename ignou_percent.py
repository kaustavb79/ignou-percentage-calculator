import streamlit as st
import pandas as pd
import numpy as np
import time
from read_percentage import IgnouPercentage as IP

st.set_page_config(page_title="IGNOU BCA/MCA CALCULATOR", page_icon=None, layout='wide', initial_sidebar_state='auto')
st.title('IGNOU BCA/MCA CALCULATOR')

st.markdown("Calculate your BCA/MCA semester-wise/total percentage and grade...")
# roll_no = st.text_input("Enter Enrollment No. :")
# option = st.selectbox("Choose Program :",('BCA','MCA'))
with st.sidebar.form(key='my_form'):
    roll_no = st.text_input("Enter Enrollment No. :")
    option = st.selectbox("Choose Program :",('BCA','MCA'))
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    print(roll_no)
    print(option)
    student = IP()
    with st.spinner("Fetching Data..."):
        RESULT = student.getStudent_RollNo_And_Program(roll_no=roll_no,program=option)

    if type(RESULT) == str:
        st.error(RESULT)
    else:  
        for x in RESULT[2][:3]:
            print(x)
            st.write(x)

        assignment_total = 0.0
        term_end = 0.0
        total = 0.0
        credits = 0
        subjects = 0
        pd.set_option('display.max_columns',None)
        for semester,results in RESULT[0].items():
            st.markdown('**'+'-'*175+'**')
            st.write("**"+semester+"**")
            __course_code=[]
            __name=[]
            __assignment=[]
            __term_end=[]
            __total=[]
            __status = []
            __credits=[]
            # sem_total = 0.0
            # sem_percent = 0.0
            # print(results)
            for lst in results.values():
                __course_code.append(lst[0])
                __name.append(lst[1])
                __assignment.append(str(round(lst[2],2)))
                __term_end.append(str(round(lst[3],2)))
                __total.append(str(round(lst[4],2)))
                __credits.append(lst[6])
                __status.append(lst[5])
                sem_total = sum(map(float,__total))
                sem_percent = sem_total/len(__name)
            st.write(pd.DataFrame({
                'COURSE CODE':__course_code,
                'SUBJECT/COURSE':__name,
                'ASSIGNMENT (30%)':__assignment,
                'TERM-END/LAB (70%)':__term_end,
                'TOTAL':__total,
                'STATUS':__status,
                'CREDITS':__credits
            }))
            st.markdown('**Semester Total** (*out of '+str(len(__name)*100)+'*) = {:.2f}'.format(sem_total))
            st.markdown('**Semester-wise Performance** = {:.2f}'.format(sem_percent)+'%')
            st.markdown('**'+'-'*175+'**')
            total += sem_total
            subjects += len(__name)
            credits += sum(__credits)
        st.markdown('**'+'*'*175+'**')
        st.write('***RESULTS***')
        st.markdown('**'+'*'*175+'**')
        st.markdown('**Total number of subjects** = *'+str(subjects)+'*')
        st.markdown('**Total** (*out of '+str(subjects*100)+'*) = {:.2f}'.format(total))
        st.markdown('**Cululative Percentage** = {:.2f}'.format(total/subjects)+'%')
        st.markdown('**Total Credits** = *'+str(credits)+'*')
        st.markdown("***Marks for Project in assignment***")