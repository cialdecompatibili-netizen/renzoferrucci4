"""Albero categorie shop (2 livelli: reparto -> sottocategorie), ispirato ai menu dei grandi marchi
(stesso ordine in Donna e Uomo: Borse, Scarpe, Portafogli, Abbigliamento, Accessori, Occhiali, Viaggio).
Fa: sostituisce `categorie` in _data/catalogo.json, rimappa i prodotti, crea/toglie le pagine
_negozio/categoria-<id>.md (IT) e en/negozio/categoria/<slug-en>.md (EN), aggiorna il dropdown Negozio.
Esclusi di proposito gioielli in metalli preziosi e orologi (restrizioni dei circuiti di pagamento).
Idempotente. Uso: python automation/albero_categorie.py (dalla radice della repo).
"""
import json, re, pathlib

R = pathlib.Path(__file__).resolve().parent.parent
SG = ["Borse", "Scarpe", "Portafogli", "Abbigliamento", "Accessori", "Occhiali", "Viaggio"]
SG_EN = ["Bags", "Shoes", "Wallets", "Clothing", "Accessories", "Eyewear", "Travel"]
SG_ID = ["borse", "scarpe", "portafogli", "abbigliamento", "accessori", "occhiali", "viaggio"]

# (id, nome IT, nome EN, genitore)  - l'ordine qui e' l'ordine nel sito
ALBERO = []
for rid, rit, ren, suf, sufen in (("donna", "Donna", "Women", "donna", "women"), ("uomo", "Uomo", "Men", "uomo", "men")):
    ALBERO.append((rid, rit, ren, None))
    for i, n in enumerate(SG):
        ALBERO.append((f"{SG_ID[i]}-{suf}", f"{n} {suf}", f"{SG_EN[i]} {sufen}", rid))
ALBERO += [
    ("fragranze", "Fragranze", "Fragrances", None),
    ("eau-de-parfum", "Eau de parfum", "Eau de parfum", "fragranze"),
    ("set-e-ricariche", "Set e ricariche", "Sets and refills", "fragranze"),
    ("accessori-fragranze", "Accessori per profumo", "Fragrance accessories", "fragranze"),
    ("casa", "Casa", "Home", None),
    ("tessili-casa", "Tessili", "Textiles", "casa"),
    ("decor-casa", "Decor", "Decor", "casa"),
    ("candele-casa", "Candele", "Candles", "casa"),
    ("accessori-in-pelle-casa", "Accessori in pelle", "Leather accessories", "casa"),
    ("regali", "Regali", "Gifts", None),
    ("regali-per-lei", "Regali per lei", "Gifts for her", "regali"),
    ("regali-per-lui", "Regali per lui", "Gifts for him", "regali"),
    ("regali-bambini", "Bambini e nascite", "Kids and newborns", "regali"),
    ("regali-personalizzati", "Personalizzazione", "Personalisation", "regali"),
]
# prodotti gia' presenti: vecchia categoria -> nuova
MAPPA = {
    "donna": "abbigliamento-donna", "borse-a-tracolla-in-pelle": "borse-donna", "borse-in-pelle": "borse-donna",
    "portafogli-in-pelle": "portafogli-donna", "portapassaporti-in-pelle": "viaggio-donna",
    "cinture-uomo": "accessori-uomo", "zaini-in-pelle-uomo": "borse-uomo",
    "borse-a-tracolla-in-pelle-uomo": "borse-uomo", "portapassaporti-in-pelle-uomo": "viaggio-uomo",
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


cp = R / "_data" / "catalogo.json"
d = json.loads(cp.read_text(encoding="utf-8-sig"))
d["categorie"] = [
    {"nome": it, "id": cid, "icona": "", **({"genitore": g} if g else {}), "tr": {"en": {"nome": en}}}
    for cid, it, en, g in ALBERO
]
for p in d["prodotti"]:
    p["categoria"] = MAPPA.get(p.get("categoria"), p.get("categoria"))
cp.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

ids = {a[0] for a in ALBERO}
it_dir, en_dir = R / "_negozio", R / "en" / "negozio" / "categoria"
for f in list(it_dir.glob("categoria-*.md")) + list(en_dir.glob("*.md")):
    m = re.search(r"^cid:\s*(\S+)", f.read_text(encoding="utf-8"), re.M)
    if m and m.group(1) not in ids:
        f.unlink()
en_cids = {re.search(r"^cid:\s*(\S+)", x.read_text(encoding="utf-8"), re.M).group(1) for x in en_dir.glob("*.md")}
for cid, it, en, g in ALBERO:
    fi = it_dir / f"categoria-{cid}.md"
    if not fi.exists():
        fi.write_text(f'---\nlayout: negozio-categoria\ntitle: "{it}"\ncid: {cid}\n'
                      f'permalink: /negozio/categoria/{cid}/\ndescription: "{it}"\nref: shop-cat-{cid}\n---\n', encoding="utf-8")
    if cid not in en_cids:
        se = slug(en)
        (en_dir / f"{se}.md").write_text(f'---\nlayout: negozio-categoria\ntitle: "{en}"\ncid: {cid}\n'
                      f'permalink: /en/shop/category/{se}/\ndescription: "{en}"\nlang: en\nlocale: en\nref: shop-cat-{cid}\n---\n', encoding="utf-8")

# dropdown Negozio (solo reparti: le sottocategorie stanno nella pagina del reparto)
sp = R / "_data" / "sottomenu.yml"
t = sp.read_text(encoding="utf-8")
voci = "".join(f'  - title: "{it}"\n    url: /negozio/categoria/{cid}/\n' for cid, it, en, g in ALBERO if not g)
blocco = 'Negozio:\n  - title: "Tutti i prodotti"\n    url: /negozio/\n  - divider: true\n' + voci + "\n"
t = re.sub(r"(?s)^Negozio:\n.*?\n(?=Journal:)", lambda m: blocco, t, flags=re.M)
sp.write_text(t, encoding="utf-8")
print("categorie:", len(ALBERO), "- prodotti rimappati:", len(d["prodotti"]))
