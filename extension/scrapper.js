import { PuppeteerWebBaseLoader } from "@langchain/community/document_loaders/web/puppeteer";
import { OpenAIEmbeddings, ChatOpenAI } from "@langchain/openai";
import { PineconeStore } from "@langchain/pinecone";
import { Pinecone as PineconeClient } from "@pinecone-database/pinecone";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
//import puppeteer from "puppeteer";
const OPENAI_API_KEY = 'your_api';
const embeddings = new OpenAIEmbeddings({
  model: "text-embedding-3-large",
  apiKey: OPENAI_API_KEY
});

//const pinecone = new PineconeClient();
//const pineconeIndex = pinecone.Index(process.env.PINECONE_INDEX!);
const pc = new PineconeClient({
  apiKey: 'your_api'
});
const index = pc.index('document');

(async () => {
    // Inicia Puppeteer

    //const browser = await puppeteer.launch({ headless: true });
  
    // Configura el loader con Puppeteer
    const loader = new PuppeteerWebBaseLoader(
      "https://www.showerthoughts.org/",
      {
        evaluate: (page) => page.evaluate(() => document.body.innerText)
      }
    );
  
    // Carga el contenido de la web como documentos
    const docs = await loader.load();
    console.log(docs[0].pageContent);
    const textSplitter = new RecursiveCharacterTextSplitter({
      chunkSize: 1000,
      chunkOverlap: 200,
    });
    const splits = await textSplitter.splitDocuments(docs);
    const vectorStore = await PineconeStore.fromDocuments(splits, embeddings, { pineconeIndex: index });
    console.log("✅ Datos almacenados en Pinecone");
    //await browser.close(); // Cierra Puppeteer
  })();