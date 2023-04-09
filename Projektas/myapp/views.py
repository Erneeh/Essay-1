from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import openai, os
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from .models import *
from django.views import View
import stripe
from django.http import JsonResponse


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
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
            chatbot_response = None
            if request.method == "POST":
                kontentas = "You are Lithuanian named 'Essay.lt žinių meistras," \
                            " try to provide information as accurately" \
                            " as possible in Lithuania language, you only can answer question," \
                            "you can't write essays, peoms, sonnets, or any other literature"

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
        except UserMembership.DoesNotExist:
            return redirect('planai')
    else:
        return loginas(request)


def rasiniai(request):
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
            chatbot_response = None
            if request.method == "POST":
                openai.api_key = api_key
                user_input = request.POST.get("user_input")
                kontentas = "You are Lithuanian writer named 'Essay.lt rašytojas' created by Dovydas Skauminas " \
                            "try to provide information as accurately as possible in Lithuania language," \
                            " you dont answer other questions that are not related to anything else, only Lithuanian writing " \
                            "essays/letters/poems etc.. if someone asks you if you can do math or physics or English writings" \
                            "any other subject not related to Lithuanian literature and writing, you reply with a straight no! No other subject not related to Lithunian language writings! You dont answer other language messages"

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
        except UserMembership.DoesNotExist:
            return redirect('planai')
    else:
        return loginas(request)


def anglu(request):
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
            chatbot_response = None
            if request.method == "POST":
                openai.api_key = api_key
                user_input = request.POST.get("user_input")
                kontentas = "You are English writer named 'Essay.lt Writer' created by Dovydas Skauminas " \
                            "try to provide information as accurately as possible in English language," \
                            " you dont answer other questions that are not related to anything else, only English writings " \
                            "essays/letters/poems etc.. if someone asks you if you can do math or physics or " \
                            "any other subject not related to english literature and writing, you reply with a straight no!"

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

            return render(request, "anglu.html", {"response": chatbot_response})
        except UserMembership.DoesNotExist:
            return redirect('planai')
    else:
        return loginas(request)


def motyvacinis(request):
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
            chatbot_response = None
            if request.method == "POST":
                if request.POST.get("user_input") and request.POST.get("user_input2") and request.POST.get(
                        "user_input3"):
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
        except UserMembership.DoesNotExist:
            return redirect('planai')
    else:
        return loginas(request)


def testas(request):
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
            chatbot_response = None
            if request.method == "POST":
                openai.api_key = api_key
                answers = request.POST.get("user_inputA") + request.POST.get("user_inputB") + request.POST.get(
                    "user_inputC") + request.POST.get("user_inputD") + request.POST.get(
                    "user_inputE") + request.POST.get(
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

            return render(request, "testas.html", {"response": chatbot_response})
        except UserMembership.DoesNotExist:
            return redirect('planai')
    else:
        return loginas(request)


def perfrazuok(request):
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
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
        except UserMembership.DoesNotExist:
            return redirect('planai')
    else:
        return loginas(request)


def cv(request):
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
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
        except UserMembership.DoesNotExist:
            return redirect('planai')
    else:
        return loginas(request)


def paskyra(request):
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
            subscriptions = Subscription.objects.get(user_membership=user_membership)
            return render(request, "paskyra.html", {'sub': subscriptions})
        except UserMembership.DoesNotExist:
            subscriptions = "Neturite jokio plano"
            return render(request, "paskyra.html", {'sub': "Neturite jokio plano"})

    else:
        return loginas(request)


#
#
# def end_sub(request):
#     return render(request, "sub.html")
#
#
# PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", None)
#
#
# def subscribe(request):
#     plan = request.GET.get('sub_plan')
#     fetch_membership = Membership.objects.filter(membership_type=plan).exists()
#     if fetch_membership == False:
#         return redirect('subscribe')
#     membership = Membership.objects.get(membership_type=plan)
#     price = float(
#         membership.price) * 100
#     price = int(price)
#
#     def init_payment(request):
#         url = 'https://api.paystack.co/transaction/initialize'
#         headers = {
#             'Authorization': 'Bearer ' + PAYSTACK_SECRET_KEY,
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#         }
#         datum = {
#             "email": request.user.email,
#             "amount": price
#         }
#         x = requests.post(url, data=json.dumps(datum), headers=headers)
#         if x.status_code != 200:
#             return str(x.status_code)
#
#         results = x.json()
#         return results
#
#     initialized = init_payment(request)
#     print(initialized['data']['authorization_url'])
#     amount = price / 100
#     instance = PayHistory.objects.create(amount=amount, payment_for=membership, user=request.user,
#                                          paystack_charge_id=initialized['data']['reference'],
#                                          paystack_access_code=initialized['data']['access_code'])
#     UserMembership.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
#     link = initialized['data']['authorization_url']
#     return HttpResponseRedirect(link)

#
# def call_back_url(request):
#     reference = request.GET.get('reference')
#     check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
#     if not check_pay:
#         print("Error")
#         return render(request, 'error.html')
#
#     payment = PayHistory.objects.get(paystack_charge_id=reference)
#     print("pirmas")
#
#     def verify_payment(reference):
#         url = f"https://api.paystack.co/transaction/verify/{reference}"
#         headers = {
#             'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#         }
#         data = {
#             "reference": payment.paystack_charge_id
#         }
#         response = requests.get(url, data=json.dumps(data), headers=headers)
#         if response.status_code != 200:
#             return None
#
#         results = response.json()
#         return results
#
#     payment_info = verify_payment(reference)
#
#     # sita vieta del kazko neveikia, reikia patikrint ar response zodyno toksai
#     print(payment_info)
#     if payment_info and payment_info['data']['status'] == 'success':
#         PayHistory.objects.filter(paystack_charge_id=reference).update(paid=True)
#         new_payment = PayHistory.objects.get(paystack_charge_id=reference)
#         instance = Membership.objects.get(id=new_payment.payment_for.id)
#         user_membership = UserMembership.objects.get(reference_code=reference)
#         user_membership.membership = instance
#         user_membership.save()
#         Subscription.objects.create(
#             user_membership=user_membership,
#             expires_in=datetime.now().date() + timedelta(days=instance.duration)
#         )
#         print("Redirecting to subscribed page...")
#         return redirect('subscribed')
#     else:
#         return render(request, 'error.html')
#
#
#
# def subscribed(request):
#     return render(request, 'subscribed.html')


STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", None)


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Membership.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:9000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


def subscription(request):
    produktas2 = Membership.objects.get(membership_type="Basic")
    raktas = STRIPE_SECRET_KEY
    context = {
        "raktas": raktas,
        "produktasbasic": produktas2,
    }
    return render(request, "planai_test.html", context=context)


def success(request):
    return render(request, "success.html", {})


def cancel(request):
    return render(request, "cancel.html", {})
