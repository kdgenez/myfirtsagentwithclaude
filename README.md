# myfirtsagentwithclaude

# 🤖 Agente LangChain con Llama3-8b-8192

Este proyecto implementa un agente conversacional inteligente usando LangChain con el modelo Llama3-8b-8192 de Groq, ejecutándose en una interfaz Streamlit.

## ✨ Características

- **LLM**: Llama3-8b-8192 via Groq API
- **Framework**: LangChain para orquestación de agentes
- **Interfaz**: Streamlit para UI web interactiva
- **Herramientas**:
  - 🔍 Búsqueda web (Google Search API)
  - 🧮 Calculadora matemática
  - 📅 Fecha y hora actual
- **Memoria**: Conversacional con historial persistente

## 📁 Estructura del Proyecto

```
langchain-agent/
├── app.py              # Aplicación principal Streamlit
├── utils.py            # Herramientas y funciones auxiliares
├── requirements.txt    # Dependencias Python
├── .env               # Variables de entorno (crear desde template)
└── README.md          # Este archivo
```

## 🚀 Instalación

### 1. Clonar/Crear el proyecto
```bash
mkdir langchain-agent
cd langchain-agent
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env .env.local  # Copia el template
```

Edita `.env` y completa las siguientes variables:

#### Obligatorias:
- `GROQ_API_KEY`: Tu API key de Groq ([obtener aquí](https://console.groq.com/keys))

#### Opcionales (para búsqueda web):
- `GOOGLE_API_KEY`: API key de Google ([obtener aquí](https://developers.google.com/custom-search/v1/introduction))
- `GOOGLE_CSE_ID`: ID del Custom Search Engine ([crear aquí](https://cse.google.com/cse/))

## 🏃‍♂️ Ejecución

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 🛠️ Uso

1. **Conversación básica**: Haz preguntas generales al agente
2. **Cálculos**: Pide cálculos matemáticos ("Calcula 2+2*5")
3. **Búsqueda web**: Solicita información actualizada ("Busca noticias sobre IA")
4. **Fecha/hora**: Pregunta por la fecha actual

### Ejemplos de uso:
- "¿Qué día es hoy?"
- "Calcula la raíz cuadrada de 144"
- "Busca información sobre el clima en Medellín"
- "¿Cuál es el resultado de sin(π/2)?"

## 🔧 Personalización

### Agregar nuevas herramientas
Edita `utils.py` y agrega nuevas funciones siguiendo este patrón:

```python
def nueva_herramienta_function(input_param: str) -> str:
    # Tu lógica aquí
    return resultado

nueva_herramienta_tool = Tool(
    name="Nombre de la Herramienta",
    func=nueva_herramienta_function,
    description="Descripción de cuándo usar esta herramienta."
)
```

### Modificar configuración del modelo
En `app.py`, ajusta los parámetros del modelo:

```python
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192",
    temperature=0.7,      # Creatividad (0-1)
    max_tokens=1024,      # Longitud máxima respuesta
    timeout=30,           # Timeout en segundos
    max_retries=2         # Reintentos en caso de error
)
```

## 🐛 Troubleshooting

### Error "No se encontró GROQ_API_KEY"
- Verifica que el archivo `.env` existe
- Confirma que `GROQ_API_KEY` está configurado correctamente
- Reinicia la aplicación después de cambios en `.env`

### Error en búsqueda web
- Las búsquedas web son opcionales
- Configura `GOOGLE_API_KEY` y `GOOGLE_CSE_ID` si quieres habilitarlas
- El agente funcionará sin estas credenciales, pero sin capacidad de búsqueda

### Errores de dependencias
```bash
pip install --upgrade -r requirements.txt
```

## 📝 Notas Técnicas

- **Modelo**: Llama3-8b-8192 es un modelo optimizado para velocidad y eficiencia
- **Memoria**: Se mantiene durante la sesión, se reinicia al cerrar/recargar
- **Limite de tokens**: 8192 tokens de contexto máximo
- **Rate limits**: Respeta los límites de la API de Groq

## 🆘 Soporte

Si encuentras problemas:

1. Verifica que todas las dependencias estén instaladas
2. Confirma que las API keys sean válidas
3. Revisa los logs en la consola de Streamlit
4. Verifica tu conexión a internet para las herramientas web

## 📄 Licencia

Este proyecto es de código abierto. Úsalo y modifícalo según tus necesidades.
