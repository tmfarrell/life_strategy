import random
from collections import OrderedDict
from itertools import product
from math import ceil

import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

if not 'FREQUENCY' in st.session_state.keys():
  st.session_state['FREQUENCY'] = [
    'Never', 'Less Than Monthly', 'Monthly', 'Weekly', 'Daily'
  ]

# strategic life metrics
SLM_REFERENCE_DATA = {
  'Health': {
    'Subjective assessment of own health': \
      OrderedDict(zip(['Very Good', 'Good', 'Average', 'Bad', 'Very Bad'], np.linspace(0, -30, 5))),
    'Frequency of sports': OrderedDict(zip(st.session_state['FREQUENCY'][:-1], np.linspace(0, 2, 4)))
  }, 
  'Personal care': {
    'Sleep': OrderedDict(zip(list(range(4, 12)), [-8, -4, -3, -2, -1, 0, -2, -4])),
    'Nutrition': OrderedDict(zip(['Never', 'Sometimes', 'Often', 'Very Often'], np.linspace(0, 3, 4)))
  }, 
  'Finances': {
    'Salary': OrderedDict(zip(list(range(10)), list(np.linspace(0, 8, 7)) + [8, 8, 8])),
    'Savings rate': OrderedDict(zip([10 * x for x in range(6)], [0, 1, 1.5, 2, 2, 2]))
  }, 
  'Relationships': {
    'Significant other': OrderedDict([
      ('Married', 4), ('Stable Relationship', 2), ('Single', 0), 
      ('Widowed', -1), ('Divorced', -1.5), ('Seperated', -4)
     ]),
    'Number of children': OrderedDict(zip(list(range(6)), [0, 1, 1.25, 1.5, 2, 1.5])),
    'Number of close friends': OrderedDict(zip(list(range(10)), np.linspace(0, 3, 10)))
  }, 
  'Community': {
    'Frequency of going to church': OrderedDict(zip(st.session_state['FREQUENCY'], np.linspace(0, 3, 5))),
    'Societal engagement': OrderedDict(zip(st.session_state['FREQUENCY'][:-1], np.linspace(0, 2, 4)))
  },
  'Interests and entertainment': {
    'Liesure': OrderedDict(zip(list(range(11)), [0, 0.25, 0.75, 1, 1, 0.8, 0.6, 0.4, 0, -0.5, -1]))
  }, 
}

OPTIMAL = {
  'Relationships': {
    'Significant other': 'Married',
    'Number of children': 4,
    'Number of close friends': 9
  }, 
  'Health': {
    'Subjective assessment of own health': 'Very Good',
    'Frequency of sports': 'Weekly'
  }, 
  'Community': {
    'Frequency of going to church': 'Daily',
    'Societal engagement': 'Weekly'
  },
  'Finances': {
    'Salary': 6,
    'Savings rate': 30
  }, 
  'Interests and entertainment': {
    'Liesure': 3
  }, 
  'Personal care': {
    'Sleep': 9,
    'Nutrition': 'Very Often'
  }
}

st.session_state['SLM_REFERENCE_DATA'] = SLM_REFERENCE_DATA
st.session_state['OPTIMAL'] = OPTIMAL

