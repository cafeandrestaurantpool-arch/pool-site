#!/usr/bin/env python3
"""最終チェック: python3 tools/check_site.py  （site/ を調べる）
リンク切れ・画像切れ・アンカー切れ、SEOタグ、h1、alt、JSON-LD、重複、禁止語（SAMPLE・要確認・ぐるなび 等）を確認する。"""
import json, os, re, sys, html
from html.parser import HTMLParser
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); SITE = os.path.join(ROOT, "site")
URL = json.load(open(os.path.join(ROOT, "src", "site.json")))["url"].rstrip("/")
NG = ["SAMPLE", "要確認", "ぐるなび", "gnavi", "050-5487", "0505487", "{{", "NEWS_LIST", "lorem"]
errs, warns = [], []

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links = []; s.ids = set(); s.h1 = 0; s.imgs = []; s.meta = {}; s.title = ""; s.in_title = False; s.canon = None; s.ld = []; s.in_ld = False; s.text = []; s.lang = None; s.skip = 0
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if t == "html": s.lang = a.get("lang")
        if t == "a" and a.get("href") is not None: s.links.append(("a", a["href"], a.get("target"), a.get("rel")))
        if t == "img": s.imgs.append(a); s.links.append(("img", a.get("src", ""), None, None))
        if t == "script" and a.get("src"): s.links.append(("script", a["src"], None, None))
        if t == "script" and a.get("type") == "application/ld+json": s.in_ld = True
        if t == "script" or t == "style": s.skip += 1
        if t == "h1": s.h1 += 1
        if t == "meta":
            k = a.get("name") or a.get("property")
            if k: s.meta[k] = a.get("content", "")
        if t == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if t == "title": s.in_title = True
    def handle_endtag(s, t):
        if t == "title": s.in_title = False
        if t == "script": s.in_ld = False
        if t in ("script", "style"): s.skip = max(0, s.skip - 1)
    def handle_data(s, d):
        if s.in_title: s.title += d
        elif s.in_ld: s.ld.append(d)
        elif not s.skip: s.text.append(d)

def local(path, href):
    h = href.split("#")[0].split("?")[0]
    if not h: return path
    base = os.path.join(SITE, h.lstrip("/")) if h.startswith("/") else os.path.join(os.path.dirname(path), h)
    if os.path.isdir(base): base = os.path.join(base, "index.html")
    return os.path.normpath(base)

pages = [os.path.join(r, f) for r, _, fs in os.walk(SITE) for f in fs if f.endswith(".html")]
ext = {}
parsed = {}
for pg in sorted(pages):
    rel = "/" + os.path.relpath(pg, SITE).replace(os.sep, "/")
    raw = open(pg, encoding="utf-8").read(); p = P(); p.feed(raw); parsed[pg] = p
    def E(m): errs.append(f"{rel}: {m}")
    def W(m): warns.append(f"{rel}: {m}")
    if not raw.lower().startswith("<!doctype html>"): E("doctype がない")
    if p.lang != "ja": E("html lang=ja がない")
    if not (10 <= len(p.title.strip()) <= 70): W(f"title の長さ {len(p.title.strip())}字（目安 10〜70）: {p.title.strip()}")
    d = p.meta.get("description", "")
    if not d: E("meta description がない")
    elif not (50 <= len(d) <= 130): W(f"description の長さ {len(d)}字（目安 50〜130）")
    exp = URL + (rel[:-10] if rel.endswith("/index.html") else rel)
    if p.canon != exp: E(f"canonical が違う: {p.canon} （正: {exp}）")
    for k in ("og:title", "og:description", "og:image", "og:url", "og:type", "twitter:card", "viewport", "robots"):
        if not p.meta.get(k): E(f"{k} がない")
    if p.h1 != 1: E(f"h1 が {p.h1} 個（1個にする）")
    if rel != "/index.html":
        for a in p.imgs:
            if not a.get("alt", "").strip() and a.get("src", "").startswith(("/img/", "/news/", "img/")): E(f"img の alt が空: {a.get('src')}")
    for a in p.imgs:
        if "alt" not in a: E(f"img に alt がない: {a.get('src')}")
        if not a.get("src"): E("img に src がない")
    for x in p.ld:
        try: json.loads(x)
        except Exception as ex: E(f"JSON-LD が壊れている: {ex}")
    if not p.ld: W("JSON-LD がない")
    txt = html.unescape("".join(p.text))
    for w in NG:
        if w in raw: E(f"禁止語が残っている: {w}")
    for kind, h, tg, rl in p.links:
        if not h: E(f"空のリンク/src（{kind}）"); continue
        if h.startswith(("tel:", "mailto:", "javascript:")): continue
        if h.startswith(("http://", "https://")):
            ext.setdefault(h, []).append(rel)
            if tg == "_blank" and "noopener" not in (rl or ""): W(f"target=_blank に noopener がない: {h}")
            continue
        if h.startswith("#"):
            continue
        t = local(pg, h)
        if not os.path.exists(t): E(f"リンク切れ({kind}): {h}")
for pg, p in parsed.items():
    rel = "/" + os.path.relpath(pg, SITE).replace(os.sep, "/")
    for kind, h, *_ in p.links:
        if h.startswith("#") and len(h) > 1:
            if h[1:] not in p.ids: errs.append(f"{rel}: アンカー切れ {h}")
        elif "#" in h and not h.startswith(("http", "tel")):
            t = local(pg, h); a = h.split("#")[1]
            if t in parsed and a and a not in parsed[t].ids: errs.append(f"{rel}: アンカー切れ {h}")
# 画像ファイルの存在・サイズ
for r, _, fs in os.walk(os.path.join(SITE, "img")):
    for f in fs:
        sz = os.path.getsize(os.path.join(r, f))
        if sz > 1_500_000: warns.append(f"画像が重い: img/{f} {sz//1024}KB")
for f in ("sitemap.xml", "robots.txt"):
    if not os.path.exists(os.path.join(SITE, f)): errs.append(f"{f} がない")
sm = open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()
for pg in pages:
    rel = "/" + os.path.relpath(pg, SITE).replace(os.sep, "/"); u = URL + (rel[:-10] if rel.endswith("/index.html") else rel)
    if u not in sm: errs.append(f"sitemap に載っていない: {u}")
print("ページ数:", len(pages)); print("外部リンク:"); [print("  ", k, "←", ",".join(sorted(set(v)))) for k, v in sorted(ext.items())]
print("\\n警告:", len(warns)); [print("  W", w) for w in warns]
print("エラー:", len(errs)); [print("  E", x) for x in errs]
sys.exit(1 if errs else 0)
