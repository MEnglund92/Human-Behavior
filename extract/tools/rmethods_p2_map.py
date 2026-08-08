# -*- coding: utf-8 -*-
"""Handbook of Research Methods in Social and Personality Psychology, 3rd ed.
(Reis, West & Judd, 2024).

Chapter map with book page ranges (displayed in the app) and source PDF page
ranges (1-indexed into %TEMP%\\opencode\\rmethods_p2.txt) used by the authoring
agents. Book page = PDF page - 15 (verified per chapter).

ids: rm01..rm27 + intro handled as chapter 0? No - the Intro is included as
rm00 so every agent gets 5 slots from real content.
"""

CHAPTERS = [
    {"num": 0, "id": "rm00", "part": "Front", "title": "Introduction", "authors": "Tessa West, Harry T. Reis, and Charles M. Judd", "pages": "1-3", "pdf": (16, 18)},
    {"num": 1, "id": "rm01", "part": "Front", "title": "The Romance of Research Methods", "authors": "Mahzarin R. Banaji", "pages": "4-14", "pdf": (19, 31)},
    {"num": 2, "id": "rm02", "part": "I", "title": "Ethical Issues in Psychological Science: Studying Humans, Analyzing Data, Publishing Findings", "authors": "Chris Crandall, Roger Giner-Sorolla, and Monica Biernat", "pages": "17-43", "pdf": (32, 59)},
    {"num": 3, "id": "rm03", "part": "I", "title": "Replication in Social and Personality Psychology", "authors": "Klaus Fiedler and Florian Ermark", "pages": "45-66", "pdf": (60, 82)},
    {"num": 4, "id": "rm04", "part": "I", "title": "Realizing the Promise of Diverse and Interdisciplinary Team Science", "authors": "Stephanie J. Tepper and Neil A. Lewis Jr.", "pages": "68-83", "pdf": (83, 99)},
    {"num": 5, "id": "rm05", "part": "I", "title": "A Cross-Cultural Method in Social and Personality Psychology: The Cultural Imagination", "authors": "Shigehiro Oishi and Ayse K. Uskul", "pages": "85-113", "pdf": (100, 129)},
    {"num": 6, "id": "rm06", "part": "II", "title": "Research Design and Issues of Validity", "authors": "Marilynn B. Brewer and William D. Crano", "pages": "115-134", "pdf": (130, 150)},
    {"num": 7, "id": "rm07", "part": "II", "title": "Experimental Design", "authors": "Eliot R. Smith", "pages": "136-158", "pdf": (151, 174)},
    {"num": 8, "id": "rm08", "part": "II", "title": "Quasi-Experimental Designs", "authors": "Leandre R. Fabrigar, Thomas I. Vaughan-Johnston, and Duane T. Wegener", "pages": "160-191", "pdf": (175, 207)},
    {"num": 9, "id": "rm09", "part": "II", "title": "Field Research Methods", "authors": "Sherry Jueyu Wu and Rebecca Littman", "pages": "193-219", "pdf": (208, 235)},
    {"num": 10, "id": "rm10", "part": "III", "title": "Survey Research", "authors": "Kristen Olson", "pages": "221-242", "pdf": (236, 258)},
    {"num": 11, "id": "rm11", "part": "III", "title": "Conducting Surveys and Experiments on the Internet", "authors": "Chadly Stern and Jordan R. Axt", "pages": "244-264", "pdf": (259, 280)},
    {"num": 12, "id": "rm12", "part": "III", "title": "Methods for Studying Everyday Experience in Its Natural Context", "authors": "Harry T. Reis, Laura Sels, and Shelly L. Gable", "pages": "266-295", "pdf": (281, 311)},
    {"num": 13, "id": "rm13", "part": "III", "title": "Mobile Sensing Methods", "authors": "Ramona Schoedel and Matthias R. Mehl", "pages": "297-320", "pdf": (312, 336)},
    {"num": 14, "id": "rm14", "part": "III", "title": "Language Research in Social Personality Psychology", "authors": "Molly E. Ireland and James W. Pennebaker", "pages": "322-347", "pdf": (337, 363)},
    {"num": 15, "id": "rm15", "part": "III", "title": "Collecting Digital Footprints in the Wild", "authors": "Michal Kosinski", "pages": "349-376", "pdf": (364, 392)},
    {"num": 16, "id": "rm16", "part": "III", "title": "Behavioral Observation and Coding", "authors": "Katherine R. Thorson and Tessa West", "pages": "378-402", "pdf": (393, 418)},
    {"num": 17, "id": "rm17", "part": "III", "title": "Automaticity and Implicit Measures", "authors": "Bertram Gawronski", "pages": "404-425", "pdf": (419, 441)},
    {"num": 18, "id": "rm18", "part": "III", "title": "Social Neuroendocrinology", "authors": "Wendy Berry Mendes", "pages": "427-451", "pdf": (442, 467)},
    {"num": 19, "id": "rm19", "part": "III", "title": "Multivariate Neuroimaging in Social and Personality Psychology", "authors": "Robert S. Chavez, William A. Cunningham, and Elliot T. Berkman", "pages": "453-469", "pdf": (468, 485)},
    {"num": 20, "id": "rm20", "part": "IV", "title": "Measurement: Reliability, Construct Validation, and Scale Construction", "authors": "William Revelle and Kayla M. Garner", "pages": "471-500", "pdf": (486, 516)},
    {"num": 21, "id": "rm21", "part": "IV", "title": "Advanced Psychometrics", "authors": "Patrick E. Shrout and Mao Mogami", "pages": "502-530", "pdf": (517, 546)},
    {"num": 22, "id": "rm22", "part": "IV", "title": "Dealing with Repeated Measures: Design Decisions and Analytic Strategies for Over-Time Data", "authors": "Amie M. Gordon and Katherine R. Thorson", "pages": "532-563", "pdf": (547, 579)},
    {"num": 23, "id": "rm23", "part": "IV", "title": "The Design and Analysis of Data from Dyads and Groups", "authors": "David A. Kenny, Robert A. Ackerman, and Deborah A. Kashy", "pages": "565-600", "pdf": (580, 616)},
    {"num": 24, "id": "rm24", "part": "IV", "title": "Random Factors and Research Generalization", "authors": "Charles M. Judd and David A. Kenny", "pages": "602-620", "pdf": (617, 636)},
    {"num": 25, "id": "rm25", "part": "IV", "title": "Combining Statistical and Causal Mediation Analysis", "authors": "Amanda Kay Montoya", "pages": "622-651", "pdf": (637, 667)},
    {"num": 26, "id": "rm26", "part": "IV", "title": "Mathematical and Computational Models", "authors": "Karl Christoph Klauer", "pages": "653-676", "pdf": (668, 692)},
    {"num": 27, "id": "rm27", "part": "IV", "title": "Meta-analysis", "authors": "Judith A. Hall and David Miller", "pages": "678-703", "pdf": (693, 719)},
]
