from package.core.enums import ClientsEnum
from package.utils import get_env, key_from_value
from package.helpers.clients.claude import documents_claude, text_claude, vision_claude

current_client = key_from_value(get_env())

claude = ClientsEnum.Claude.name

text_clients = {claude: text_claude}

vision_clients = {claude: vision_claude}

documents_clients = {claude: documents_claude}