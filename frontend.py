import streamlit as st
from ai_agent import chatbot
from langchain_core.messages import HumanMessage
import uuid

st.set_page_config(page_title="ENKI Chat - Demo", page_icon=":robot:")
st.header("ENKI Chat - Demo")
# st.session_state -> dict ->


 ## utility functionss
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
def generate_thread():
    return uuid.uuid4()
def reset_chat():
    new_thread_id = generate_thread()
    del st.session_state.message_history[:]
    st.session_state['thread_id'] = new_thread_id
    add_thread(new_thread_id)
    st.rerun()
def get_thread_hist(thread_id):
    return chatbot.get_state(config={"configurable": {"thread_id": thread_id}}).values.get( 'messages' ,[])
#### intialization
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread()
add_thread(st.session_state['thread_id'])

# loading the conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):

        st.text(message["content"])


### Side bar UI

st.sidebar.title('ENKI BOT')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My Conversations')
for thread in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread)):
        st.session_state['thread_id']=thread
        response = get_thread_hist(thread_id=thread)
        # print(response)
        temp_messages =[]
        for msg in response:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':msg.content})
        st.session_state["message_history"] = temp_messages
# {'role': 'user', 'content': 'Hi'}
# {'role': 'assistant', 'content': 'Hi=ello'}

#### Main UI


user_input = st.chat_input("Type here")

if user_input:

    # first add the message to message_history
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.text(user_input)

    # first add the message to message_history
    with st.chat_message("assistant"):
        CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            )
        )

    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
