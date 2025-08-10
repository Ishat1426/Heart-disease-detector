import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("dataset.csv")  # make sure your dataset path is correct

# Split features & labels
X = df.drop("target", axis=1)
y = df["target"]

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build improved model
model = Sequential([
    Dense(64, activation='relu', kernel_regularizer=l2(0.001), input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(32, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Early stopping to avoid overfitting
early_stop = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)

# Train model
history = model.fit(X_train, y_train, validation_split=0.2, epochs=200, batch_size=16, callbacks=[early_stop], verbose=0)

# Evaluate
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"✅ Improved Model Test Accuracy: {acc:.4f}")

# Optional: Predictions
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print("Prediction sample:", y_pred[:10].ravel())

def predict_from_dict(user_inputs):
    """
    Takes a dictionary of user inputs, preprocesses them, and returns (probability, label).
    """
    import numpy as np
    import pandas as pd
    input_df = pd.DataFrame([user_inputs])
    user_input_scaled = scaler.transform(input_df)
    prediction_probability = model.predict(user_input_scaled, verbose=0)[0][0]
    label = "Yes (High likelihood of heart disease)" if prediction_probability >= 0.5 else "No (Low likelihood of heart disease)"
    return float(prediction_probability), label

# Only run training if this file is executed directly
if __name__ == "__main__":
    # Training code is already executed above, so just print final results
    print(f"Final Model Accuracy: {acc:.4f}")
    print("Model is ready for predictions!")
