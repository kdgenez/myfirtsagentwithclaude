import os
import requests
from datetime import datetime
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.utilities import GoogleSearchAPIWrapper
import math

def web_search_function(query: str) -> str:
    """
    Función para realizar búsquedas web usando Google Search API.
    Requiere GOOGLE_API_KEY y GOOGLE_CSE_ID en variables de entorno.
    """
    try:
        # Verificar si las credenciales están disponibles
        if not os.getenv("GOOGLE_API_KEY") or not os.getenv("GOOGLE_CSE_ID"):
            return "Error: No se encontraron las credenciales de Google Search API. Verifica GOOGLE_API_KEY y GOOGLE_CSE_ID."
        
        # Inicializar wrapper de Google Search
        search = GoogleSearchAPIWrapper(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            google_cse_id=os.getenv("GOOGLE_CSE_ID"),
            k=3  # Número de resultados a retornar
        )
        
        # Realizar búsqueda
        results = search.run(query)
        return results
        
    except Exception as e:
        return f"Error en la búsqueda web: {str(e)}"

def calculator_function(expression: str) -> str:
    """
    Calculadora segura que evalúa expresiones matemáticas básicas.
    Soporta operaciones aritméticas y funciones matemáticas comunes.
    """
    try:
        # Diccionario de funciones matemáticas permitidas
        allowed_functions = {
            'abs': abs,
            'round': round,
            'pow': pow,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'pi': math.pi,
            'e': math.e,
        }
        
        # Limpiar la expresión de caracteres peligrosos
        safe_expression = expression.replace("__", "").replace("import", "").replace("exec", "").replace("eval", "")
        
        # Evaluar la expresión de forma segura
        result = eval(safe_expression, {"__builtins__": {}}, allowed_functions)
        
        return f"Resultado: {result}"
        
    except ZeroDivisionError:
        return "Error: División por cero"
    except Exception as e:
        return f"Error en el cálculo: {str(e)}. Asegúrate de usar una expresión matemática válida."

def get_current_datetime() -> str:
    """
    Obtiene la fecha y hora actual en formato legible.
    """
    try:
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = now.strftime("%A")
        
        return f"Fecha y hora actual: {formatted_datetime} ({day_of_week})"
        
    except Exception as e:
        return f"Error al obtener fecha y hora: {str(e)}"

def create_memory():
    """
    Crea una instancia de memoria conversacional para el agente.
    """
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )

# Definición de herramientas para el agente
web_search_tool = Tool(
    name="Web Search",
    func=web_search_function,
    description="Útil para buscar información actualizada en internet. Input: consulta de búsqueda como texto."
)

calculator_tool = Tool(
    name="Calculator",
    func=calculator_function,
    description="Útil para realizar cálculos matemáticos. Input: expresión matemática como texto (ej: '2+2', 'sqrt(16)', 'sin(pi/2)')."
)

get_current_datetime_tool = Tool(
    name="Current DateTime",
    func=get_current_datetime,
    description="Útil para obtener la fecha y hora actual. No requiere input, simplemente úsala cuando necesites saber qué día/hora es."
)

def validate_environment_variables():
    """
    Valida que todas las variables de entorno necesarias estén presentes.
    """
    required_vars = ["GROQ_API_KEY"]
    optional_vars = ["GOOGLE_API_KEY", "GOOGLE_CSE_ID"]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    return missing_required, missing_optional

def get_system_info():
    """
    Retorna información básica del sistema y configuración.
    """
    missing_required, missing_optional = validate_environment_variables()
    
    info = {
        "required_vars_missing": missing_required,
        "optional_vars_missing": missing_optional,
        "all_required_present": len(missing_required) == 0
    }
    
    return info
