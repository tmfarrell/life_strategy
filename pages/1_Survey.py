import random

import streamlit as st
import pandas as pd
import plotly.express as px
#from streamlit_extras.app_logo import add_logo

if not 'FREQUENCY' in st.session_state.keys():
  st.session_state['FREQUENCY'] = [
    'Never', 'Less Than Monthly', 'Monthly', 'Weekly', 'Daily'
  ]

MARTIAL_STATUS = [
  'Single', 'Stable Relationship', 'Married', 'Widowed', 'Seperated', 'Divorced'
]

# strategic life metrics
SLM = {
  'Finances': {
    'Salary': (st.select_slider, list(range(10)), 'Monthly net income ($k)', 0),
    'Savings rate': (st.select_slider, [10 * x for x in range(6)], 'Percentage income saved (%)', 0)
  }, 
  'Health': {
    'Subjective assessment of own health': (
      st.select_slider, ['Very Good', 'Good', 'Average', 'Bad', 'Very Bad'], None, 'Average'
    ),
    'Frequency of sports': (st.select_slider,st.session_state['FREQUENCY'][:-1], None, 'Never')
  }, 
  'Relationships': {
    'Significant other': (
      st.selectbox, MARTIAL_STATUS, "Relationship status", 'Single'
     ),
    'Number of children': (st.select_slider, list(range(6)), None, 0),
    'Number of close friends': (st.select_slider, list(range(10)), None, 0)
  }, 
  'Community': {
    'Frequency of going to church': (st.select_slider, st.session_state['FREQUENCY'], None, 'Never'),
    'Societal engagement': (st.select_slider, st.session_state['FREQUENCY'][:-1], None, 'Never')
  },
  'Interests and entertainment': {
    'Liesure': (st.select_slider, list(range(11)), 'Hours of spare time per weekday', 0)
  }, 
  'Personal care': {
    'Sleep': (st.select_slider, list(range(4, 12)), 'Hours of sleep per weekday', 9),
    'Nutrition': (
      st.select_slider, ['Never', 'Sometimes', 'Often', 'Very Often'], 
      'Attention paid to health-conscious nutrition', 'Never'
    )
  }
}

st.session_state['SLM'] = SLM
st.session_state['BASELINE'] = {
  sla: {slm: SLM[sla][slm][-1] for slm in SLM[sla]} for sla in SLM
}

# Main Streamlit app
def main():

    if not 'survey_submitted' in st.session_state: 
      st.session_state['survey_submitted'] = False


    if not st.session_state['survey_submitted']: 

      st.title("Survey")
      st.markdown(
        """
          Fill out this survey about your life. 
        """
      )

      with st.form('ls_survey'): 
        if not 'portfolio' in st.session_state: 
          st.session_state['portfolio'] = {}
        
        for sla in SLM: 
          st.markdown(f"#### {sla}")
          if not sla in st.session_state['portfolio']:
            st.session_state['portfolio'][sla] = {}
          
          cols = st.columns(len(SLM[sla]), gap='medium')
          for slm, col in zip(SLM[sla], cols): 
            component, choices, desc, baseline = SLM[sla][slm]
            
            if slm != 'Significant other': 
              if slm in st.session_state['portfolio'][sla]: 
                default = st.session_state['portfolio'][sla][slm] 
              else: 
                default = baseline 
              st.session_state['portfolio'][sla][slm] = col.select_slider(slm, options=choices, value=default)
            
            else: 
              if slm in st.session_state['portfolio'][sla]: 
                default = MARTIAL_STATUS.index(st.session_state['portfolio'][sla][slm])
              else: 
                default = MARTIAL_STATUS.index(baseline)

              st.session_state['portfolio'][sla][slm] = col.selectbox(slm, options=choices, index=default)
            
            if desc: 
              col.caption(desc)

        st.session_state['survey_submitted'] = st.form_submit_button(label="Submit", type="primary")

    if st.session_state['survey_submitted']: 
      st.markdown(
        """
          
        ##### Thanks for your submission! Go to the Benchmark page to see your results.
        """
      )

    #add_logo("strategy.png", height=100)

if __name__ == "__main__":
    main()
