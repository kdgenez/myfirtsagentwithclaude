import streamlit as st
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
# Alternativa con OpenAI-compatible API
from langchain_community.chat_models import ChatOpenAI
from utils import (
    web_search_tool,
    calculator_tool,
    get_current_datetime_tool,
    create_memory
)

# Cargar variables de entorno
load_dotenv()

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Agente LangChain con Llama3",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def initialize_llm():
    """
    Inicializa el modelo LLM Llama3-8b-8192 usando Groq.
    Se usa cache para evitar reinicializar el modelo en cada interacción.
    """
    try:
        # Opción 1: Usar Groq como OpenAI-compatible
        llm = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1024,
            timeout=30
        )
        return llm
    except Exception as e:
        st.error(f"Error al inicializar el LLM: {str(e)}")
        return None

@st.cache_resource
def initialize_agent_chain(_llm):
    """
    Inicializa el agente con las herramientas disponibles.
    El underscore en _llm evita problemas de hashing en st.cache_resource.
    """
    try:
        # Definir las herramientas disponibles para el agente
        tools = [
            web_search_tool,
            calculator_tool,
            get_current_datetime_tool,
        ]
        
        # Crear memoria para conversaciones
        memory = create_memory()
        
        # Inicializar el agente con tipo ZERO_SHOT_REACT_DESCRIPTION
        # Este tipo es ideal para tareas generales con herramientas
        agent = initialize_agent(
            tools=tools,
            llm=_llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
            early_stopping_method="generate"
        )
        
        return agent
    except Exception as e:
        st.error(f"Error al inicializar el agente: {str(e)}")
        return None

def display_chat_history():
    """
    Muestra el historial de chat almacenado en st.session_state.
    """
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

def main():
    """
    Función principal que maneja la interfaz de usuario y la lógica de la aplicación.
    """
    # Título principal
    st.title("🤖 Agente LangChain con Llama3-8b-8192")
    st.markdown("---")
    
    # Sidebar con información del proyecto
    with st.sidebar:
        st.header("ℹ️ Información del Agente")
        st.markdown("""
        **Modelo:** Llama3-8b-8192  
        **Proveedor:** Groq  
        **Herramientas disponibles:**
        - 🔍 Búsqueda web
        - 🧮 Calculadora
        - 📅 Fecha y hora actual
        
        **Memoria:** Conversacional con buffer
        """)
        
        # Botón para limpiar historial
        if st.button("🗑️ Limpiar Historial"):
            st.session_state.chat_history = []
            st.session_state.memory = create_memory()
            st.rerun()
    
    # Verificar API Key
    if not os.getenv("GROQ_API_KEY"):
        st.error("⚠️ No se encontró GROQ_API_KEY en las variables de entorno.")
        st.stop()
    
    # Inicializar LLM y agente
    llm = initialize_llm()
    if llm is None:
        st.stop()
    
    agent = initialize_agent_chain(llm)
    if agent is None:
        st.stop()
    
    # Inicializar estado de la sesión
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "memory" not in st.session_state:
        st.session_state.memory = create_memory()
    
    # Mostrar historial de chat existente
    display_chat_history()
    
    # Input del usuario
    user_input = st.chat_input("Escribe tu pregunta aquí...")
    
    if user_input:
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.write(user_input)
        
        # Agregar mensaje del usuario al historial
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        
        # Generar respuesta del agente
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # Ejecutar el agente con la entrada del usuario
                    response = agent.run(input=user_input)
                    
                    # Mostrar respuesta
                    st.write(response)
                    
                    # Agregar respuesta al historial
                    st.session_state.chat_history.append(AIMessage(content=response))
                    
                except Exception as e:
                    error_msg = f"Error al procesar la solicitud: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append(AIMessage(content=error_msg))

if __name__ == "__main__":
    main()
