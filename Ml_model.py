# Importing Libraries
import pandas as pd  # Dataframe Manipulation  
import numpy as np  # Array/lists Handlings
import matplotlib.pyplot as plt  # Data Visualization
import seaborn as sns  # For data visualization
from pandas.api.types import is_numeric_dtype
import joblib 
from sklearn.preprocessing import LabelEncoder

# Importing Dataset
df = pd.read_csv("cleaned_data.csv")

# Initializing encoder
encoder = LabelEncoder()
# Dataset splitting
X = df.iloc[:, :-1].values  # Features (independent variables)
y = df.iloc[:, -1].values   # Target (dependent variable)

# Splitting into training and testing dataset
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=21)

# Training the RandomForestClassifier model
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Making predictions
y_pred = clf.predict(X_test)

# Comparing the predicted values with actual values
comparison = np.concatenate((y_test.reshape(len(y_test), 1), y_pred.reshape(len(y_pred), 1)), 1)
for i in range(20):
    print(comparison[i])

# Classification Metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

# Calculating metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')  # Use 'weighted' for multi-class
recall = recall_score(y_test, y_pred, average='weighted')        # Use 'weighted' for multi-class
f1 = f1_score(y_test, y_pred, average='weighted')               # Use 'weighted' for multi-class
conf_matrix = confusion_matrix(y_test, y_pred)

# ROC-AUC Score (only for binary classification)
if len(np.unique(y)) == 2:  # Check if it's a binary classification problem
    roc_auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
else:
    roc_auc = None  # ROC-AUC is not applicable for multi-class without adjustments

# Displaying evaluated metrics
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")
print("Confusion Matrix:")
print(conf_matrix)

if roc_auc is not None:
    print(f"ROC-AUC Score: {roc_auc:.2f}")

# Saving the trained model
joblib.dump(clf, 'water_quality_model.pkl')

# Saving the label encoder as well (for encoding the categorical data when making predictions)
joblib.dump(encoder, 'label_encoder.pkl')