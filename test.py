from langfuse.decorators import observe, langfuse_context
from langfuse import Langfuse
import google.generativeai as genai
import os

# GEMINI
class GeminiGo:
    def __init__(self):
        genai.configure(api_key="AIzaSyBYoPvmaMksSDmRVvwQg3PKEdPLpRqrRso")  # Obtenha em: https://aistudio.google.com/app/apikey
        self.model = genai.GenerativeModel('gemini-pro')

    def generate(self, prompt: str):
        try:
            response = self.model.generate_content(prompt)
            return response
        except Exception as e:
            
            class DefaultResponse:
                text = f"O modelo não respondeu devido ao erro {e}. Por favor, tente novamente mais tarde."
                class UsageMetadata:
                    prompt_token_count = 0
                    candidates_token_count = 0
                    total_token_count = 0
                usage_metadata = UsageMetadata()
            return DefaultResponse()

# LANGFUSE
class LangFuseGo:
    def __init__(self):

        os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-27ab311a-ee65-4ca0-88ab-322b33c8467d"
        os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-1c4e4496-7e91-425b-acba-19b3a9b9eb34"
        os.environ["LANGFUSE_HOST"] = "http://localhost:3000"
        self.langfuse = Langfuse()

    @observe(as_type="generation")
    def send_lang(self, prompt: str, response, name_user,sess_id):

        # Atualização dos metadados
        langfuse_context.update_current_observation(
            input=prompt,
            output=response.text,
            model="gemini-pro",
            usage={"input": response.usage_metadata.prompt_token_count,
                    "output": response.usage_metadata.candidates_token_count,
                    "total": response.usage_metadata.total_token_count})

        # Atualizar ID
        langfuse_context.update_current_trace(user_id=name_user,session_id=sess_id)

        # Coleta de feedback do usuário
        feedback   = input("Por favor, avalie a resposta de 0 a 1: ") # Valor da avaliação do usuário
        comment    = input("Deixe um comentário (opcional): ") or "Sem comentario"
        evaluation = "avaliacao-resposta-chat"

        # Adição de score usando método correto
        langfuse_context.score_current_observation(name=evaluation,value=float(feedback),  comment=comment)

        self.langfuse.flush()

if __name__ == "__main__":

    
    name_user = str(input("Nome Do Usuario : "))
    sess_id   = "Sessão_"+name_user

    go_model = GeminiGo()
    go_lang = LangFuseGo()
    prompt_lang = go_lang.langfuse.get_prompt("juridico_instrutor", label="latest")
    print("Prompt Editado ",prompt_lang.prompt)
    while True :
        
        prompt = str(input("Digite a pergunta: "))
        response_model = go_model.generate(prompt_lang.prompt+prompt)
        print(response_model.text)
        go_lang.send_lang(prompt,response_model,name_user,sess_id)
