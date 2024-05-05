import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the saved model
model = load_model('question_generation_model.h5')

# Load preprocessed data
data = pd.read_csv(r"C:\Users\harsha anand\Desktop\Miniproject\flask\static\uploads\extracted_questions.csv")  # Assuming your data is in a CSV file

# Drop rows with missing values in the 'Question' column
data = data.dropna(subset=['Question'])

# Identify rows with missing values in the 'Difficulty' column
missing_indices = data[data['Difficulty'].isnull()].index

# Separate features (X) and target variable (Y)
X = data['Question']

# Tokenize the text data using the same tokenizer used during training
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)

# Convert text data to sequences
X_seq = tokenizer.texts_to_sequences(X)

# Pad sequences
max_length = 100  # Should be the same as used during training
X_pad = pad_sequences(X_seq, maxlen=max_length, padding='post')

# Make predictions for missing values
predictions = model.predict(X_pad[missing_indices])

# Fill in missing values with predicted labels
predicted_labels = [np.argmax(pred) + 1 for pred in predictions]  # Add 1 to convert indices to 1-based numbering

# Fill in missing values with predicted labels
data.loc[missing_indices, 'Difficulty'] = predicted_labels

# Save the updated DataFrame to a new CSV file
data.to_csv('new_data.csv', index=False)
