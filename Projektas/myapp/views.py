from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import openai, os
from dotenv import load_dotenv


def index(request):
    return render(request, "index.html", {})


def services(request):
    return render(request, "services.html", {})


def contacts(request):
    return render(request, "contacts.html", {})


def register(request):
    uname = request.POST.get('uname')
    nickname = User.objects.filter(username=uname).exists()
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        password2 = request.POST.get('pass2')
        nickname = User.objects.filter(username=uname).exists()

        if password == password2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, f"Slapyvardis '{uname}' užimtas!")
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"El.paštas '{email}' užimtas!")
                    return redirect("register")
                else:
                    new_user = User.objects.create_user(uname, email, password)
                    new_user.save()
                    return redirect('login')
        else:
            messages.error(request, "Slaptažodžiai nesutampa!")
            return redirect("register")
    return render(request, "register.html", {"nickname": nickname})


def loginas(request):
    if request.method == "POST":
        name = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Vartotojas neegzistuoja arba neteisingi duomenys!")
            return redirect('login')

    return render(request, "login.html", {})


def logoutuser(request):
    logout(request)
    return redirect('index')


load_dotenv()

api_key = os.getenv("OPENAI_KEY", None)


def paklausk(request):
    chatbot_response = None
    if request.method == "POST":
        kontentas = "You are Lithuanian named 'Essay.lt žinių meistras," \
                    " try to provide information as accurately" \
                    " as possible in Lithuania language"

        openai.api_key = api_key
        user_input = request.POST.get("user_input")

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system",
                 "content": kontentas},
                {"role": "user", "content": user_input}
            ],

            temperature=0.7
        )
        chatbot_response = response['choices'][0]['message']['content']

    return render(request, "paklausk.html", {"response": chatbot_response})


def rasiniai(request):
    chatbot_response = None
    if request.method == "POST":
        openai.api_key = api_key
        user_input = request.POST.get("user_input")
        kontentas = "You are Lithuanian writer named 'Essay.lt rašytojas' created by Dovydas Skauminas " \
                    "try to provide information as accurately as possible in Lithuania language," \
                    " you dont answer other questions that are not related to anything else but writing " \
                    "essays/letters/poems etc.. if someone asks you if you can do math or physics or " \
                    "any other subject not related to literature and writing, you reply with a straight no!"

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system",
                 "content": kontentas},
                {"role": "user", "content": user_input}
            ],

            temperature=0.3
        )
        chatbot_response = response['choices'][0]['message']['content']

    return render(request, "rasiniai.html", {"response": chatbot_response})


def motyvacinis(request):
    chatbot_response = None
    if request.method == "POST":
        if request.POST.get("user_input") and request.POST.get("user_input2") and request.POST.get("user_input3"):
            openai.api_key = api_key
            user_input = "Parašyk darbo laišką darbdaviui, " + "turiu " + request.POST.get(
                "user_input") + request.POST.get(
                "user_input2") + "srityje, " "pretenduoju į " + request.POST.get("user_input3") + "poziciją"
            kontentas = "You are Lithuanian cover letter writer, you can only build cover letter for job application" \
                        "try to provide information as accurately as possible in Lithuania language," \
                        "you dont answer other questions that are not related to anything that is not cover letter" \
                        "if someone asks you if you can do math or physics, essays, sonnets or " \
                        "any other subject that is not cover letter, you reply with a straight no!"

            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system",
                     "content": kontentas},
                    {"role": "user", "content": user_input}
                ],

                temperature=0.4
            )
            chatbot_response = response['choices'][0]['message']['content']
        else:
            chatbot_response = "Prašau užpildyti visus langelius"

    return render(request, "motyvacinis.html", {"response": chatbot_response})


def testas(request):
    chatbot_response = None
    if request.method == "POST":
        openai.api_key = api_key
        answers = request.POST.get("user_inputA") + request.POST.get("user_inputB") + request.POST.get(
            "user_inputC") + request.POST.get("user_inputD") + request.POST.get("user_inputE") + request.POST.get(
            "user_inputF")
        user_input = f"The subject is {request.POST.get('dalykas')} the question is " \
                     f"{request.POST.get('user_input')}, posibble answers is {answers}"

        kontentas = "You are Lithuanian knowlage master, you can only answer a right answer by given possible answers" \
                    "try to provide information as accurately as possible in Lithuania language," \
                    "you dont answer other questions that are not related to anything that is not selected subject" \
                    "if someone asks you if you can write essays, sonnets or " \
                    "any other poetry, you reply with a straight no, and " \
                    "if you dont understand the questions say that you dont understand the question"

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system",
                 "content": kontentas},
                {"role": "user", "content": user_input}
            ],

            temperature=0.4
        )
        chatbot_response = response['choices'][0]['message']['content']
    else:
        chatbot_response = "Prašau užpildyti visus langelius"

    return render(request, "testas.html", {"response": chatbot_response})


def perfrazuok(request):
    chatbot_response = None
    if request.method == "POST":
        kontentas = "You are Lithuanian paraphraser named 'Essay.lt perfrazuotojas'," \
                    "you can only to paraphrase a user entered text," \
                    "paraphrase text only in Lithuania language," \
                    "you dont answer other questions that are not related to anything that is not to paraphrase text" \
                    "if someone asks you if you can do math or physics or " \
                    "any other subject that is not related to literature and writing, you reply with a straight no!" \
                    "you only can paraphrase the given text"

        openai.api_key = api_key
        user_input = request.POST.get("user_input")

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system",
                 "content": kontentas},
                {"role": "user", "content": user_input}
            ],

            temperature=0.7
        )
        chatbot_response = response['choices'][0]['message']['content']

    return render(request, "perfrazuok.html", {"response": chatbot_response})


def cv(request):
    chatbot_response = None
    if request.method == "POST":
        kontentas = "You are Lithuanian cv writer named 'Essay.lt CV specialistas'," \
                    "you can only write cv by given information a user a user has entered," \
                    "write CV only in Lithuania language," \
                    "you dont answer other questions that are not related to anything that is not related to CV" \
                    "if someone asks you if you can do math or physics or " \
                    "any other subject that is not related to CV writing, you reply with a straight no!"

        openai.api_key = api_key
        user_input = request.POST.get("user_input")

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system",
                 "content": kontentas},
                {"role": "user", "content": user_input}
            ],

            temperature=0.7
        )
        chatbot_response = response['choices'][0]['message']['content']

    return render(request, "cv.html", {"response": chatbot_response})


def paskyra(request):
    return render(request, "paskyra.html", {})