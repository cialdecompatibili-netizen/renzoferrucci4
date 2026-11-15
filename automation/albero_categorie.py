"""Aggiunge l'albero categorie luxury (2 livelli) a _data/catalogo.json e crea le pagine
_negozio/categoria-<id>.md (IT) + en/negozio/categoria/<slug-en>.md (EN).
Idempotente: salta gli id gia' presenti, non tocca categorie e prodotti esistenti.
NON include gioielli in metalli preziosi, orologi (restrizioni dei circuiti di pagamento).
Uso: python automation/albero_categorie.py   (dalla radice della repo)
"""
import json, re, pathlib

R = pathlib.Path(__file__).resolve().parent.parent
CAT = R / "_data" / "catalogo.json"

# (id, nome IT, nome EN, genitore)  -- genitore None = reparto
ALBERO = [
    ("regali", "Regali", "Gifts", None),
    ("casa", "Casa", "Home", None),
    ("scarpe-donna", "Scarpe donna", "Shoes women", "donna"),
    ("abbigliamento-donna", "Abbigliamento donna", "Clothing women", "donna"),
    ("accessori-donna", "Accessori donna", "Accessories women", "donna"),
    ("scarpe-uomo", "Scarpe uomo", "Shoes men", "uomo"),
    ("abbigliamento-uomo", "Abbigliamento uomo", "Clothing men", "uomo"),
    ("portafogli-uomo", "Portafogli uomo", "Wallets men", "uomo"),
    ("tessili-casa", "Tessili", "Textiles", "casa"),
    ("decor-casa", "Decor", "Decor", "casa"),
    ("candele-casa", "Candele", "Candles", "casa"),
    ("regali-per-lei", "Regali per lei", "Gifts for her", "regali"),
    ("regali-per-lui", "Regali per lui", "Gifts for him", "regali"),
    ("regali-personalizzati", "Personalizzazione", "Personalisation", "regali"),
]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


d = json.loads((R / "_data" / "catalogo.json").read_text(encoding="utf-8-sig"))
gia = {c["id"] for c in d["categorie"]}
nuove = 0
for cid, it, en, gen in ALBERO:
    if cid in gia:
        continue
    c = {"nome": it, "id": cid, "icona": ""}
    if gen:
        c["genitore"] = gen
    c["tr"] = {"en": {"nome": en}}
    d["categorie"].append(c)
    nuove += 1
    # pagina IT
    (R / "_negozio" / f"categoria-{cid}.md").write_text(
        f'---\nlayout: negozio-categoria\ntitle: "{it}"\ncid: {cid}\n'
        f'permalink: /negozio/categoria/{cid}/\ndescription: "{it}"\nref: shop-cat-{cid}\n---\n',
        encoding="utf-8")
    # pagina EN
    se = slug(en)
    (R / "en" / "negozio" / "categoria" / f"{se}.md").write_text(
        f'---\nlayout: negozio-categoria\ntitle: "{en}"\ncid: {cid}\n'
        f'permalink: /en/shop/category/{se}/\ndescription: "{en}"\nlang: en\nlocale: en\nref: shop-cat-{cid}\n---\n',
        encoding="utf-8")

(R / "_data" / "catalogo.json").write_text(
    json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("categorie nuove:", nuove, "- totale:", len(d["categorie"]))
