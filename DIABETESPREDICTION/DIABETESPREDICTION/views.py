from django.shortcuts import render
from django.http import HttpResponse
import joblib

def index(request):
    # Load the trained model
    file_path = 'C:/Users/Administrator/Desktop/Train_test/DIABETES/diabetes_model.pkl'
    try:
        trained_model = joblib.load(file_path)
        print("Model loaded successfully!")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return HttpResponse("Error: Model file not found.", status=500)
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return HttpResponse("Error: Failed to load model.", status=500)

    if request.method == 'POST':
        # Get the form data
        Pregnancies = float(request.POST.get('Pregnancies'))
        Glucose = float(request.POST.get('Glucose'))
        BloodPressure = float(request.POST.get('BloodPressure')) 
        SkinThickness = float(request.POST.get('SkinThickness'))
        Insulin = float(request.POST.get('Insulin'))
        BMI = float(request.POST.get('BMI'))
        DiabetesPedigreeFunction = float(request.POST.get('DiabetesPedigreeFunction'))
        Age = int(request.POST.get('Age'))

        # Make prediction
        input_data = [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
        try:
            prediction = trained_model.predict(input_data)
            if prediction[0] == 1:
                result_message = 'You have Diabetes.'
            else:
                result_message = 'You do not have Diabetes.'
        except Exception as e:
            print(f"An error occurred while making prediction: {e}")
            return HttpResponse("Error: Failed to make prediction.", status=500)

        # Pass the result message to the template
        return render(request, 'home.html', {'result_message': result_message})
    
    return render(request, 'home.html', {'result_message': None})
