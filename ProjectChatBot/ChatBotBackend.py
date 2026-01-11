#1 import the ConversationSummaryBufferMemory, ConversationChain, ChatBedrock or ChatBedrockConverse Langchain Modules
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_aws import ChatBedrockConverse
#2a Write a function for invoking model- client connection with Bedrock with profile, model_id & Inference params- model_kwargs

def demo_chatbot():
    demo_llm=ChatBedrockConverse(
        model = "us.deepseek.r1-v1:0",
        temperature=0.1,
        max_tokens=1000)
    return demo_llm


#2b Test out the LLM with invoke method
# user_message="What is LLM ?"
# messages=[ 
#       { 
#          "content": [ 
#             {"text":user_message}
#          ],
#          "role": "user"
#       }
#    ]
# responce=demo_chatbot(messages)
# print(responce)
#3 Create a Function for ConversationBufferMemory (llm and max token limit)
def demo_memory():
    llm_data=demo_chatbot()
    memory=ConversationSummaryBufferMemory(llm=llm_data,max_token_limit=2000)
    return memory

#4 Create a Function for Conversation Chain - Input text + Memory (i.e. llm and memory)
def demo_conversation(input,memory):
    llm_chain_data=demo_chatbot()
    llm_conversation=ConversationChain(llm=llm_chain_data,memory=memory,verbose=True)
    chat_reply=llm_conversation.invoke(input)
    return chat_reply['response']

#5 Chat response using invoke (Prompt template)
#Links :
#https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html
#https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html
#https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html