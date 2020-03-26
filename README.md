# wyeworks-interview-exercise

This app reads a `discography.txt` file containing data about Bob Dylan's Discography, searches for the albums' cover arts in Spotify and creates a board in Trello in which the discography is organized.

---

Create trello/credentials.json and set the properties `TRELLO_CLIENT_ID` and `RELLO_ACCESS_TOKEN`

**Server Token**

https://developers.trello.com/page/authorization

---

Create spotify/credentials.json and set the properties `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`

**Client Credentials Flow**

https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow

---

Execute `python3 main.py` in root folder.
Optional argument `-d` deletes previously generated boards (with "Bob Dylan Discography" in their name) before creating the new one.
