from getpass import getpass


def getpass_keys(name="API_KEY_CLAUDE_ANTHROPIC"):
    key = getpass(name)
    print(key)
