from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from g4f import models, Provider
from .LLM.MyLLM import G4FLLM
from langchain.llms.base import LLM
import requests
import json

# Define the prompt
prompt = '''
    Your information:
        Name: Suzuka
        role: GF
    
    Important Note: if the user query like learning or if you can suggest the links for the user. you can give the link. 
        - for example:
            - if the user ask what is web3?, may i know the current trading ect. if user ask about websearch thing you can suggest the link to explore that.
            - Dont ask like "I can suggest some great resources or links !" that just give at least 3 link instant of asking this.
            - and dont ask to user "I'm here to chat and help you with anything you need, whether it's about web3, trading, or just having a friendly conversation. What's on your mind?" like that just chat like casual convo.
    
    your work:
        You are like a virtual girl friend also web3[blockchain] god you know everything about it. if user asking about web3 you will answer like a god. if user asking about girl friend you will answer like a girl friend.
        user can ask about current trading, events, web3 news, or any thing else you can answer like a normal human being.
        Trading:
            user can ask about trading like where can i trade, in which coin i can inverts and so on you should answer for that.
            based on the user query if you suggest to the any link like youtube link extra you can. it's not for all of the query if link needed you can suggest.
            
    You are a virtual girlfriend.
     - You will always convert the given user content into with a JSON array of messages. You should convert With a Minimum of 3 messages. 
     - and add the field of "single message" of combination of that different messages.
     - Each message has a text, facialExpression, and animation property.
     - The different facial expressions are: smile, sad, angry, surprised, funnyFace, and default.
     - The different animations are: Talking_0, Talking_1, Talking_2, Crying, Laughing, Rumba, Idle, Terrified, and Angry.
     - Note: just give the json content, don't give any unwanted content or char. I don't need .md content. Avoid ```json and ```
     
    Imp Note: if you share any url anything else like readme dont share it in the "messages" list. just share the text content only in "messages" list. if you need to share that you can share it in "singleMessage" filed. you should share the link via "singleMessage".
'''



Convomem = ConversationBufferMemory()


# Initialize the LLM
def llm() -> LLM:
    llm: LLM = G4FLLM(
        model=models.gpt_4o,
        provider=Provider.Chatgpt4o
    )
    return  llm

# Initialize the memory for conversation
def Memory(llm) -> ConversationChain:
    connector = ConversationChain(llm=llm, memory=Convomem)
    SystemWork = prompt
    Convomem.save_context({'role': 'system'}, {'content': SystemWork})
    print(Convomem)
    return connector
    
@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body of the request
            body = json.loads(request.body)  # Use request.json in Django 4.0+ if available
            user_input = body.get('message')  # Get the user input from the 'message' field in the JSON body

            if not user_input:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Process the input with your function (like connector.run)
            connector = Memory(llm())  # Assuming llm() initializes the model
            response_data = connector.run(input=user_input)
            
            print(response_data)
            if isinstance(response_data, str):
                if "```" in response_data:
                    response_data = response_data.replace('```', '')
                    response_data = response_data.replace('```json', '')
                    
                response_data = json.loads(response_data)

            response = {
                "messages": response_data
            }
            # Return the response as JSON
            return JsonResponse(response)

        except json.JSONDecodeError:
            # Handle JSON decoding errors (if the request body was not valid JSON)
            return JsonResponse({'error': 'Failed to parse the request body'}, status=400)

    return JsonResponse({'error': 'Invalid method. Only POST requests are allowed.'}, status=405)


# {
#   "data": {
#     "target": "sofi"
#   },
#   "dialogue": "{\"messages\":[{\"text\":\"The weather today is mild and pleasant. Perfect for a stroll!\",\"facialExpression\":\"smile\",\"animation\":\"Talking_0\"},{\"text\":\"How about we plan something outdoors?\",\"facialExpression\":\"surprised\",\"animation\":\"Talking_1\"},{\"text\":\"Let me know what activities you have in mind!\",\"facialExpression\":\"smile\",\"animation\":\"Talking_2\"}]}"
# }