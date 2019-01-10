def error(text):
    return '\N{NO ENTRY SIGN} {}'.format(text)


def warning(text):
    return '\N{WARNING SIGN} {}'.format(text)


def info(text):
    return '\N{INFORMATION SOURCE} {}'.format(text)


def prompt(text):
    return '\N{BLACK QUESTION MARK ORNAMENT} {}'.format(text)


def bold(text):
    return '**{}**'.format(text)


def code(text, lang=''):
    return '```{}\n{}\n```'.format(lang, text)


def code_single(text):
    return '`{}`'.format(text)


def italics(text):
    return '*{}*'.format(text)


def strikethrough(text):
    return '~~{}~~'.format(text)


def underline(text):
    return '__{}__'.format(text)


def pages(text, endl=None, *, escape=True, shorten=8, length=2000):
    """Will ignore code blocks."""
    if endl is None:
        endl = ['\n']
    input_text = text
    if escape:
        mentions = text.count('@here') + text.count('@everyone')
        shorten += mentions
    length -= shorten
    while len(input_text) > length:
        nearest_endl = max([input_text.rfind(d, 0, length)
                            for d in endl])
        nearest_endl = nearest_endl if nearest_endl != -1 else length
        if escape:
            finale = escape_mass_mentions(input_text[:nearest_endl])
        else:
            finale = input_text[:nearest_endl]
        yield finale
        input_text = input_text[nearest_endl:]

    if escape:
        yield escape_mass_mentions(input_text)
    else:
        yield input_text


def escape(text, mass_mentions=False, markdown=False):
    if mass_mentions:
        text = text.replace('@everyone', '@\u200beveryone')
        text = text.replace('@here', '@\u200bhere')
    if markdown:
        text = (
            text.replace('`', '\\`')
                .replace('*', '\\*')
                .replace('_', '\\_')
                .replace('~', '\\~'))
        return text


def escape_mass_mentions(text):
    return escape(text, mass_mentions=True)