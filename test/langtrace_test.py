# Must precede any llm module imports
import os
from langtrace_python_sdk import langtrace
import google.generativeai as genai
from langtrace_python_sdk import get_prompt_from_registry
os.environ["LANGTRACE_API_KEY"] = '42bcffeefbe4144f13cb6a64394de34e521bf64ec65b45b1f7a0743c29165202'


print(os.environ["LANGTRACE_API_KEY"])  # Verifica se foi definida corretamente


import google.generativeai as genai
import os
from langtrace_python_sdk import langtrace, with_langtrace_root_span  # Must precede any llm module imports

langtrace.init(api_key = '42bcffeefbe4144f13cb6a64394de34e521bf64ec65b45b1f7a0743c29165202')


# @with_langtrace_root_span("chat_complete")
# def chat_complete():
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     genai.configure(api_key="AIzaSyBYoPvmaMksSDmRVvwQg3PKEdPLpRqrRso"])

#     chat_response = genai.chat.complete(
#         model=model,
#         response=model.generate_content("Conte sobre a história do Brasil"),

#     )
#     print(chat_response.text)
#     print(chat_response.choices[0].response.content)

# chat_complete()


genai.configure(api_key="AIzaSyBYoPvmaMksSDmRVvwQg3PKEdPLpRqrRso") 
def gemini_completion(prompt: str):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        data = {
            "userScore": user_score,
            "userId": user_id,
            "spanId": span_id,
            "traceId": trace_id
        }
        SendUserFeedback().evaluate(data=data)
            
        return response.text
    
    except Exception as e:
        print( f"Erro na geração: {str(e)}")
        raise


import json


# Paste this code after your langtrace init function
response = get_prompt_from_registry('cm6shwnlx00015sky13q97qk9')

# prompt = json.loads(prompt) # for json prompts (ex: tool calling)
prompt = response['value']

print(prompt)

result = gemini_completion(prompt)
print(f"Resposta: {result}")
