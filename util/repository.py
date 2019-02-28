from .essential import get

masters = get("config.json").masters


def is_master(ctx):
    return ctx.author.id in masters