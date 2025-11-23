from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage


chat_temp = ChatPromptTemplate([('system','You are a helpful {domain} Expert'),('human','Explain in the simple term what is {topic}')
    ])

prompt = chat_temp.invoke({
    'domain':'cricket','topic':'Dusra'
})

print(prompt)
