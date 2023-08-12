from movie.handler import movie_callback, movie_link, characters_page_callback
from movie.command import movie_search
from tmdb_handler import tmdb_search

from tv.command import tv_search
from tv.handler import tv_season, tv_servers, tv_episodes


routes = [
    {
        "func": movie_callback,
        "path": "movie_"
    },
    # {
    #     "func": movie_server_links,
    #     "path": "m_links_"
    # },
    {
        "func": movie_link,
        "path": "mserver_"
    },
    {
        "func": characters_page_callback,
        "path": "action_"
    },
    {
        "func": tv_season,
        "path": "tv_"
    },
    {
        "func": tv_servers,
        "path": "season_"
    },
    {
        "func": tv_episodes,
        "path": "tserver_"
    },
]


commands = [
    {
        "command": "tmdb",
        "func": tmdb_search
    },
    {
        "command": "movie",
        "func": movie_search
    },
    {
        "command": "tv",
        "func": tv_search
    }
]
