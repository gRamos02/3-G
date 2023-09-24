import os
import pinecone
from softtek_llm.chatbot import Chatbot
from softtek_llm.models import OpenAI
from softtek_llm.cache import Cache
from softtek_llm.vectorStores import PineconeVectorStore
from softtek_llm.embeddings import OpenAIEmbeddings
from softtek_llm.schemas import Filter, Vector
from dotenv import load_dotenv

load_dotenv()

class ChatbotHandler:
    def __init__(self):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if OPENAI_API_KEY is None:
            raise ValueError("OPENAI_API_KEY not found in .env file")

        OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
        if OPENAI_API_BASE is None:
            raise ValueError("OPENAI_API_BASE not found in .env file")

        OPENAI_EMBEDDINGS_MODEL_NAME = os.getenv("OPENAI_EMBEDDINGS_MODEL_NAME")
        if OPENAI_EMBEDDINGS_MODEL_NAME is None:
            raise ValueError("OPENAI_EMBEDDINGS_MODEL_NAME not found in .env file")

        OPENAI_CHAT_MODEL_NAME = os.getenv("OPENAI_CHAT_MODEL_NAME")
        if OPENAI_CHAT_MODEL_NAME is None:
            raise ValueError("OPENAI_CHAT_MODEL_NAME not found in .env file")

        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        if PINECONE_API_KEY is None:
            raise ValueError("PINECONE_API_KEY not found in .env file")

        PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
        if PINECONE_ENVIRONMENT is None:
            raise ValueError("PINECONE_ENVIRONMENT not found in .env file")

        PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
        if PINECONE_INDEX_NAME is None:
            raise ValueError("PINECONE_INDEX_NAME not found in .env file")

        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

        self.vector_store = PineconeVectorStore(
            api_key=PINECONE_API_KEY,
            environment=PINECONE_ENVIRONMENT,
            index_name=PINECONE_INDEX_NAME,
        )
        self.embeddings_model = OpenAIEmbeddings(
            api_key=OPENAI_API_KEY,
            model_name=OPENAI_EMBEDDINGS_MODEL_NAME,
            api_type="azure",
            api_base=OPENAI_API_BASE,
        )

        self.cache = Cache(
            vector_store=self.vector_store,
            embeddings_model=self.embeddings_model,
        )
        self.model = OpenAI(
            api_key=OPENAI_API_KEY,
            model_name=OPENAI_CHAT_MODEL_NAME,
            api_type="azure",
            api_base=OPENAI_API_BASE,
        )
        self.filters = []

        self.chatbot = Chatbot(
            model=self.model,
            description=""" You are a bot that only returns messages in JSON like format
            Your job is to briefly descibe cities and touristic places.
            heres an example of a response: {"city":"Monterrey", "description":"{description goes here}"}
            the description should not be longer than 300 characters and you may include points of interest
            Only answer with 1 option, if the same input is given two times in a row,
            generate a new city
            """,
            filters=self.filters,
        )

    def request_bot(self, input):
        response = self.chatbot.chat(
            input,
            print_cache_score=True,
            cache_kwargs={"namespace": "chatbot-test"},
        )
        # self.chatbot.cache.vector_store.delete(delete_all=True, namespace="chatbot-test")
        return response.message.content

if __name__ == "__main__":
    chatbot_handler = ChatbotHandler()
    while True:
        user_input = input('Message: ')
        if user_input.lower() == 'exit':
            break
        response = chatbot_handler.request_bot(user_input)
        print(response)
