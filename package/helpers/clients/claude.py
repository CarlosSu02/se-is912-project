# functions for claude client: vision, documents and text

from anthropic import Anthropic
from package.utils.handle_dotenv import get_env, clients

API_KEY_CLAUDE = get_env(clients["Claude"])
MODEL_SONNET = "claude-3-5-sonnet-20241022"
MODEL_OPUS = "claude-3-opus-20240229"

text = """
        Basado en el documento presentado, elaboraré un resumen estructurado sobre los Sistemas Expertos:

        DEFINICIÓN Y CONCEPTO
        - Los sistemas expertos son programas que reproducen el proceso intelectual de expertos humanos en campos específicos.
        - Son capaces de mejorar la productividad, ahorrar tiempo y dinero, conservar conocimientos valiosos y facilitar su difusión.

        CARACTERÍSTICAS PRINCIPALES
        1. Base de Conocimiento:
        - Almacena información especializada y estructurada
        - Contiene reglas y experiencias de expertos humanos

        2. Motor de Inferencia:
        - Procesa la información usando reglas predefinidas
        - Genera conclusiones y recomendaciones

        3. Interfaz de Comunicación:
        - Permite la interacción entre usuario y sistema
        - Explica el razonamiento seguido para llegar a conclusiones

        VENTAJAS
        - Rapidez en procesamiento de información
        - Disponibilidad permanente
        - Decisiones más objetivas y consistentes
        - Conservación del conocimiento experto
        - Capacidad de manejar información compleja
    """


def get_client():
    return Anthropic(api_key=API_KEY_CLAUDE)


def vision_claude(image_media_type, base64_string):
    # print(image_media_type)
    # return "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    return text

    client = get_client()

    max_tokens = 1024

    messages = (
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": base64_string,
                        },
                    },
                    {"type": "text", "text": "Describe la imagen, en español"},
                ],
            }
        ],
    )

    completion = get_completion(client, max_tokens, messages, MODEL_OPUS)

    return completion


def documents_claude(document_media_type, base64_string):
    return text
    client = Anthropic(
        default_headers={"anthropic-beta": "pdfs-2024-09-25"},
        api_key="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",
    )

    max_tokens = 2048

    prompt = """
    Asume el rol de un experto en la elaboración de resúmenes claros, precisos y bien estructurados de documentos de cualquier tipo, como informes, ensayos, investigaciones académicas, contratos o libros. Eres capaz de identificar las ideas principales, sintetizar información relevante y destacar conclusiones clave sin perder detalles importantes. Adapta el nivel de detalle y el lenguaje según las necesidades del usuario, ya sea un resumen ejecutivo, un análisis académico o un extracto simplificado para fines generales. Responde de manera concisa, ordenada y profesional.
    """

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": document_media_type,
                        "data": base64_string,
                    },
                },
                {"type": "text", "text": prompt},
            ],
        }
    ]

    completion = get_completion(client, max_tokens, messages, MODEL_SONNET)

    return completion


def text_claude(prompt, text):
    return text
    client = get_client()

    max_tokens = 1024

    messages = [
        {"role": "user", "content": text},
        {"type": "text", "text": prompt},
    ]

    completion = get_completion(client, max_tokens, messages, MODEL_OPUS)

    return completion


def get_completion(client, tokens, messages, model_name):
    return (
        client.messages.create(model=model_name, max_tokens=tokens, messages=messages)
        .content[0]
        .text
    )
