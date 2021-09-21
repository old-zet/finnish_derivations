# finnish_derivations
This project is a part of my 2020 comparative study between morphological properties of French and Finnish available in French (DOI: 10.13140/RG.2.2.18236.05768/1):
https://www.researchgate.net/publication/348191805_Possibilites_derivationnelles_selon_le_type_de_la_langue

Its code executes the following steps:
1) Find morphological patterns between nouns and verbs in the Finnish language via Kotus' XML corpus (cf. https://kaino.kotus.fi/sanat/nykysuomi/ which was EDA'd beforehand), 
2) Log them in TXTs by 12 to 5 common characters,
3) Clean the original corpus from such derivations leaving only the nouns that cannot be derived into verbs, and vice versa, i.e. sterile lexical units for further analysis as for why they are morphologically unaccessible in an agglutinative language like Finnish.
