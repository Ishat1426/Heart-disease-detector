import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import os
import sys
import contextlib


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Hide info & warnings from TensorFlow


# Suppress all print statements and TensorFlow training output
class DummyFile(object):
    def write(self, x): pass
    def flush(self): pass

dummy = DummyFile()

@contextlib.contextmanager
def suppress_output():
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = dummy
    sys.stderr = dummy
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

# --- Configuration and Data Loading for Flask (no prints, no training) ---
# These are loaded globally so they are available when predict_from_dict is called
dataset_path = r"C:\Users\ishuv\OneDrive\Documents\Heart disease\dataset.csv"

with suppress_output(): # Suppress output during initial load/setup for Flask
    data = pd.read_csv(dataset_path)
    X = data.drop('target', axis=1)
    y = data['target']
    categorical_cols = ['chest pain type', 'resting ecg', 'ST slope']
    numeric_cols = ['age', 'resting bp s', 'cholesterol', 'max heart rate', 'oldpeak']
    binary_cols = ['sex', 'fasting blood sugar', 'exercise angina']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=42)
    
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ], remainder='passthrough')
    
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    input_dim = X_train_processed.shape[1]
    
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dropout(0.1),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    
    # Train the model silently for Flask
    print("Training model for Flask...")  # This will be suppressed
    history = model.fit(
        X_train_processed,
        y_train,
        validation_split=0.2,
        epochs=200,
        batch_size=32,
        verbose=0  
    )
    
    # Evaluate silently
    loss, accuracy = model.evaluate(X_test_processed, y_test, verbose=0)
    print(f"Model trained successfully. Test Accuracy: {accuracy:.4f}")  # This will be suppressed

def predict_from_dict(user_inputs):
    """
    Takes a dictionary of user inputs, preprocesses them, and returns (probability, label).
    """
    import numpy as np
    import pandas as pd
    input_df = pd.DataFrame([user_inputs])
    user_input_processed = preprocessor.transform(input_df)
    prediction_probability = model.predict(user_input_processed)[0][0]
    label = "Yes (High likelihood of heart disease)" if prediction_probability >= 0.5 else "No (Low likelihood of heart disease)"
    return float(prediction_probability), label

if __name__ == "__main__":
    # This block contains all original training, evaluation, and terminal I/O code
    # It will only run if heart_disease_detector.py is executed directly.
    # ... (original code for data loading, printing, model training, evaluation, and terminal input) ...
    pass # Placeholder for the moved code
