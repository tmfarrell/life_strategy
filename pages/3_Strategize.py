from itertools import product

import streamlit as st
import pandas as pd


def build_rls_df():
	#optimal_diff = 0 
	optimal_delta = pd.DataFrame()
	for sla in st.session_state['portfolio']:
	  for slm in st.session_state['portfolio'][sla]: 
	    value = round(st.session_state['SLM_REFERENCE_DATA'][sla][slm][st.session_state['portfolio'][sla][slm]], 2)
	    optimal = st.session_state['SLM_REFERENCE_DATA'][sla][slm][st.session_state['OPTIMAL'][sla][slm]]
	    delta = round(value - optimal, 2)
	    #optimal_diff += delta
	    optimal_delta = pd.concat(
	    	[optimal_delta, pd.DataFrame([{'SLA': sla, 'SLM': slm, 'delta': delta}])], 
	    	ignore_index=True
	    )
	optimal_delta['delta'] = optimal_delta['delta'].round(2)

	return optimal_delta.sort_values('delta')


def slm_to_improve(sla, slm): 
	# Health 
	if slm == 'Subjective assessment of own health': 
		return "Exercise at least 1 more day more per week"
	elif slm == 'Frequency of sports': 
		return "Play sports or games more frequently"
	# Personal care
	if slm == 'Sleep': 
		return "Get 1 hour more of sleep per night"
	elif slm == 'Nutrition': 
		return "Eat healthier at least 1 more day per week"
	# Finances
	elif slm == 'Salary': 
		return "Increase net income by $1k"
	elif slm == 'Savings rate': 
		return "Increase savings rate by 10%"
	# Relationships
	elif slm == 'Significant other': 
		if st.session_state['portfolio'][sla][slm] == 'Stable Relationship': 
			return 'Take "next step" with signifant other'
		elif st.session_state['portfolio'][sla][slm] == 'Separated':
			return 'File for divorce'
		else:
			return 'Find a significant other'
	elif slm == 'Number of children':
		if st.session_state['portfolio'][sla][slm] == 0: 
			return "Have a child"
		else: 
			return "Have another child"
	elif slm == 'Number of close friends': 
		return "Add 1 close friend"
	# Community
	elif slm == 'Frequency of going to church': 
		return "Go to church more frequently"
	elif slm == 'Societal engagement': 
		return "Engage with your community more frequently"
	# Interests/ hobbies
	elif slm == 'Leisure': 
		return "Get 1 more hour per day of free time"


def slm_to_maintain(sla): 
	# Health 
	if sla == 'Health': 
		return "Maintain frequency of exercising and/ or playing sports"
	# Personal care
	if sla == 'Personal care': 
		return "Maintain personal care routines"
	# Finances
	if sla == 'Finances': 
		return "Maintain current financial habits"
	# Relationships
	if sla == 'Relationships': 
		return 'Maintain current set of relationships'
	# Community
	if sla == 'Community': 
		return "Maintain community engagement"
	# Interests/ hobbies
	if sla == 'Interests and entertainment': 
		return "Maintain leisure time"


def main():
	if not st.session_state['survey_submitted']: 
		st.markdown('Submit your <a style="color:red" href="Survey" target="_self">Survey</a> first!', unsafe_allow_html=True)
	else: 
		st.title("Strategize")

		df = build_rls_df()

		st.subheader("Diagnosis")

		slas_worst_df = df.groupby('SLA').delta.sum().reset_index().sort_values('delta').head(2)
		slas_worst = slas_worst_df.SLA.unique().tolist()
		slas_worst_str = ':red[**' + '**] and :red[**'.join(slas_worst) + '**]'

		st.markdown(
			f"""
			Two areas you're likely :red[**least**] satisfied with: {slas_worst_str}.  

			Relative life satisfaction you're missing out on: 
			"""
		)

		st.dataframe(
			slas_worst_df
			.rename(columns={'SLA': '', 'delta': 'relative life satisfaction'})
			.style.format(precision=2)
			.background_gradient(subset=['relative life satisfaction'], cmap='RdYlGn', vmin=df.delta.min(), vmax=0),
			hide_index=True
		)

		slas_best_df = df.groupby('SLA').delta.sum().reset_index().sort_values('delta', ascending=False).head(2)
		slas_best = slas_best_df.SLA.unique().tolist()
		slas_best_str = ':green[**' + '**] and :green[**'.join(slas_best) + '**]'

		st.markdown(
			f"""
			Two areas you're likely :green[**most**] satisfied with: {slas_best_str}.  

			Relative life satisfaction from optimal: 
			"""
		)

		st.dataframe(
			slas_best_df
			.rename(columns={'SLA': '', 'delta': 'relative life satisfaction'})
			.style.format(precision=2)
			.background_gradient(subset=['relative life satisfaction'], cmap='RdYlGn', vmin=df.delta.min(), vmax=0),
			hide_index=True
		)

		st.subheader("Guiding Policies")

		st.markdown(
			f"""
			- Focus on building satisfaction in {slas_worst_str}  
			- Maintain strength in {slas_best_str}
			"""
		)


		st.subheader("Specific Action Plan")
		
		slms_worst_df = df[df.SLA.isin(slas_worst) & (df.delta < 0)].sort_values('delta')
		slms_best_df = df[df.SLA.isin(slas_best) & (df.delta < 0)].sort_values('delta', ascending=False)

		specific_actions_str = ''
		for i in slms_worst_df.index: 
			specific_actions_str += f"  \n- {slm_to_improve(slms_worst_df.loc[i, 'SLA'], slms_worst_df.loc[i, 'SLM'])}"

		for i in slms_best_df.index: 
			maintain_str = slm_to_maintain(slms_best_df.loc[i, 'SLA'])
			if not maintain_str in specific_actions_str: 
				specific_actions_str += f"  \n- {maintain_str}"

		st.markdown(specific_actions_str)

		#print(list(product(slms_best_df.SLM.tolist(), slms_worst_df.SLM.tolist())))

		st.markdown(' ')
		st.markdown(' ')
		st.markdown(' ')
		st.markdown(
        """
          
        ##### If you found this useful, please consider <a style="color:red" href="https://www.buymeacoffee.com/tfarrell01j">supporting this project</a>! 
        """, unsafe_allow_html=True
      	)	

		st.markdown(' ')
		st.markdown(' ')
		st.divider()
		st.markdown(' ')
		_, c1, c2, _ = st.columns([1, 1, 1, 1])
		link = '<a style="color:grey" href="https://3dii87bqw3k.typeform.com/to/S5n2mSPK">Give Feedback</a>'
		c1.markdown(link, unsafe_allow_html=True)
		link = '<a style="color:grey" href="https://www.buymeacoffee.com/tfarrell01j">Support</a>'
		c2.markdown(link, unsafe_allow_html=True)

		



if __name__ == '__main__': 
	main()