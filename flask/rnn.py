import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load preprocessed data and labels
data = pd.read_csv(r"C:\Users\harsha anand\Desktop\Miniproject\flask\static\uploads\extracted_questions.csv")
data = data.dropna()

# Separate features (X) and target variable (Y)
X = data['Question']  # Assuming 'Question' is the column name for input text
Y = data['Difficulty']  # Assuming 'Difficulty' is the column name for target variable

# Splitting data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.2, random_state=42)

# Tokenize the text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

# Convert text data to sequences
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_val_seq = tokenizer.texts_to_sequences(X_val)

# Pad sequences
max_length = 100  # Example value, adjust based on your maximum sequence length
X_train_pad = pad_sequences(X_train_seq, maxlen=max_length, padding='post')
X_val_pad = pad_sequences(X_val_seq, maxlen=max_length, padding='post')

# Define model parameters
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 100  # Example value, adjust based on your embedding dimension
num_classes = 3  # Since your numerical encoding is already 1 for easy, 2 for medium, and 3 for hard

# Define the RNN model
model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length))
model.add(LSTM(units=64, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(X_train_pad, y_train, epochs=10, batch_size=32, validation_data=(X_val_pad, y_val))

# Save the trained model
model.save(r"c:\Users\harsha anand\Desktop\Miniproject\flask\static\uploads\question_generation_model.h5")
