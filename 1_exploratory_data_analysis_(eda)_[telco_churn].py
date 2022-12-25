# -*- coding: utf-8 -*-
"""1. Exploratory Data Analysis (EDA) [TELCO CHURN]

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yUOZH1JOlJ4ytt3quvY8cMnaBHMQc1_v

## Steps involved in EDA

1. **Data Sourcing** <br>
    1.1. Public Data <br>
    1.2. Private Data <br>
2. **Data Cleaning** <br>
    2.1. Handle Missing Values <br>
    2.2. Standardization of Data <br>
    2.3. Outlier Treatment <br>
    2.4. Indentify important features <br>
3. **Univarient Analysis with Visualization** <br>
    3.1. Frequency <br>
    3.2. Central tendecy <br>
    3.3. Dispersion <br>
4. **Bivarient Analysis with Visualization** <br>
    4.1. Correlation <br>
    4.2. Covarience <br>
5. **Derived Matrtics ( Feature Engineering )** <br>
    5.1. Feature Encoding

## Telco Churn Analysis

### Import Necessary Libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

"""### Load Data"""

telco_base_data = pd.read_csv("/content/WA_Fn-UseC_-Telco-Customer-Churn.csv")

"""### Check DataFrame"""

telco_base_data.head()

"""### DataFrame Information"""

telco_base_data.info()

"""### Observation
* **We have 21 Columns, means 20 Features and one Target Column.** <br>
* **We have 7043 Observations, No missing Values in Columns / Features.** <br>
* **Most of them are categorical Columns. Only *SeniorCitizen*,*tenure* and *MonthlyCharges* are Numerical Columns.**

### Data Cleaning

#### Missing Data
"""

telco_base_data.isnull().sum()

"""##### 1. Make a Copy of our Base DataFrame"""

telco_data = telco_base_data.copy()

"""##### 2. Total Charges should be Numeric Amount. We need to convert this column to **Numeric Data Type**"""

telco_data['TotalCharges'] = pd.to_numeric(telco_data['TotalCharges'], errors='coerce')

"""##### 3. As we can see there are 11 missing values in TotalCharges column. Let's check the percentage of Missing values"""

telco_data.isnull().sum()

features_with_na = [features for features in telco_data.columns if telco_data[features].isnull().sum()>0]

print(features_with_na)

for feature in features_with_na:
    print(feature, np.round(telco_data[feature].isnull().mean(), 4),  ' % missing values')

missing = pd.DataFrame((telco_data.isnull().sum())*100/telco_data.shape[0]).reset_index()
plt.figure(figsize=(16,5))
ax = sns.pointplot('index',0,data=missing)
plt.xticks(rotation =90,fontsize =7)
plt.title("Percentage of Missing values")
plt.ylabel("PERCENTAGE")
plt.show()

"""##### 4. Missing Value Treatment 
Since the % of these records compared to total dataset is very low ie 0.16%, it is safe to ignore them from further processing.
"""

telco_data.dropna(inplace=True) # make the Change Permanent with inplace = True

"""### Numerical Features"""

telco_data.columns

numerical_features_DF = telco_data[['SeniorCitizen','tenure','MonthlyCharges', 'TotalCharges']] ## New DataFrame

numerical_features_DF.head()

"""To Find all Numerical Features in a DataFrame you can use following code:"""

numerical_features = [feature for feature in telco_data.columns if telco_data[feature].dtypes != 'O']
print(numerical_features)

telco_data[numerical_features].head()

telco_data['SeniorCitizen'].value_counts()

sns.pairplot(telco_data,hue='Churn')

print(telco_data['tenure'].unique())

"""Group the Customer Tenure in year-wise"""

label = ["{}-{}".format(i,i+11) for i in range(1,72,12) ]
print(label)

telco_data['tenure_group'] = pd.cut(telco_data['tenure'],range(1,80,12),labels=label,right=False)

telco_data.head()

telco_data['tenure_group'].value_counts()

sns.countplot(x='tenure_group',hue='Churn',data=telco_data)

"""**Remove Columns which is not required**"""

telco_data.drop(labels=['customerID','tenure'], axis=1,inplace=True)

telco_data.head()

"""### Univarient Analysis"""

telco_data.columns

"""**Univarient Analysis for Categorical Data**"""

for col in telco_data.drop(columns=['MonthlyCharges','TotalCharges', 'Churn']):
  plt.figure(col,figsize=(9,5))
  ax = sns.countplot(x=col,data=telco_data,hue='Churn')
  for p in ax.patches: 
        ax.annotate(f'\n{p.get_height()}', (p.get_x()+0.2, p.get_height()), ha='center', va='top', color='white', size=8)

"""**Univarient Analysis for Numerical Data**"""

sns.displot(data=telco_data,x='MonthlyCharges',hue='Churn')

sns.displot(data=telco_data,x='TotalCharges')

telco_data['TotalCharges'].skew()

