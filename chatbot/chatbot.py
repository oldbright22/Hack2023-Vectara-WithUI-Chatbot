
import os
import requests

#from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain.chat_models import ChatOpenAI
#from langchain.llms import HuggingFaceHub
#from langchain.vectorstores import Pinecone
#from langchain.chains import LLMChain

#from langchain.prompts.chat import (
#    ChatPromptTemplate,
#    SystemMessagePromptTemplate,
#    HumanMessagePromptTemplate,
#)

#from getpass import getpass

from dotenv import find_dotenv, load_dotenv
import streamlit as st

CUSTOMER_ID = st.secrets("CUSTOMER_ID")
X_API_KEY = st.secrets("X_API_KEY")
CUSTOMERID = st.secrets("CUSTOMERID")
VTOKEN = st.secrets("TOKEN")
CORPUSID = st.secrets("CORPUSID")            

class MaverickChatbot:
    
    def __init__(self):
        load_dotenv(find_dotenv())

    @st.cache_data(show_spinner=False)
    def get_response_from_query(_self, query):
        """
        Function that generates a response to a customer question using LLama and Vectara DB
        """
        try:


            madeitthisfar = "begin"
            # Get the values from environment variables
            #customer_id = os.getenv("CUSTOMER_ID")
            #x_api_key = os.getenv("VECTARA_API_KEY")
            #customerid = os.getenv("CUSTOMERID")
            #vectara_token = os.getenv("TOKEN")
            #corpusid = os.getenv("CORPUSID")
           

            madeitthisfar = f"(1){CUSTOMER_ID} (2) {X_API_KEY} (3) {CUSTOMERID} (4) {VTOKEN} (5) {CORPUSID} "

            url = 'https://api.vectara.io/v1/query'


            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'customer-id': CUSTOMER_ID,
                'x-api-key': X_API_KEY
            }


            data = {
                "query": [
                    {
                        "query": query,
                        "start": 0,
                        "numResults": 5,
                        "corpusKey": [
                            {
                                "customerId": CUSTOMERID,
                                "corpusId": CORPUSID,
                                "semantics": "DEFAULT",
                                "dim": [
                                    {
                                        "name": "string",
                                        "weight": 0
                                    }
                                ],
                                "metadataFilter": "part.lang = 'eng'",
                                "lexicalInterpolationConfig": {
                                    "lambda": 0
                                }
                            }
                        ],
                        "rerankingConfig": {
                            "rerankerId": 272725717
                        },
                        "summary": [
                            {
                                "summarizerPromptName": "string",
                                "maxSummarizedResults": 0,
                                "responseLang": "string"
                            }
                        ]
                    }
                ]
            }
        
        
            madeitthisfar = "prior to api call - vectara"
            #Perform API call - POST towards  VECTARA DB  
            response1 = requests.post(url, headers=headers, json=data)

            madeitthisfar = "after to api call - vectara"
            if response1.status_code == 200:
                response_json = response.json()

                # Check if results are available
                if "responseSet" in response_json and len(response_json["responseSet"]) > 0:
                    ##############################################################################################################################
                    # text = response narrow down from VectaraDB to a customer query that will be used later by Llama-2-70b-chat-hf as GUIDELINE
                    ##############################################################################################################################
                    for result in response_json["responseSet"][0]["response"]:
                        text = result.get("text", "")
                        madeitthisfar = "got a text narrow down from vectara"
                        #print("Extracted Text:")
                        #print(text)
                else:
                    return "1ST -- No results were found for the query."
                    #print("No results were found for the query.")
            else:
                return f"2ND -- Request failed with status code: {response1.status_code}"
                #print(f"Request failed with status code: {response.status_code}")


            s = requests.Session()

            madeitthisfar = "prior to LLM call"
            #api_base = os.getenv("ANYSCALE_API_BASE")
            api_base = "https://api.endpoints.anyscale.com/v1"
            token = VTOKEN
            url = f"{api_base}/chat/completions"
            body = {
                    "model": "meta-llama/Llama-2-70b-chat-hf",
                    "messages": [{"role": "system", "content": "Your name is Kamal and you are a helpful and casual consultation doctor, you will extract and summarize factual information from {text} and give an accurate response(don't summarize links so write them as source), The is information from {text} is to prevent you from hallucination and guide you to provide factual information. Make sure you are conversational, use relevant emojis in some some cases. You understand how to handle compliment and greetings such as Hello, what's up, hey, Thank you etc. In a circumstance in which you don't have enough information just say 'I'm out of information, can say something different?' "}, 
                                 {"role": "user", "content": query}],
                                  "temperature": 0.7
                   }

            response = s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body)

            madeitthisfar = "after LLM call"
            if response.status_code == 200:
                response_json = response.json()
                chatbot_response = response_json["choices"][0]["message"]["content"]
                #print("Chatbot Response:")
                madeitthisfar = "after LLM call" + chatbot_response
                return chatbot_response
            else:
                return f"4th -- Request failed with status code: {response.status_code}"
                #print(f"Request failed with status code: {response.status_code}")

            
        except:
            return f"EXCEPTION - No response available at this time - how far in the code are we = {madeitthisfar}"
