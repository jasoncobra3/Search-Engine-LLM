import streamlit as st 
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper , ArxivAPIWrapper
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun , DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import  StreamlitCallbackHandler
from dotenv import load_dotenv
import os
### Arxiv and Wikipedia Tools
arxiv_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)
wiki_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki=WikipediaQueryRun(api_wrapper=wiki_wrapper)
##
search=DuckDuckGoSearchRun(name="Search")

st.title("🔎 LangChain - Chat with search")
"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""
### Sidebar for API key
st.sidebar.title("API Key")
api_key=st.sidebar.text_input("Enter your Groq API Key:",type="password")

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assisstant","content":"Hi,I'm a Chatbot who can search the Web. How can I help you ?"}
    ]
    
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])
    

if prompt:=st.chat_input(placeholder="What is Machine learning?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
    
    llm=ChatGroq(api_key=api_key,model_name="Llama3-8b-8192",streaming=True )
    tools=[search,arxiv,wiki]
    
    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True,allow_tool_calls=True  # Ensure the agent properly calls tools
)
    
    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)
