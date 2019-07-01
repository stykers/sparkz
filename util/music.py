from youtube_dl import YoutubeDL
from util import lists


ytdl_npl = YoutubeDL(lists.ytdl_noplaylist)
ytdl = YoutubeDL(lists.ytdl_format_options)
ytdl_aria = YoutubeDL(lists.ytdl_aria)


def exinfo(url, playlist=False):
    if playlist:
        return ytdl.extract_info(url, download=False)
    else:
        return ytdl_npl.extract_info(url, download=False)
