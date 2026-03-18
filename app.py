import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Smart Expenditure Planner')
st.write('Upload your past expense data and enter your monthly income to get a personalised spending plan that guarantees at least 5% monthly savings.')

monthly_income = st.number_input(
    'Enter your monthly income (KSh)',
    min_value=0,
    value=50000
)

uploaded_file = st.file_uploader('Upload your transactions CSV', type='csv')

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error('The uploaded file is empty. Please upload a valid CSV.')
        else:
            df['Date'] = pd.to_datetime(df['Date'])
            num_months = df['Date'].dt.to_period('M').nunique()
            st.success('File uploaded successfully!')
            st.dataframe(df.head())

            st.divider()
            st.subheader('Your Spending Plan')

            monthly_avg = df.groupby('Category')['Amount'].sum() / num_months
            total_monthly_spending = monthly_avg.sum()
            savings_target = monthly_income * 0.05
            available_for_spending = monthly_income - savings_target

            st.write(f'Your average monthly expenses: **KSh {int(total_monthly_spending):,}**')
            st.write(f'Your minimum savings target (5%): **KSh {int(savings_target):,}**')
            st.write(f'Your available spending budget: **KSh {int(available_for_spending):,}**')

            st.divider()
            st.subheader('Recommended Monthly Budget per Category')

            if total_monthly_spending > available_for_spending:
                reduction_needed = total_monthly_spending - available_for_spending
                reduction_ratio = reduction_needed / total_monthly_spending
                recommended = monthly_avg * (1 - reduction_ratio)
                st.warning(f'Your spending exceeds your budget by KSh {int(reduction_needed):,}. We have adjusted your category budgets below.')
            else:
                recommended = monthly_avg.copy()
                st.success('Great news! Your current spending already allows for at least 5% savings. Here is your recommended monthly budget.')

            plan_df = pd.DataFrame({
                'Historical Average': monthly_avg.apply(lambda x: f'KSh {int(x):,}'),
                'Recommended Budget': recommended.apply(lambda x: f'KSh {int(x):,}')
            })
            st.dataframe(plan_df)

            st.divider()
            st.subheader('Your Personalised Savings Tips')

            for category in monthly_avg.index:
                historical = monthly_avg[category]
                recommended_amount = recommended[category]
                saving = historical - recommended_amount
                if saving > 0:
                    st.write(f'- Reduce **{category}** spending by **KSh {int(saving):,}** per month to stay on track.')
                else:
                    st.write(f'- **{category}** spending is within a healthy range. Maintain your current habits.')

            st.divider()
            st.subheader('Historical vs Recommended Budget')

            fig, ax = plt.subplots()
            x = range(len(monthly_avg.index))
            width = 0.35

            ax.bar([i - width/2 for i in x], monthly_avg.values, width, label='Historical Average')
            ax.bar([i + width/2 for i in x], recommended.values, width, label='Recommended Budget')
            ax.set_xticks(list(x))
            ax.set_xticklabels(monthly_avg.index, rotation=45)
            ax.set_ylabel('Amount (KSh)')
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)

    except Exception as e:
        st.error(f'Error reading file: {e}')




