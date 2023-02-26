from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Feature
import openai, datetime

# Create your views here.
def index(request):
    context={
        'name':'surya',
        'age':20,
        'nationality':'Indian'

    }#return render(request,'index.html',context)  this is to render the index.html content

    feature1=Feature()
    feature1.id =0
    feature1.name='Very Fast'
    feature1.details='it is compartively very fast then others'

    feature2=Feature()
    feature2.id =1
    feature2.name='high Transimission'
    feature2.details='it is compartively very fast then others devies'

    feature3=Feature()
    feature3.id =2
    feature3.name='responsive to all screens'
    feature3.details='it is compartively very fast then others objects'

    features=[feature1,feature2,feature3]
    
    return render(request,'index.html',{'features':features})

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        #phone_no=request.POST['phone_no']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exits')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exits')
                return redirect('register')
            #elif User.objects.filter(phone_no=phone_no).exists():
             #   messages.info(request,'phone number already exits')
             #   return redirect('register')'''
            elif User.objects.filter(first_name=first_name).exists():
                messages.info(request,'First name already exits')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
                user.save()
                return redirect('studemp')
        else:
            messages.info(request,'password not the same')
            return redirect('register')
    else:
        return render(request,'register.html')

def counter(request):
    letters=request.POST['text']     #this is the place where the text from index.html is rendered
    amt_of_words=len(letters.split())
    return render(request,'counter.html',{'count':amt_of_words})

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home') 
        else:
            messages.info(request,'Credential are not valid')
            return redirect('login')
    else:
        return render(request,'login.html')

def studemp(request):
    return render(request,'studemp.html')

'''def store(request):
    return HttpResponse('<h1>this is surya\'s store</h1>')'''


# chatbot ...........................................
def gpt(queary):
    openai.api_key = "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"
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    return response.choices[0].get("text")

messages = []
def chatbot(request):
    times = datetime.datetime.now()
    current_time = times.strftime("%H:%M %p")
    usr_input = request.GET.get('usr_input')
    print(usr_input)
    messages.append(usr_input)
    replay=""
    try:
        replay = gpt(usr_input)
        messages.append(replay)
    except:
        replay=None
    print(replay)
    if(replay == None):
        if usr_input != None :
            replay = gpt(usr_input)
        elif(usr_input == None) :
            replay = ""
        messages.append(replay)
    makefullcode = ""
    for i,x in enumerate(messages):
        if(i != 0 and i != 1):
            if(i%2 == 0):
                user = f"""<div id="messages" class="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch">
                                <div class="chat-message">
                                    <div class="flex items-end">
                                        <div class="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-2 items-start">
                                            <div><span class="px-4 py-2 rounded-lg inline-block rounded-bl-none bg-gray-300 text-gray-600">{x}</span></div>
                                        </div>
                                        <img src="https://images.unsplash.com/photo-1549078642-b2ba4bda0cdb?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=3&amp;w=144&amp;h=144" alt="My profile" class="w-6 h-6 rounded-full order-1">
                                    </div>
                            </div>
                
                """
                makefullcode = makefullcode + user 
            else:
                system_ = f"""<div class="chat-message">
                                    <div class="flex items-end justify-end">
                                        <div class="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-1 items-end">
                                            <div><span class="px-4 py-2 rounded-lg inline-block rounded-br-none bg-blue-600 text-white ">{x}</span></div>
                                        </div>
                                        <img src="https://images.unsplash.com/photo-1590031905470-a1a1feacbb0b?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=3&amp;w=144&amp;h=144" alt="My profile" class="w-6 h-6 rounded-full order-2">
                                    </div>
                                </div>                
                """
                makefullcode = makefullcode + system_ 
    frontend = {"codes":makefullcode}

    return render(request,'chatbot/chatbot.html',frontend)
    


# ....... room chating