np.log(telco_data['TotalCharges']).skew()

telco_data['MonthlyCharges'].skew()

np.log(telco_data['MonthlyCharges']).skew()

plt.figure(figsize=(9,5))
sns.kdeplot(telco_data[telco_data['Churn'] == 'No']['MonthlyCharges'],color='Green')
sns.kdeplot(telco_data[telco_data['Churn'] == 'Yes']['MonthlyCharges'],color='Red',shade=True)

"""**Insight:** Churn is high when Monthly Charges are high"""

plt.figure(figsize=(9,5))
sns.kdeplot(telco_data[telco_data['Churn'] == 'No']['TotalCharges'],color='Green')
sns.kdeplot(telco_data[telco_data['Churn'] == 'Yes']['TotalCharges'],color='Red',shade=True)

"""**Surprising insight** as higher Churn at lower Total Charges

However if we combine the insights of 3 parameters i.e. Tenure, Monthly Charges & Total Charges then the picture is bit clear :- Higher Monthly Charge at lower tenure results into lower Total Charge. Hence, all these 3 factors viz **Higher Monthly Charge**,  **Lower tenure** and **Lower Total Charge** are linkd to **High Churn**.

**Bivarient Analysis for Numerical Data**
"""

sns.jointplot(x='MonthlyCharges',y='TotalCharges',data=telco_data)

"""**Bivarient Analysis for Categorical Data**"""

sns.barplot(x='tenure_group',y='MonthlyCharges',data =telco_data, hue='Churn' )

plt.figure(figsize=(20,8))
sns.boxplot(x='tenure_group',y='MonthlyCharges',data =telco_data, hue='Churn' )

"""**Find the Correlation between all features with Target**"""

telco_data.corr() # -1 to +1

"""**Issue:** correlation can be drawn only for numerical features."""

telco_data.head()

len(telco_data.columns)

"""#### Let's make all Categorical Features to Numerical Features
There are two ways we can do that:


*   Label Encoding : Suitable when there are two categories in Features
*   One Hot Encoding/Converting to Dummy Variable : Suitable where are more than two categories.

**Convert the target variable 'Churn' in a binary numeric variable i.e. Yes=1 ; No = 0**
"""

def convert_to_numerical(label):
  if label =='Yes':
    return 1
  else:
    return 0

telco_data['Churn'].apply(convert_to_numerical)

telco_data['Churn'].apply(lambda label: 1 if label=='Yes' else 0)

telco_data['Churn'] = telco_data['Churn'].apply(lambda label: 1 if label=='Yes' else 0)

telco_data.head()

"""**Convert all Categorical Data into Dummy Data** """

telco_data_dummies = pd.get_dummies(telco_data)

telco_data_dummies.head()

telco_data_dummies.corr( )['Churn'].sort_values(ascending= False)

plt.figure(figsize=(20,8))
telco_data_dummies.corr()['Churn'].sort_values(ascending= False).plot(kind='bar')

plt.figure(figsize=(20,20))
sns.heatmap(telco_data_dummies.corr(),cmap='RdYlGn',linecolor='Black',linewidths=1)

"""#### Feature Selection
* Filter Method
* Wrapper Method
"""

telco_data_dummies

features = telco_data_dummies.drop('Churn',axis=1)

target = telco_data_dummies['Churn']

"""**Filter Method**

* **The Chi-square** test is used for categorical features in a dataset. 
* We calculate Chi-square between each feature and the target and select the desired number of features with the best Chi-square scores. 
* The following conditions have to be met: the variables have to be categorical, sampled independently and values should have an expected frequency greater than 5.
"""

from sklearn.feature_selection import SelectKBest # Class
from sklearn.feature_selection import chi2 # Method

bestFeatures = SelectKBest(score_func=chi2,k=12) # instantiate
fit = bestFeatures.fit(features,target)
dfScore = pd.DataFrame(fit.scores_)
dfColumns = pd.DataFrame(features.columns)
featuresScore = pd.concat([dfColumns,dfScore], axis =1)
featuresScore.columns = ['Features','Chi-Squred Score']
featuresScore.sort_values(by='Chi-Squred Score',ascending=False).head(5)

fit = bestFeatures.fit(features,target)

dfScore = pd.DataFrame(fit.scores_)
dfScore.head()

dfColumns = pd.DataFrame(features.columns)
dfColumns.head()

featuresScore = pd.concat([dfColumns,dfScore], axis =1)

featuresScore.head()

featuresScore.columns = ['Features','Chi-Squred Score']

featuresScore.head()

featuresScore.sort_values(by='Chi-Squred Score',ascending=False).head(12)

"""**Wrapper Method**

**Option 1**
"""

from sklearn.ensemble import  ExtraTreesClassifier

model = ExtraTreesClassifier()

model.fit(features,target)

print(model.feature_importances_)

dfImportance = pd.DataFrame(model.feature_importances_)
dfImportance.head()

