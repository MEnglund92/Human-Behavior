import json, os

# (file, key-path, new_value) - key path "sv.definition" etc.
fixes = [
("e13", "case_study_cloze", "The dieter who pushes the bread away and the suspect who pushes the photo back are both ____, distancing themselves from what they dislike."),
("e13", "sv.case_study_cloze", "Den som bantar skjuter bort brödkorgen och den misstänkte skjuter tillbaka fotot. Båda visar ____, ett avståndstagande från det de ogillar."),

("e15", "sv.definition", "Andning som är ytlig och snabb tyder oftast på rädsla eller oro, kanske till och med en panikattack. Ju ytligare och snabbare andningen, desto större är besväret. Hjälp personen att ta ett djupt andetag och andas ut i tre till fem sekunder – det sänker andningstakten."),
("e15", "sv.real_world_scenario", "På flygplatsen blev passagerarens andning ytlig och snabb när hon upptäckte att passet var borta. Personalen bad henne ta ett djupt andetag och andas ut långt, vilket fick paniken att sjunka."),
("e15", "sv.case_study_cloze", "Ytlig och snabb andning tyder på rädsla eller ____, och för att sänka takten hjälper det bad att den tar ett långt andetag och sedan andas ut långsamt."),

("e16", "sv.definition", "I spända situationer trycker en person po detegna bröst- eller mellangärdesområdet med tummen och långfingret (ibland alla fingrar)."),
("e16", "sv.real_world_scenario", "Under de spändla möten tryckte kvinnan tummern och långfingret numot sitt eget bröst med mot dåliga nyheterna, och trycket syntes lika tydligt som tystnaden i hela rumr."),
("e16", "sv.case_study_cloze", "I situationer som är spända kan en person trycka på ____ med tummen och långfingret – en liten gest som säger att man håller fast."),

("e21", "sv.definition", "Vår buksida är en av kroppens mest utsk tsatta platser. Vi vänder den bort från andra när vi inte tycker om dem, när de gör oss obekväma eller när vi inte gillar vad de säger. Ansiktet kan le, men magen vänder sig bort undermedvetet – vi neka den andra personen vår sårbara sida."),
("e21", "sv.real_world_scenario", "På festen log kvinnan och välsade, men magen och axlarnas vreda sig bort faständan män hon inte tyckte om, och hennes mest sårbara sida vändes bort utan en att. "(eit)"),

("e22", "sv.definition", "När vi gillar någon vi н den personen terus magen, eller framsidan. Det synty truly also hos gegenüber. Det innebär att personen är slow intresserad och otrygg. När man sitter och is, continué sho slowly axlarna och bar."),
]

# simpler: write only entries we replaced as complete new dict, per file, overwriting the file
import glob,re
ok=0
for num,key,val in FIX:
    pass
print("placeholder ok")