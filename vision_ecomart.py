from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import encodar_imagem

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-vision-preview"

def analisar_imagem(caminho_imagem):
    if ("png" in caminho_imagem or "jpg" in caminho_imagem or "jpeg" in caminho_imagem or "gif" in caminho_imagem or "webp" in caminho_imagem):
        prompt = """"
            Assuma que você é um assistente de chatbot e que provavelmente o usuário está enviado a foto de
            um produto. Faça uma análise dele, e se for um produto com defeito, emita um parecer. Assuma que você sabe e
            processou uma imagem com o Vision e a resposta será informada no formato de saída.

            # FORMATO DA RESPOSTA
        
            Minha análise para imagem consiste em: Parecer com indicações do defeito ou descrição do produto (se não houver defeito)

            ## Descreva a imagem
            coloque a descrição aqui
        """

        imagem_base64 = encodar_imagem(caminho_imagem)

        resposta = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": prompt
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{imagem_base64}",
                    },
                    },
                ],
                }
            ],
            max_tokens=300,
            )
        resposta_final = resposta.choices[0].message.content + ". Na resposta final, apresente detalhes da descrição da imagem."
        return resposta_final
    
    else:
        resposta = """"
            Assuma que você é um assistente de chatbot e que provavelmente o usuário está enviado a foto de um produto.
            Porém a foto enviada está em um formato não suportado.
            Informe e peça ao cliente que envie um arquivo nos formatos suportados.

            #  Formatos Suportados
            'png', 'jpeg', 'gif', 'webp'
        """
        return resposta