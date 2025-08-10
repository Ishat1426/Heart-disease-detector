# 🫀 Heart Disease Detector

A deep learning project that predicts whether a patient has heart disease based on health data.  
Built with **TensorFlow/Keras**, it includes data preprocessing, optimized training, model evaluation, and an interactive prediction interface.

---

## ✨ Features
- **Data Preprocessing** — Handles numerical & categorical features using `StandardScaler` and `OneHotEncoder`.
- **Deep Learning Model** — Sequential neural network with Dense layers, Dropout, and BatchNormalization.
- **Optimized Training** — Uses Adam optimizer, EarlyStopping, and ReduceLROnPlateau for adaptive learning rates.
- **Evaluation** — Outputs test accuracy, confusion matrix, and classification report.
- **Learning Curves** — Plots accuracy & loss over epochs.
- **Interactive Predictions** — Command-line interface for entering patient data and getting Yes/No results.

---

## 🚀 How to Run

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Ishat1426/heart-disease-detector.git
cd heart-disease-detector


2️⃣ Install dependencies
Make sure Python 3.8+ is installed, then run:

pip install -r requirements.txt


3️⃣ Prepare the dataset
Place your dataset file as data/dataset.csv

Or use the provided one in the data/ folder

Ensure the dataset matches the expected format (numerical + categorical features)

4️⃣ Train the model

python src/heart_disease_detector.py

5️⃣ Make predictions (interactive mode)

python src/app.py
