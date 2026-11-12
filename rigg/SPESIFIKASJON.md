# Dashman-rigg: animert Dashman i videoer

Mål: Dashman kan stå nede i høyre hjørne i videoene (der læreren ellers står foran grønnskjermen) og snakke med
lærerens stemme. Læreren spiller bare inn lyd; Claude lager leppesynk, blunking og poser.

## Det læreren tegner (én gang, på iPad, hver del på eget lag eller egen side, eksport som PDF)

- **Kropp i 6–8 poser** (uten hode): nøytral, peker mot tavla (til venstre), peker opp, begge armer opp («ta-da!»),
  tenker (hånd på haka), trekker på skuldrene, overrasket, skriver/holder noe.
- **Hode** uten øyne og munn (rett fram, og gjerne litt mot venstre).
- **Munner (5–6):** lukket (m/b/p), litt åpen, vid «a», rund «o», bred «i/e», «f/v» (tenner på leppa).
- **Øyne:** åpne, lukket (blunk), ser til venstre, ser opp.
- **Ekstra:** svettedråpe, spørsmålstegn, lyspære, «!».

Tegn alt i samme størrelse og med samme ankerpunkt (f.eks. et lite kryss i halsen på alle deler), så delene passer sammen.

## Det Claude gjør

- Tale til tekst (ordtider) → munnform per lyd; blunk med tilfeldige mellomrom; lett pust/vipp.
- Poser styres av manuset: `[Dashman: peker]`, `[Dashman: tenker]` osv., eller av **[Du: …]**-linjene.
- Dashman ser mot det på tavla som snakkes om, og kan gå bort til tavla.

## Status (12. november 2026)

Læreren har tegnet riggen: `dashman_rigg.pdf` (11 sider). Delene er klippet ut som PNG med gjennomsiktig bakgrunn i `deler/`
(hvite streker, merkelappene tatt bort):

- **Poser:** `noytral`, `noytral_kopp`, `peker_tavla` (peker mot høyre – speilvendes når Dashman står nede til høyre),
  `peker_opp`, `armer_opp`, `tada`, `undrende`, `mystisk` (hånd på haka), `lattermild`, `hoho`, `hoho_x` (latter),
  `skuldre`, `gruble`, `overrasket`, `skrive`, `skrive_ferdig`.
- **Deler:** `hode`, `oyne_aapne`, `oyne_lukket_v/h`, `oyne_venstre`, `munn_lukket`, `munn_o`, `munn_aapen`, `munn_smil_tenner`, `munn_tunge`.
- **Ekstra:** `kopp` (med grønn R), `penn`, `ark`, `lyspaere`, `svette_a/b`, `spm`, `utrop`, `utrop_spm`.

`rigg.json` sier hvor øynene og munnen er i hver positur (bokser og strekkomponenter, funnet med `finn_ansikt.py`
og rettet for hånd). Poser uten munn (hånd foran munnen, latter) brukes som de er.

`eksempel_test.py` lager en test på 11 s: munnform fra lyden (stille → lukket, mørk lyd → «o», middels → åpen,
lys → smil med tenner), blunk, pust/vipp, et lite hopp ved ny positur, og poser fra en liste med tider.
