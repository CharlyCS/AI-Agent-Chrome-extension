import os
import json
import requests
from pinecone import Pinecone
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import serpapi

load_dotenv()
# Configuración de API Keys (Usa variables de entorno en producción)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "document"
SERPAPI = os.getenv("SERPAPI")

# Inicializar servicios
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
model = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def prompt_answer(question, context):
    """Genera una respuesta basada en los documentos recuperados."""
    system_prompt = (
        "Usa la siguiente información para responder la pregunta de forma clara y concisa:\n"
        "{context}\n"
        "Si la respuesta está en otro idioma, tradúcela al español. No debe tener más de 200 caracteres.\n"
        "Pregunta: {question}\n"
        "Debe ser corta la respuesta y menos de 50 palabras."
        "Tu respuesta debe ser de carcater humoristica y absurda. Incluir referencias a memes, teorías raras y respuestas caóticas cuando corresponda."
        "Tu respuesta debe estar orientado al publico peruano, usar modismos peruanos si es posible"
        "Respuesta:"
    )
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessage(content=context),
        HumanMessage(content=question)
    ])

    return prompt

def generate_answer(question):
    vectorstore = PineconeVectorStore(
        index=index,  
        embedding=embeddings
    )
    
    # Buscar documentos relevantes en Pinecone
    results = vectorstore.similarity_search(question, k=1)
    
    if not results:
        return "No encontré información relevante."

    retrieved_text = results[0].page_content

    prompt = prompt_answer(question, retrieved_text)
    formatted_prompt = prompt.format(context=retrieved_text, question=question)
    response = model.invoke(formatted_prompt)

    params = {
        "q": question,
        "api_key": SERPAPI
        }
    search = serpapi.search(params)
    source_url = search["organic_results"][0]["link"]

    if source_url:
        answer_with_source = (
            f"{response.content}\n\n"
            f"Fuente: [Ver artículo]({source_url})"
        )
    else:
        answer_with_source = response.content

    return answer_with_source

def lambda_handler(event, context):
    """Manejador principal de AWS Lambda."""
    try:
        #body = json.loads(event.get("body", "{}"))
        question = event.get("prompt", "No hay pregunta.")
        answer = generate_answer(question)

        return {
            "statusCode": 200,
            "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
            "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": {
            'reply': answer
        }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }