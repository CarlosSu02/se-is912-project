# functions for claude client: vision, documents and text

from anthropic import Anthropic
from package.utils.handle_dotenv import get_env, clients

API_KEY_CLAUDE = get_env(clients["Claude"])
MODEL_SONNET = "claude-3-5-sonnet-20241022"
MODEL_OPUS = "claude-3-opus-20240229"

# client = Anthropic(api_key=API_KEY_CLAUDE)

# print(client)


def get_client():
    return Anthropic(api_key=API_KEY_CLAUDE)


def vision_claude(image_media_type, base64_string):
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


def documents_claude(base64_string):
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
                        "media_type": "application/pdf",
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
