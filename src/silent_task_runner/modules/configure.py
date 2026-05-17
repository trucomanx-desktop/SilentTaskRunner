import os
import json


def merge_defaults(config, defaults):
    """
    Faz merge recursivo entre config e defaults.

    Regras:
    - dict: adiciona chaves faltantes
    - list: faz merge item a item por índice
    - outros tipos: mantém config existente
    """

    changed = False

    # -------------------------
    # DICT
    # -------------------------
    if isinstance(defaults, dict) and isinstance(config, dict):

        for key, value in defaults.items():

            if key not in config:
                config[key] = value
                changed = True

            else:
                if merge_defaults(config[key], value):
                    changed = True

    # -------------------------
    # LIST
    # -------------------------
    elif isinstance(defaults, list) and isinstance(config, list):

        for i, default_item in enumerate(defaults):

            # adiciona itens faltantes
            if i >= len(config):
                config.append(default_item)
                changed = True

            else:
                if merge_defaults(config[i], default_item):
                    changed = True

    return changed


def verify_default_config(path, default_content=None):
    """
    Garante que o arquivo JSON exista e contenha todas as chaves
    definidas em default_content.
    Se faltar alguma chave, adiciona com valor padrão.
    """
    if default_content is None:
        default_content = {}

    # Garante que os diretórios existam
    conf_dir = os.path.dirname(path)
    if conf_dir:
        os.makedirs(conf_dir, exist_ok=True)

    config = {}

    # Se o arquivo existir, tenta carregar
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("Arquivo corrompido. Recriando com defaults.")
            config = {}
    else:
        print("Arquivo não existe. Criando com defaults.")

    # Verifica e adiciona chaves faltantes
    changed = merge_defaults(config, default_content)

    # Se arquivo não existia ou houve mudança, salva
    if not os.path.exists(path) or changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    return config


def load_config(config_path, default_content=None):
    """
    Carrega o JSON de configuração garantindo defaults.
    """
    return verify_default_config(config_path, default_content)


def save_config(path, content):
    """
    Cria o arquivo JSON no caminho especificado com conteúdo padrão,
    criando diretórios intermediários se necessário.
    """

    # Garante que os diretórios existam
    conf_dir = os.path.dirname(path)
    if conf_dir:
        os.makedirs(conf_dir, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

