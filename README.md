# Proyecto: AI-Powered Chatbot con AWS Lambda y Extensión de Chrome

## Descripción
Este proyecto combina una extensión de Chrome con un backend en AWS Lambda y API Gateway para proporcionar respuestas enriquecidas utilizando un sistema de Retrieval-Augmented Generation (RAG). El sistema utiliza Pinecone para la búsqueda de documentos, OpenAI para la generación de respuestas y SerpAPI para obtener enlaces relevantes desde la web.

## Características principales
- **Web Scraping con SerpAPI:** Obtiene enlaces relevantes desde la web para enriquecer las respuestas.
- **Respuestas humorísticas y personalizadas:** Las respuestas están diseñadas para ser divertidas, absurdas y orientadas al público peruano.

## Tecnologías Utilizadas
- **Python 3.10**
- **AWS Lambda**
- **Pinecone**
- **OpenAI API**
- **Requests** (para búsquedas web)
- **Extensión Chrome (JavaScript, HTML, CSS)**

## Instalación y Configuración
### **Configuración del Backend en AWS Lambda**
1. Instala dependencias:
   ```sh
   pip install -r requirements.txt -t .
   ```
2. Sube el código a AWS Lambda.
3. Configura las siguientes variables de entorno en Lambda:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `SERPAPI_KEY` 
4. Asegúrate de que Lambda tenga permisos para acceder a internet. Habilita el CORS

### **Configuración de la Extensión de Chrome**
1. Clona el repositorio:
   ```sh
   git clone https://github.com/CharlyCS/AI-Agent-Chrome-extension.git
   ```
2. Abre **Google Chrome** y ve a:
   ```
   chrome://extensions/
   ```
3. Activa el **modo desarrollador**.
4. Haz clic en "Cargar extensión sin empaquetar" y selecciona la carpeta `chrome-extension/`.

---

## Uso
### 🚀 **Extensión de Chrome**
1. Haz clic en el ícono de la extensión.
2. Escribe una pregunta.
3. Recibe respuestas generadas por IA en tiempo real.

### 🌎 **API en AWS Lambda**
Puedes hacer una petición POST a la API en AWS con el siguiente formato:
```json
{
  "prompt": "De que trata Where the Zinnias Grow"
}
```
Respuesta esperada:
```json
{
    "statusCode": 200,
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
        "Access-Control-Allow-Headers": "Content-Type"
    },
    "body": {
        "reply": "\"Where the Zinnias Grow\" habla de reflexiones sobre la vida, el dolor y la empatía mientras el autor se encuentra en un jardín botánico. Las zinnias son como los Pokémon raros: bonitos pero con picaduras de experiencia.\n\nFuente: [Ver artículo](https://www.almanac.com/plant/zinnias)"
    }
}
```