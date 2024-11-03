
from lightrag import LightRAG, QueryParam
from langchain_community.document_loaders import PyPDFLoader
import asyncio

import os 

rag = LightRAG(working_dir="./fuuast_index")

def rag_response_generator(user_message) -> str:
    """
    you will respond to user question if something specific about university
    """
    master = os.environ.get('ASSISTANT_MASTERY','gynecologist')
    result = rag.query(f"""
                    you are helpful assistant and you provide information about
                       Fedral Urdu University of  Arts, Science and Technology 
                       Islamabad. You have access to knowladge. You will understand
                       user query  and provide relevant information. 
                       If no relevent information is given then you will generate response 
                       yourself.

                       Here is user message

                       {user_message}
                    """, param=QueryParam(mode="global"))
    return result



