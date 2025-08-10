from flask import Flask, render_template_string, request
import heart_disease_detector

app = Flask(__name__)

# Use Bootstrap 5 dark mode and custom dark theme for a premium look
template = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Heart Disease Predictor</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
  <style>
    body {
      background: linear-gradient(135deg, #181c24 0%, #232a34 100%);
      color: #f8fafc;
      min-height: 100vh;
    }
    .card {
      background: rgba(30, 34, 45, 0.98);
      border-radius: 1.2rem;
      box-shadow: 0 8px 32px 0 rgba(0,0,0,0.25);
      border: 1px solid #232a34;
    }
    .form-label {
      font-weight: 500;
      color: #e0e6ed;
    }
    .form-control {
      background: #232a34;
      color: #f8fafc;
      border: 1px solid #353b48;
      border-radius: 0.5rem;
    }
    .form-control:focus {
      background: #232a34;
      color: #fff;
      border-color: #4f8cff;
      box-shadow: 0 0 0 0.2rem rgba(79,140,255,0.15);
    }
    .predict-btn {
      width: 100%;
      background: linear-gradient(90deg, #4f8cff 0%, #3358ff 100%);
      border: none;
      font-weight: 600;
      letter-spacing: 1px;
      box-shadow: 0 2px 8px 0 rgba(79,140,255,0.15);
    }
    .predict-btn:hover {
      background: linear-gradient(90deg, #3358ff 0%, #4f8cff 100%);
    }
    .premium-result {
      animation-duration: 1s;
      animation-fill-mode: both;
      margin-bottom: 2rem;
      background: linear-gradient(90deg, #232a34 60%, #2d3542 100%);
      border: 2px solid #00ffd0;
      color: #fff;
      font-size: 1.5rem;
      font-weight: 700;
      box-shadow: 0 0 24px #00ffd0aa;
      border-radius: 1rem;
      letter-spacing: 1px;
    }
    .result {
      font-size: 1.2rem;
      font-weight: bold;
      color: #fff;
      background: linear-gradient(90deg, #232a34 0%, #2d3542 100%);
      border-radius: 0.7rem;
      border: 1px solid #353b48;
    }
    .container-fluid {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0;
    }
    .card {
      width: 100%;
      max-width: 900px;
      margin: 0 auto;
    }
    h2 {
      color: #4f8cff;
      font-weight: 700;
      letter-spacing: 1px;
    }
    ::placeholder {
      color: #b0b8c1 !important;
      opacity: 1;
    }
  </style>
</head>
<body>
  <div class="container-fluid px-0">
    <div class="w-100" style="max-width: 900px;">
      {% if prediction is not none %}
        <div class="alert alert-dark premium-result shadow-lg mb-4 text-center animate__animated animate__fadeInDown" role="alert">
          <span>Prediction: {{ prediction }}</span><br>
          {% if probability is not none %}
            <span style="font-size: 1.1rem; color: #00ffd0;">Probability: {{ probability }}</span>
          {% endif %}
        </div>
      {% endif %}
      <div class="card p-4 mx-auto">
        <h2 class="mb-4 text-center">Heart Disease Prediction</h2>
        <form method="post">
          {% for field, label, type in fields %}
            <div class="mb-3">
              <label class="form-label">{{ label }}</label>
              <input type="text" class="form-control" name="{{ field }}" required placeholder="Enter {{ label.lower() }}">
            </div>
          {% endfor %}
          <button type="submit" class="btn predict-btn">Predict</button>
        </form>
      </div>
    </div>
  </div>
</body>
</html>
'''

# Updated input fields and labels to match heart_disease_detector.py
input_fields = [
    ("age", "Age", float),
    ("sex", "Sex (1 for male, 0 for female)", int),
    ("chest pain type", "Chest Pain Type (1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic)", int),
    ("resting bp s", "Resting Blood Pressure (mm/Hg)", float),
    ("cholesterol", "Cholesterol (mg/dl)", float),
    ("fasting blood sugar", "Fasting Blood Sugar > 120 mg/dl (1 for True, 0 for False)", int),
    ("resting ecg", "Resting ECG (0: normal, 1: ST-T wave abnormality, 2: left ventricular hypertrophy)", int),
    ("max heart rate", "Maximum Heart Rate Achieved", float),
    ("exercise angina", "Exercise Induced Angina (1 = yes, 0 = no)", int),
    ("oldpeak", "OldPeak", float),
    ("ST slope", "ST slope (1: upsloping, 2: flat, 3: downsloping)", int),
]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    probability = None
    if request.method == 'POST':
        user_inputs = {}
        for field, label, typ in input_fields:
            value = request.form.get(field)
            try:
                user_inputs[field] = typ(value)
            except Exception:
                user_inputs[field] = value
        try:
            prob, pred = heart_disease_detector.predict_from_dict(user_inputs)
            prediction = pred
            probability = f"{prob:.2%}"
        except Exception as e:
            prediction = f"Error: {e}"
            probability = "-"
    return render_template_string(template, fields=input_fields, prediction=prediction, probability=probability)

if __name__ == '__main__':
    app.run(debug=True) 