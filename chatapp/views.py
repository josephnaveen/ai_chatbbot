from django.shortcuts import render, redirect
from .models import Student
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
# Load the JSON file
from django.http import JsonResponse

with open('chatapp\college_qp.json', 'r') as file:
    college_qp = json.load(file)

questions = college_qp['questions']
responses = college_qp['answers']


def home(request):
    return render(request, 'chatbot/home.html')

def register_new_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')
        # Similarly, get other fields as needed

        # Create a new student instance and save it to the database
        student = Student(name=name, email=email, password=password, mobile=mobile, location=location)
        student.save()

        return redirect('chatbot')
    return render(request, 'chatbot/register.html')


def login_existing_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Student.objects.filter(name=username, password=password).exists():
            return redirect('chatbot')
    return render(request, 'chatbot/login.html')

# def chatbot(request):
#     messages = request.session.get('messages', [])
    
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         question, response = process_message(message)
#         messages.append((question, "response"))
#         request.session['messages'] = messages
#         return render(request, 'chatbot/chatbot.html', {'response': response, 'messages': messages})
    
#     return render(request, 'chatbot/chatbot.html', {'response': None, 'messages': messages})

def chatbot(request):
    if request.method=='POST':
        message=request.POST.get('message')
        response=process_message(message)
        return JsonResponse({
            # 'message':message,
            'response':response

        })

    return render(request,'chatbot/chatbot.html')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'chatbot/student_list.html', {'students': students})



# Sample dataset of questions and responses


# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

def process_message(user_query):
    # Vectorize the user query
    user_query_vectorized = vectorizer.transform([user_query])

    # Calculate the cosine similarity between the user query and the questions
    similarities = cosine_similarity(user_query_vectorized, X)

    # Get the index of the most similar question
    most_similar_index = np.argmax(similarities)

    # Return the corresponding response
    if similarities[0][most_similar_index] < 0.5:  # Adjust the threshold as needed
        return "I'm sorry, but I don't have that information available at the moment. Is there anything else I can help you with?"
    return responses[most_similar_index]


