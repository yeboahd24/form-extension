# Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Load the diabetes.csv dataset
df = pd.read_csv('/home/backend/Map/crimemap/maps/diabetes.csv')

# Split the dataset into predictor and target variables
x = df.drop(['Outcome'],axis=1)
y = df.Outcome

# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize a logistic regression estimator
lr = LogisticRegression()

# Fit the estimator to the training data
lr.fit(x_train, y_train)

# Evaluate performance using the test data
accuracy = lr.score(x_test, y_test)
print('Accuracy:', accuracy)

# Save the trained model in a pkl file
filename = 'diabetes.pkl'
pickle.dump(lr, open(filename, 'wb'))