dfColumns = pd.DataFrame(features.columns)
dfColumns.head()

featuresImportance = pd.concat([dfColumns,dfImportance], axis =1)
featuresImportance.head()

featuresImportance.columns = ['Features','Importance Score']

featuresImportance.sort_values(by='Importance Score',ascending=False).head(12)

"""**Option 2**"""

from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel

feature_sel_model = SelectFromModel( Lasso(alpha=0.005) )

feature_sel_model.fit(features,target)

feature_sel_model.get_support()

selected_feat = features.columns[feature_sel_model.get_support()]

selected_feat

len(selected_feat)

"""#### Outlier Treatment"""

features['MonthlyCharges'].describe()

features['TotalCharges'].describe()

sns.boxplot(features['TotalCharges'])

"""**Option 1**"""

Q1 =  features['TotalCharges'].quantile(0.25)
Q3 =  features['TotalCharges'].quantile(0.75)
IQR = Q3 - Q1
upper_fence = Q3 + 0.5 * IQR
lower_fence = Q1 - 0.5 * IQR

print ("IQR: {} Upper Fence {} Lower Fence {}".format(IQR,upper_fence,lower_fence))

features[(features['TotalCharges'] > lower_fence) & (features['TotalCharges'] <upper_fence)]

temp_df = features[(features['TotalCharges'] > lower_fence) & (features['TotalCharges'] <upper_fence)]

np.log(temp_df['TotalCharges']).skew()

sns.displot((temp_df['TotalCharges']))

sns.displot(np.log(temp_df['TotalCharges']))

lower_fence =  features['TotalCharges'].quantile(0.15)
upper_fence =  features['TotalCharges'].quantile(0.85)

features['TotalCharges'].clip(lower_fence,upper_fence,axis=0)

"""#### Data Scaling """

features.head()

from sklearn.preprocessing import StandardScaler

feature_scaled = StandardScaler().fit_transform(features)

feature_scaled_df = pd.DataFrame(feature_scaled, columns=features.columns)
feature_scaled_df

target_df = pd.DataFrame(target)
target_df

final_scaled_dataset = pd.concat([feature_scaled_df,target_df],axis=1)

final_scaled_dataset.head()

final_scaled_dataset.to_csv('Scaled_Churn_data.csv',index=False) # Optional

"""# Summary

* **Data Cleaning**: Convert Data Type, Missing Values
* **Analysis** : Univarient & Bi-Varient, Numerical & Categorical 
* **Data Normalization** : for Skewed Data
* **Outlier Treatment** : Clipping Method
* **Feature Selection & Colinearity** : Correlation, Filter,Wrapper
* **Data Scaling** : Standard Scaler

# Model Building

## Load Data
"""

churn_data = pd.read_csv('/content/Scaled_Churn_data.csv')

churn_data.head()

churn_data.isnull().sum()

churn_data.dropna(inplace=True)

churn_data.isnull().sum()

"""**Divide Data into Features (X) and Target (y)**"""

X = churn_data.drop('Churn',axis=1)

y = churn_data['Churn']

"""**Split Training And Test Data**"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=0, test_size=0.20)

X_train.shape

X_test.shape

"""**Select Appropriate Algorithm**"""

from sklearn.tree import DecisionTreeClassifier

model_dt = DecisionTreeClassifier()

"""**Train Model with Algorithm + Train Data**"""

model_dt.fit(X_train,y_train)

"""**Test  Model with Test Dataset**"""

y_pred = model_dt.predict(X_test)
y_pred

from sklearn.metrics import confusion_matrix

y_test.shape

conf_Matrix = confusion_matrix(y_test, y_pred)
print(conf_Matrix)

from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred , labels=[0,1]))

"""**Because wehave imbalanced data, so need to do upSmapling our Data**
* Method: SMOTE-ENN
"""

from imblearn.combine import SMOTEENN

sm = SMOTEENN()

X_resample,y_resample = sm.fit_sample(X,y)

X.shape

X_resample.shape

X_train, X_test, y_train, y_test = train_test_split(X_resample, y_resample,random_state=0, test_size=0.20)
model_dt = DecisionTreeClassifier()
model_dt.fit(X_train,y_train)
y_pred = model_dt.predict(X_test)
print(classification_report(y_test, y_pred , labels=[0,1]))

"""**Random Forest Classifier**"""

from sklearn.ensemble import RandomForestClassifier

model_rf = RandomForestClassifier()
model_rf.fit(X_train,y_train)
y_pred = model_rf.predict(X_test)
print(classification_report(y_test, y_pred , labels=[0,1]))

"""**Save Best model**"""

import pickle

pickle.dump(model_rf,open("Model_RF.sav",'wb')) # Write-Binary

"""**Read Model**"""

load_model = pickle.load(open('Model_RF.sav','rb')) # Read-Binary

y_pred = load_model.predict(X_test)
print(classification_report(y_test, y_pred , labels=[0,1]))