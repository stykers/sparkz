from youtube_dl import YoutubeDL
from util import list


ytdl_npl = YoutubeDL(list.ytdl_noplaylist)
ytdl = YoutubeDL(list.ytdl_format_options)
ytdl_aria = YoutubeDL(list.ytdl_aria)
