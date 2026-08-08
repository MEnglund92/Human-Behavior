# -*- coding: utf-8 -*-
"""Snoop: What Your Stuff Says About You (Gosling, 2008).

Chapter map with book page ranges (displayed in the app) and source PDF page
ranges (1-indexed into %TEMP%\\opencode\\snoop_p2.txt) used by the authoring
agents. Book page = PDF page - 12 (verified per chapter).
"""

CHAPTERS = [
    {"num": 1, "id": "snoop01", "title": "Prologue: The Arrival of the Mystery Box", "pages": "1-8", "pdf": (15, 20)},
    {"num": 2, "id": "snoop02", "title": "Less Than Zero Acquaintance", "pages": "9-32", "pdf": (21, 44)},
    {"num": 3, "id": "snoop03", "title": "OCEAN's Five", "pages": "33-54", "pdf": (45, 66)},
    {"num": 4, "id": "snoop04", "title": "Getting to Know You", "pages": "55-74", "pdf": (67, 86)},
    {"num": 5, "id": "snoop05", "title": "Belgian Sleuths and Scandinavian Seabirds", "pages": "75-86", "pdf": (87, 100)},
    {"num": 6, "id": "snoop06", "title": "Jumpers, Bumpers, Groovers, and Shakers", "pages": "87-112", "pdf": (101, 124)},
    {"num": 7, "id": "snoop07", "title": "Space Doctoring", "pages": "113-136", "pdf": (125, 150)},
    {"num": 8, "id": "snoop08", "title": "In Defense of Stereotypes", "pages": "137-166", "pdf": (151, 180)},
    {"num": 9, "id": "snoop09", "title": "When Good Judgments Go Bad", "pages": "167-186", "pdf": (181, 200)},
    {"num": 10, "id": "snoop10", "title": "Like a Super Snooper", "pages": "187-202", "pdf": (201, 216)},
    {"num": 11, "id": "snoop11", "title": "An Office and a Gentleman", "pages": "203-218", "pdf": (217, 230)},
    {"num": 12, "id": "snoop12", "title": "Bringing It Home", "pages": "219-228", "pdf": (231, 240)},
]
