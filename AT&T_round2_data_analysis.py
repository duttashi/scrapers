import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from scipy.stats import ttest_1samp

# load data
df = pd.read_csv("../data/LoanStats3a.csv", skiprows=1, low_memory=False)
print("\ndata shape: ", df.shape) # (42538, 144)
# relabel factor levels of loan_status col
df['loan_status']=df['loan_status'].replace({'Does not meet the credit policy. Status:Fully Paid':'Fully Paid',
                           'Does not meet the credit policy. Status:Charged Off':'Charged Off'}
                          )
print(df['loan_status'].value_counts())

# Initial plots
df.dtypes.value_counts().sort_values().plot(kind='barh')
plt.title('Number of columns distributed by Data Types',fontsize=15)
plt.xlabel('Number of columns',fontsize=12)
plt.ylabel('Data type',fontsize=12)
plt.show()

fig = plt.figure(figsize=(22,6))
sns.kdeplot(df.loc[df['loan_status'] == 'Fully Paid', 'loan_amnt'], label = 'Fully Paid')
sns.kdeplot(df.loc[df['loan_status'] == 'Charged Off', 'loan_amnt'], label = 'Charged Off');
plt.xlabel('Loan Amount',fontsize=15)
plt.ylabel('Density',fontsize=15)
plt.title('Distribution of Loan Amount',fontsize=20)
plt.show()

fig = plt.figure(figsize=(22,6))
df[df['loan_status']=='Fully Paid'].groupby('addr_state')['loan_status'].count().sort_values().plot(kind='barh')
plt.ylabel('State',fontsize=15)
plt.xlabel('Number of loans',fontsize=15)
plt.title('Number of defaulted loans per state',fontsize=20)
plt.show()

fig, ax = plt.subplots(1, 3, figsize=(16,5))
loan_amount = df["loan_amnt"].values
funded_amount = df["funded_amnt"].values
investor_funds = df["funded_amnt_inv"].values
sns.histplot(loan_amount, ax=ax[0], color="#F7522F")
ax[0].set_title("Loan Applied by the Borrower", fontsize=14)
sns.histplot(funded_amount, ax=ax[1], color="#2F8FF7")
ax[1].set_title("Amount Funded by the Lender", fontsize=14)
sns.histplot(investor_funds, ax=ax[2], color="#2EAD46")
ax[2].set_title("Total committed by Investors", fontsize=14)
plt.show()

def missing_data_stats(df):
        mis_val = df.isnull().sum()
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        print ("The dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns with missing values.")
        return mis_val_table_ren_columns
# Missing values statistics
missing_data_stats(df)

# missing data treatment
df1 = df[df.columns[df.isnull().mean()<=0.80]]
print("df1 shape: ",df1.shape) # (42542, 54)

cols = df1.columns.values
df1[cols]=df1[cols].fillna(df1.mode().iloc[0])
missing_data_stats(df1)

# Feature engineering
# Answer to question 4a
temp_list = [1 if i=='Fully Paid' else 0 for i in df1['loan_status']]
df1['target'] = temp_list
df1['target'] = df1['target'].astype(str)
print(df1['target'].value_counts()) # 1= Fully Paid 36104, 0= Charged Off 6438
df1 = df1.drop('loan_status',axis=1)
print("df1 shape: ",df1.shape) # (42542, 54)

# CORRELATION Check and TREATMENT
cor = df1.corr(numeric_only = True)
cor.loc[:,:] = np.tril(cor, k=-1) # below main lower triangle of an array
cor = cor.stack()
print(cor[(cor > 0.80) | (cor < -0.80)])
# remove highly correlated vars
# Create correlation matrix
corr_matrix = df1.corr(numeric_only = True).abs()
# Select upper triangle of correlation matrix
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
# Find features with correlation greater than 0.80
to_drop = [column for column in upper.columns if any(upper[column] > 0.80)]
print("high correlated features:\n", to_drop)
# # Drop features
df1.drop(to_drop, axis=1, inplace=True)
print("new df1 shape after removing high corr: ", df1.shape)
df1.int_rate = pd.Series(df1.int_rate).str.replace('%', '').astype(float)
missing_data_stats(df1)

# Answer to Q2
print("\n #### Average annual income by state ####")
print(df.groupby('addr_state', as_index=False)['annual_inc'].mean())
print("\n #### Number of loan applicants by state ####")
print(df.groupby('addr_state', as_index=False)['application_type'].count().reset_index().sort_values(by='application_type', ascending=False))

# Answer to Q3(a)
df_t = df[(df1['annual_inc']>0) & (df1['addr_state']=='WV')] # WV = West Virginia
t = df[(df1['annual_inc']>0) & (df1['addr_state']=='NM')] # NM = New Mexico
df_f = pd.concat([df_t, t])
sns.catplot(data=df_f, x='addr_state',y='annual_inc')
plt.show()

# Answer to Q3(b)
annual_inc_mean = np.mean(df_f['annual_inc'])
tset, pval = ttest_1samp(df_f['annual_inc'], annual_inc_mean)
print("p-values: ",pval)
if (pval < 0.05):    # p-value is 0.05 or 5%
   print(" we are rejecting null hypothesis")
else:
  print("we are accepting null hypothesis")
# delete temp vars
a = [df_t, t]
del(a)

# Answer to Q 4(a) Label encoding for building machine learning model
df2 = df1.copy()
print("df2 shape: ", df2.shape) # (42542, 45)

# Take a random sample of data because most categorical vars have high number of levels
df2_smpl = df2.sample(frac=0.05)
# checking if sample is 0.25 times data or not
print("data sampled: ", df2_smpl.shape)
print("sample data columns\n", df2_smpl.columns)

count = 0
le = preprocessing.LabelEncoder()
for col in df2_smpl:
    if df2_smpl[col].dtype == 'object':
        # If 2 or fewer unique categories
        if len(list(df2_smpl[col].unique())) <=2:
            df2_smpl[col] = le.fit_transform(df2_smpl[col])
            print (col)
            count += 1
print('%d columns were label encoded.' % count)

df3 = pd.get_dummies(df2_smpl)
print("\nLabel encoded data and shape: ", df3.shape)
df3.to_csv("../data/loandata_clean_encoded.csv", index=False)

# Answer to Q 4(b) Machine Learning (ML)
y = df3['target']
x_train,x_test,y_train,y_test = train_test_split(df3,y,test_size = 0.20 ,random_state = 24, stratify =y)
# ML model on imbalanced predictor variable
lr = LogisticRegression(solver='liblinear', max_iter=100)
lr.fit(x_train, y_train)
predictions = lr.predict(x_test)
print("\n######### Imbalanced data classification #########")
print(classification_report(y_test, predictions))

# Predictor variable balancing
sm = SMOTE(random_state = 24)
y = df3.loc[:, df3.columns == 'target']
x_train,x_test,y_train,y_test = train_test_split(df3,y,test_size = 0.20 ,random_state = 24, stratify =y)
X_res, y_res = sm.fit_resample(x_train, y_train)
print("Resampled data shape: ", X_res.shape)
print("Balanced target\n", X_res['target'].value_counts())
lr1 = LogisticRegression(solver='liblinear', max_iter=100)
# ML model on balanced predictor variable
lr1.fit(X_res, y_res.values.ravel())
predictions1 = lr1.predict(x_test)
print("\n######### Balanced data using SMOTE #########")
print(classification_report(y_test, predictions1))
df4 = x_test.copy()
df4['preds'] = predictions1
df4.to_csv("../data/LoanDefault_Preds.csv")
