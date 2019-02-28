from util import essential

masters = essential.get("config.json").masters
version = "1.0.0-ALPHA"


def is_master(ctx):
    return ctx.author.id in masters