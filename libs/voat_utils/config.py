import json


def get_config():
    with open('/etc/voat/config/config.json', 'r') as cfg:
        return json.load(cfg)


def write_value(key, value):

    config = get_config()

    config[key] = value

    with open('/etc/voat/config/config.json', 'w') as cfg:
        cfg.write(json.dumps(config))

