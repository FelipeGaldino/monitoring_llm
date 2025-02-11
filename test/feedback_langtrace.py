from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
from langtrace_python_sdk import langtrace, with_langtrace_root_span, SendUserFeedback
import google.generativeai as genai
from langtrace_python_sdk import get_prompt_from_registry
import os
os.environ["LANGTRACE_API_KEY"] = 'a0815fb2c80110889dfbfb581f9de77bbc4c1496bed006a24702591629cc128e'

_ = load_dotenv(find_dotenv())

# Initialize Langtrace SDK
langtrace.init()

genai.configure(api_key="AIzaSyBYoPvmaMksSDmRVvwQg3PKEdPLpRqrRso") 
def gemini_api(span_id, trace_id):
    print(trace_id)

    try:
        model = genai.GenerativeModel('gemini-pro')

        # Paste this code after your langtrace init function
        response = get_prompt_from_registry('cm6sbjzyp0014tefad9ei9068')

        # prompt = json.loads(prompt) # for json prompts (ex: tool calling)
        prompt = response['value']
        print(prompt)

        response = model.generate_content(prompt)

        data = {
            "userScore": 10,
            "userId": "Felipe123",
            "spanId": span_id,
            "traceId": trace_id}

        SendUserFeedback().evaluate(data=data) 
        # Registre o feedback
    # Adicionar feedback como atributos
        langtrace.inject_additional_attributes({
            "user_score": 5,
            "user_id": "felipegaldino",
            "feedback_text": "Resposta útil!"
        })
        return response.text
    
    except Exception as e:
        print( f"Erro na geração: {str(e)}")
        raise

# wrap the API call with the Langtrace root span
wrapped_api = with_langtrace_root_span()(gemini_api)

# Call the wrapped API
wrapped_api()


