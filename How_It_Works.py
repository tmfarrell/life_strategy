
import streamlit as st


st.set_page_config(page_title="Your Life Strategy")

if not 'survey_submitted' in st.session_state: 
      st.session_state['survey_submitted'] = False

st.session_state['FREQUENCY'] = [
  'Never', 'Less Than Monthly', 'Monthly', 'Weekly', 'Daily'
]


st.title("Strategize Life")

st.markdown(
	"""
	**_Want to improve your life but not sure where to start?_**

	This app helps you build a strategy for improving your life, using a simple 3-step process and leveraging 
	the latest research and best practices on life satisfaction and strategy.<sup>[[ref]](#references)</sup>

	Follow the 3-step process, execute the personalized plan and _you will undoubtedly 
	find yourself with greater satisfaction in life!_
	""", unsafe_allow_html=True
)

print('''
st.markdown('  ')
st.markdown('  ')
st.markdown(
	"""
	##### How It Works
	"""
) 
''')

st.image("strategy_process.png", width=550)
st.markdown(
	"""
	  
	##### Take the <a style="color:red" href="Survey" target="_self">survey</a>  now!
	""", unsafe_allow_html=True
)

print('''
st.markdown(
	"""

	_What you do:_

	1. **:red[Survey]** your life's portfolio

	_What the app does:_

	2. **:red[Benchmark]** your estimated life satisfaction relative to optimal
	
	3. **:red[Strategize]** how to improve your life satisfaction and build a specific action plan

	"""
)

st.markdown('  ')
st.markdown('  ')
st.markdown('  ')
'''
)

st.markdown('  ')
st.markdown('  ')
st.markdown('  ')
st.divider()
st.markdown('  ')

st.markdown(
	"""
	##### References 

	1. Strack, Dyrchs and Bailey. "Use Strategic Thinking to Create the Life You Want" Harvard Business Review. Dec 2023. https://hbr.org/2023/12/use-strategic-thinking-to-create-the-life-you-want.
	2. Rumelt, Richard. Good Strategy/Bad Strategy. New York: Random House, 2011. 
	"""
)





