from util import essential

masters = essential.get("config.json").masters


def is_master(ctx):
    return ctx.author.id in masters