# Main Streamlit app
def main():
    if not st.session_state['survey_submitted']: 
      st.markdown('Submit your <a style="color:red" href="Survey" target="_self">Survey</a> first!', unsafe_allow_html=True)
    else: 
      st.title("Benchmark")

      for sla in SLM_REFERENCE_DATA: 

        num_cols = 2
        num_rows = int(ceil(len(SLM_REFERENCE_DATA[sla]) / 2))

        fig = make_subplots(
          rows=num_rows, cols=num_cols, vertical_spacing = 0.15,
          subplot_titles=list(SLM_REFERENCE_DATA[sla].keys())
        )

        row_cols_index = product(map(int, range(1, num_rows + 1)), map(int, range(1, num_cols + 1)))
        for slm, (row, col) in zip(SLM_REFERENCE_DATA[sla].keys(), row_cols_index):

          gap_gain_colors = ['rgba(255, 0, 0, 0.25)', 'rgba(0, 128, 0, 0.25)']

          X = list(range(len(SLM_REFERENCE_DATA[sla][slm].keys())))
          Y = list(SLM_REFERENCE_DATA[sla][slm].values())

          fig.add_trace(go.Scatter(x=X, y=Y, mode='lines', name="", hoverinfo='skip'), row=row, col=col) 
          fig.update_traces(line_color='lightgrey', line_width=0.5, row=row, col=col)
          fig.update_yaxes(showgrid=False)
          fig.update_xaxes(labelalias=dict(zip(
            range(len(SLM_REFERENCE_DATA[sla][slm].keys())), map(str, SLM_REFERENCE_DATA[sla][slm].keys())
          )), showticklabels=True, tickmode='array', row=row, col=col)

          x_survey = list(SLM_REFERENCE_DATA[sla][slm].keys()).index(st.session_state['portfolio'][sla][slm])
          y_survey = SLM_REFERENCE_DATA[sla][slm][st.session_state['portfolio'][sla][slm]]
          x_optimal = list(SLM_REFERENCE_DATA[sla][slm].keys()).index(OPTIMAL[sla][slm])
          y_optimal = SLM_REFERENCE_DATA[sla][slm][OPTIMAL[sla][slm]]

          if col == 1: 
            fig.update_yaxes(title="Relative life satisfaction (RLU)", title_font_size=12, row=row, col=col)

          if st.session_state['SLM'][sla][slm][2]: 
            fig.update_xaxes(title=st.session_state['SLM'][sla][slm][2], title_font_size=12, row=row, col=col)

          if y_survey < y_optimal: 
            fig.add_hrect(
              y0=y_survey, y1=y_optimal,
              line=dict(width=0), fillcolor=gap_gain_colors[0], 
              row=row, col=col
            )
            y_to_max = round(y_optimal - y_survey, 2)
            if type(y_to_max) != int and y_to_max.is_integer(): 
              y_to_max = int(y_to_max)
            fig.add_annotation(
              x=x_optimal, 
              y=y_survey + ((y_optimal - y_survey) / 2),
              text= f'{y_to_max} RLUs to max', 
              font=dict(size=10, color='red'),
              showarrow=False, 
              row=row, col=col
            )

          if y_survey > 0: 
            fig.add_hrect(
              y0=0, y1=y_survey,
              line=dict(width=0), fillcolor=gap_gain_colors[-1], 
              row=row, col=col
            )

          # add survey point with lines 
          fig.add_scatter(
            x=[x_survey], y=[y_survey], name="", 
            marker=dict(color='grey', size=7.5, symbol='x'),
            row=row, col=col
          )
          #fig.add_shape(type='line',
          #              x0=0, y0=y_survey, x1=max(X), y1=y_survey,
          #              line=dict(color='grey', width=0.5, dash='dash'),
          #              row=row, col=col)
          fig.add_annotation(
            x=x_survey, y=y_survey,
            text="current", 
            font=dict(size=10, color='black'),
            showarrow=False, 
            yshift=-10, row=row, col=col
          )
          # add optimal point with lines 
          fig.add_scatter(
            x=[x_optimal], y=[y_optimal], name="", 
            marker=dict(color='lightgreen', size=7.5, symbol='cross'),
            row=row, col=col
          )
          #fig.add_shape(type='line',
          #              x0=0, y0=y_optimal, x1=max(X), y1=y_optimal,
          #              line=dict(color='lightgreen', width=0.5, dash='dash'),
          #              row=row, col=col)
          fig.add_annotation(
            x=x_optimal, y=y_optimal,
            text="max", font=dict(size=10, color='green'),
            showarrow=False, 
            yshift=10, row=row, col=col
          )

        for i in range(len(fig.layout.annotations)):
          #print(i, fig.layout.annotations[i])
          if fig.layout.annotations[i].text != 'current' \
            and not 'max' in fig.layout.annotations[i].text: 
            fig.layout.annotations[i].font = dict(size=16)
        
        fig.update_layout(
          title=sla, title_font_size=28, 
          showlegend=False, height=375 * num_rows
        )

        st.plotly_chart(fig)

      st.markdown(' ')
      st.markdown(' ')
      st.markdown(
        """
          
        ##### Go to the Strategize page to see your action plan!
        """
      )

      st.markdown(' ')
      st.divider()
      st.markdown(' ')
      _, c1, c2, _ = st.columns([1, 1, 1, 1])
      link = '<a style="color:grey" href="https://3dii87bqw3k.typeform.com/to/S5n2mSPK">Give Feedback</a>'
      c1.markdown(link, unsafe_allow_html=True)
      link = '<a style="color:grey" href="https://www.buymeacoffee.com/tfarrell01j">Support</a>'
      c2.markdown(link, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
