import sys

from bisect import insort
from datetime import datetime

from sortedcontainers import SortedDict

import trello.api as trello
import spotify.api as spotify

from threading import Thread


def parse_discography():

    with open("discography.txt", "r") as source:
        raw_albums = source.read().splitlines()

    albums = [tuple(line.split(" ", 1)) for line in raw_albums]
    albums = [(int(year), title) for (year, title) in albums]

    discography = SortedDict()

    for (year, title) in albums:

        decade = year - year % 10

        if decade not in discography:
            discography[decade] = []

        insort(discography[decade], (year, title))

    return discography


def fetch_and_set_cover_art(album, card_id):

    cover_art_url = spotify.get_cover_art(album)

    if cover_art_url is not None:
        attachment_id = trello.create_attachment(cover_art_url, card_id)
        trello.set_card_cover(card_id, attachment_id)


if __name__ == "__main__":

    base_board_name = "Bob Dylan Discography"

    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        trello.delete_boards(base_board_name)

    discography = parse_discography()

    board_id = trello.create_board(f"{base_board_name} {datetime.now()}")

    threads = []

    for index, (decade, albums) in enumerate(discography.items()):

        list_id = trello.create_list(f"{decade}'s", board_id, index+1)

        for album in albums:

            year, title = album
            card_id = trello.create_card(f"{year} - {title}", list_id)

            t = Thread(target=fetch_and_set_cover_art, args=(album, card_id))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()
