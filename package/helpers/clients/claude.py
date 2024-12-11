# functions for claude client: vision, documents and text
import asyncio
from stringprep import b1_set

from anthropic import Anthropic
from package.utils import get_env
from package.core.constants import clients

API_KEY_CLAUDE = get_env(clients["Claude"])
MODEL_SONNET = "claude-3-5-sonnet-20241022"
MODEL_OPUS = "claude-3-opus-20240229"

text = """
# Historia de Python

Python fue creado a finales de los años 80 por Guido van Rossum, un programador holandés que trabajaba en el Centro para las Matemáticas y la Informática (CWI) en los Países Bajos. Van Rossum buscaba crear un lenguaje de programación que fuera fácil de leer, escribir y mantener.

## Orígenes y desarrollo inicial

- En diciembre de 1989, Van Rossum comenzó a trabajar en Python como un sucesor del lenguaje de programación ABC, en el que había estado involucrado anteriormente.
- El nombre "Python" fue inspirado por el amor de Van Rossum por la comedia británica "Monty Python's Flying Circus".
- La primera versión pública de Python, la versión 0.9.0, fue lanzada en febrero de 1991.

## Evolución y versiones principales

- Python 2.0, lanzado en octubre de 2000, introdujo características como listas por comprensión, recolección de basura para la gestión de memoria y compatibilidad con Unicode.
- Python 3.0, una versión importante que no es completamente compatible con versiones anteriores, se lanzó en diciembre de 2008. Esta versión tiene como objetivo eliminar duplicidad y complejidad del lenguaje.
- Actualmente, Python se encuentra en la versión 3.9.x, lanzada en octubre de 2020, y continúa evolucionando con nuevas características y mejoras.

## Filosofía y principios de diseño

Python se adhiere a una filosofía de diseño conocida como "El Zen de Python", que enfatiza la legibilidad, simplicidad y claridad del código. Algunos de los principios clave son:

- La legibilidad cuenta.
- Explícito es mejor que implícito.
- Simple es mejor que complejo.
- Complejo es mejor que complicado.
- La practicidad le gana a la pureza.

## Adopción y popularidad

- Python ha ganado popularidad en una amplia gama de dominios, incluyendo desarrollo web, ciencia de datos, aprendizaje automático, scripting y automatización.
- Su sintaxis clara y legible, junto con una extensa biblioteca estándar y un rico ecosistema de paquetes de terceros, han contribuido a su adopción generalizada.
- Python es consistentemente clasificado como uno de los lenguajes de programación más populares en encuestas y rankings de la industria.

## Comunidad y gobierno

- Python tiene una comunidad activa y diversa de desarrolladores que contribuyen al lenguaje, crean paquetes y promueven su uso.
- La Python Software Foundation (PSF), una organización sin fines de lucro, se encarga del desarrollo y promoción del lenguaje.
- El desarrollo de Python sigue un modelo de gobierno basado en la comunidad, con discusiones y decisiones tomadas a través de listas de correo y PEPs (Propuestas de Mejora de Python).

Python ha recorrido un largo camino desde sus humildes comienzos hace más de tres décadas. Hoy en día, es un lenguaje de programación maduro y versátil, utilizado por desarrolladores, científicos y educadores de todo el mundo. Con su enfoque en la legibilidad y la simplicidad, Python continúa atrayendo a nuevos programadores y siendo una herramienta valiosa para los profesionales experimentados.
"""


def get_client_claude():
    return Anthropic(api_key=API_KEY_CLAUDE)


async def vision_claude(image_media_type, base64_string):
    # print(image_media_type)
    # print(base64_string)
    # return "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    # await asyncio.sleep(5)
    return text

    client = get_client_claude()

    max_tokens = 1024

    messages = [
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
                {"type": "text", "text": "Describe la imagen, en español, respuesta en formato markdown"},
            ],
        }
    ]

    completion = await get_completion_claude(client, max_tokens, messages, MODEL_OPUS)

    return completion


async def documents_claude(document_media_type, base64_string):
    return text
    client = Anthropic(
        default_headers={"anthropic-beta": "pdfs-2024-09-25"},
        api_key=API_KEY_CLAUDE
    )

    max_tokens = 2048

    prompt = """
    Asume el rol de un experto en la elaboración de resúmenes claros, precisos y bien estructurados de documentos de cualquier tipo, como informes, ensayos, investigaciones académicas, contratos o libros. Eres capaz de identificar las ideas principales, sintetizar información relevante y destacar conclusiones clave sin perder detalles importantes. Adapta el nivel de detalle y el lenguaje según las necesidades del usuario, ya sea un resumen ejecutivo, un análisis académico o un extracto simplificado para fines generales. Responde de manera concisa, ordenada y profesional. Respuesta en formato de markdown.
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

    completion = await get_completion_claude(client, max_tokens, messages, MODEL_SONNET)

    return completion


async def text_claude(prompt, text):
    return text
    client = get_client_claude()

    max_tokens = 1024

    messages = [
        {"role": "user", "content": text},
        {"role": "user", "content": prompt},
        {"role": "user", "content": "Respuesta en formato de markdown."}
    ]

    completion = await get_completion_claude(client, max_tokens, messages, MODEL_OPUS)

    return completion


# async def get_completion(client, tokens, messages, model_name):
#     res = await client.messages.create(model=model_name, max_tokens=tokens, messages=messages)
#     print(res)
#     return res.content[0].text
# return (
#     client.messages.create(model=model_name, max_tokens=tokens, messages=messages)
#     .content[0]
#     .text
# )

async def get_completion_claude(client, max_tokens, messages, model_name):
    res = await asyncio.to_thread(
        client.messages.create,
        model=model_name,
        max_tokens=max_tokens,
        messages=messages
    )
    print(res)
    return res.content[0].text


def get_completion_stream_claude(client, max_tokens, messages, model_name):
    return client.messages.stream(model=model_name, max_tokens=100, messages=messages)