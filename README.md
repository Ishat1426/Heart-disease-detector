This project aims to build and train a neural network model using TensorFlow/Keras for binary classification of heart disease. It includes data preprocessing steps, model training with callbacks for optimal performance, and an interactive command-line interface for new patient predictions.

Features
Data Preprocessing: Handles numerical and categorical features using StandardScaler and OneHotEncoder.

Deep Learning Model: A sequential neural network with multiple Dense layers, Dropout for regularization, and BatchNormalization for stable training.

Optimized Training: Utilizes Adam optimizer, EarlyStopping to prevent overfitting, and ReduceLROnPlateau for adaptive learning rate adjustments.

Model Evaluation: Provides test accuracy, confusion matrix, and classification report.

Learning Curves: Plots training and validation accuracy/loss over epochs.

Interactive Prediction: Allows users to input patient details and receive a "Yes" or "No" prediction for heart disease.