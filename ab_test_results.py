import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

ab_test = pd.read_csv("ab_test_data.csv")

ab_df = pd.DataFrame(ab_test)
#print(ab_df.sample(5))
#print(ab_df.groupby(ab_df['test_group']).describe())

#p-value
alpha = 0.05
statistics, pvalue = stats.ttest_ind(
    ab_df[ab_df['test_group'] == 'a']['conversion'],
    ab_df[ab_df['test_group'] == 'b']['conversion'],
    alternative = 'less'
)

if pvalue < alpha:
    print(f'The null hypothesis is rejected: p-value is {round(pvalue, 17)}')
else:
    print(f'We cannot reject the null hypothesis: p-value is {round(pvalue, 17)}')

#users count
a_users = sum(ab_df['test_group'] == 'a')
b_users = sum(ab_df['test_group'] == 'b')
print(a_users, b_users)

#conversion
ab_group = ab_df.groupby(ab_df['test_group'])
conv_count = ab_group['conversion'].sum()
print(conv_count)

a_conv = conv_count['a'] / a_users
print(round(a_conv, 3) * 100)

b_conv = conv_count['b'] / b_users
print(round(b_conv, 3) * 100)

#ab test duration
ab_df['timestamp'] = pd.to_datetime(ab_df['timestamp'])
test_start = ab_df['timestamp'].min()
test_end = ab_df['timestamp'].max()
test_days = (test_end - test_start).days
print(f'''A/B test was started at {test_start};
A/B test was ended at {test_end};
A/B test was performed for {test_days} days.''' )

#plot
ci_level = (1-alpha) * 100
sns.barplot(x = ab_df['test_group'],
            y = ab_df['conversion'],
            errorbar = ('ci', ci_level),
            palette={'a': 'skyblue', 'b': 'pink'}
            )

plt.title('AB Test Results: Conversion Rate')
plt.xlabel('')  
plt.ylabel('Conversion Rate') 

plt.show()