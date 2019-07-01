from util import essential

masters = essential.get("config.json").masters
version = "1.1.0"


def is_master(context):
    return context.author.id in masters
