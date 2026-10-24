#!/usr/bin/env python3
"""POOL site generator. usage: python3 tools/make_site.py  (run from the repo root)

src/base/        トップ・固定ページ・画像のもと（ふだんは触らない）
src/posts/YYYY-MM-DD[-n]/post.md   NEWS記事（写真は同じフォルダに入れる）
site/            出力（Netlifyはこのフォルダをそのまま公開する）
"""
import datetime as dt, html, os, re, shutil, sys
from PIL import Image, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC, BASE, OUT = [os.path.join(ROOT, p) for p in ("src/posts", "src/base", "site")]
e = html.escape

import json
sys.path.insert(0, os.path.dirname(__file__))
import langs
SITE = json.load(open(os.path.join(ROOT, "src", "site.json"), encoding="utf-8"))
URL = SITE["url"].rstrip("/")
NAME = "CAFE & RESTAURANT POOL（カフェ＆レストラン プール）"
IG = "https://www.instagram.com/cafeandrestaurant_pool/"


def og_image(src, dst):
    """1200x630。写真は切らずに全体を入れ、余った所は紺色にする。"""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    c = Image.new("RGB", (1200, 630), (4, 72, 108))
    s = min(1200 / im.width, 630 / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    c.paste(im, ((1200 - im.width) // 2, (630 - im.height) // 2))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    c.save(dst, "JPEG", quality=86, optimize=True)


def ld(o):
    return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "</script>"


def finalize(frag, title, desc, path, og, lds=(), kind="website"):
    """断片HTML → 完全なHTML。SEOタグ（title/description/canonical/OGP/Twitter/JSON-LD）を入れる。"""
    f = re.sub(r"<!doctype html>|</?html[^>]*>|</?head>|<meta charset[^>]*>|<meta name=\"viewport\"[^>]*>|<meta name=\"claude:viewport-fit-sides\"[^>]*>|<meta name=\"description\"[^>]*>", "", frag, flags=re.I)
    f = re.sub(r"<title>.*?</title>", "", f, flags=re.S)
    i = f.index("</style>") + len("</style>")
    keep, body = f[:i], f[i:].replace("</body>", "")
    url = URL + path
    t, d = e(title), e(desc)
    head = ('<!doctype html><html lang="ja"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f"<title>{t}</title><meta name=\"description\" content=\"{d}\">"
            f'<link rel="canonical" href="{url}">'
            '<meta name="robots" content="index,follow,max-image-preview:large">'
            '<meta name="theme-color" content="#04486c">'
            '<link rel="icon" href="/img/logo-d.png">'
            f'<meta property="og:type" content="{kind}"><meta property="og:site_name" content="CAFE &amp; RESTAURANT POOL">'
            f'<meta property="og:locale" content="ja_JP"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
            f'<meta property="og:url" content="{url}"><meta property="og:image" content="{URL}{og}">'
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{URL}{og}">'
            + "".join(ld(x) for x in lds) + keep + "</head><body>")
    return head + body + "</body></html>"


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": URL + u} for i, (n, u) in enumerate(items)]}


RESTAURANT = {"@context": "https://schema.org", "@type": "Restaurant", "name": "CAFE & RESTAURANT POOL", "alternateName": "カフェ＆レストラン プール",
    "url": URL + "/", "image": [URL + "/og/top.jpg"], "telephone": "+81-742-42-6430", "servesCuisine": ["フレンチ", "カフェ", "ワイン"],
    "address": {"@type": "PostalAddress", "postalCode": "630-8258", "addressRegion": "奈良県", "addressLocality": "奈良市", "streetAddress": "船橋町7", "addressCountry": "JP"},
    "geo": {"@type": "GeoCoordinates", "latitude": 34.6881509, "longitude": 135.8217667},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "11:30", "closes": "15:00"},
                                  {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "18:00", "closes": "22:00"}],
    "acceptsReservations": True, "sameAs": [IG], "hasMap": "https://www.google.com/maps/search/?api=1&query=34.6881509,135.8217667&query_place_id=ChIJYbS7iPQ7AWARTCyDlQkKDoo"}
TOP_TITLE = "奈良・船橋町のカフェ＆レストラン POOL｜ランチ・ディナー・ナチュラルワイン"
TOP_DESC = "奈良市船橋町の古い建物を生かしたカフェ＆レストランPOOL。旬の奈良野菜を使ったカジュアルフレンチとナチュラルワインを、ランチ・ディナーで。近鉄奈良駅から徒歩9分。ご予約はお電話またはDMで。"


def parse(path, slug):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    head, _, body = raw.partition("\n---\n")
    meta = {}
    for line in head.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    if not meta.get("title"):
        sys.exit(f"[{slug}] title がありません")
    try:
        d = dt.date.fromisoformat(meta.get("date") or slug[:10])
    except ValueError:
        sys.exit(f"[{slug}] date は 2026-10-24 の形で書いてください")
    return meta, body.strip(), d


def prep(src, dst, maxw=2400):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "JPEG", quality=88, optimize=True, progressive=True)
    return im.size


def find(sd, fn):
    p = os.path.join(sd, fn)
    if os.path.isfile(p):
        return p
    sys.exit(f"写真が見つかりません: {fn}（{sd}）")


def md(body, slug, sd):
    out, para, lst = [], [], []

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + "<br>".join(e(x) for x in para) + "</p>"); para = []
        if lst:
            out.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in lst) + "</ul>"); lst = []

    for line in body.split("\n"):
        s = line.strip()
        m = re.match(r"!\[(.*?)\]\((.+?)\)", s)
        if not s:
            flush()
        elif s.startswith("## "):
            flush(); out.append(f"<h2>{e(s[3:])}</h2>")
        elif m:
            flush()
            alt, fn = m.groups()
            name = re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.splitext(fn)[0]) + ".jpg"
            w, h = prep(find(sd, fn), os.path.join(OUT, "news", slug, name))
            out.append(f'<figure><img src="/news/{slug}/{name}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy">'
                       + (f"<figcaption>{e(alt)}</figcaption>" if alt else "") + "</figure>")
        elif s.startswith("- "):
            if para: flush()
            lst.append(s[2:])
        else:
            if lst: flush()
            para.append(s)
    flush()
    return "\n".join(out)


def plain(body):
    t = re.sub(r"!\[.*?\]\(.*?\)", "", body)
    t = re.sub(r"^## |^- ", "", t, flags=re.M)
    return re.sub(r"\s+", "", t)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(BASE, "img"), os.path.join(OUT, "img"))
    tpl = open(os.path.join(BASE, "page.template.html"), encoding="utf-8").read()
    img = lambda n: os.path.join(BASE, "img", n)
    og_image(img("n_room.jpg"), os.path.join(OUT, "og", "top.jpg"))
    og_image(img("chef-clean.jpg"), os.path.join(OUT, "og", "message.jpg"))
    posts = []
    for slug in sorted(os.listdir(SRC)) if os.path.isdir(SRC) else []:
        sd = os.path.join(SRC, slug)
        if not os.path.isfile(os.path.join(sd, "post.md")):
            continue
        meta, body, d = parse(os.path.join(sd, "post.md"), slug)
        cover, cw = meta.get("photo"), None
        if cover:
            cw = prep(find(sd, cover), os.path.join(OUT, "news", slug, "cover.jpg"))
            og_image(os.path.join(OUT, "news", slug, "cover.jpg"), os.path.join(OUT, "og", slug + ".jpg"))
        posts.append(dict(slug=slug, meta=meta, body=body, d=d, sd=sd, cover=bool(cover), cw=cw, tag=meta.get("tag", "NEWS")))
    posts.sort(key=lambda p: (p["d"], p["slug"]), reverse=True)
    for i, p in enumerate(posts):
        txt = plain(p["body"])
        p["excerpt"] = txt[:60] + ("…" if len(txt) > 60 else "")
        p["desc"] = p["meta"].get("description") or (txt[:110] + ("…" if len(txt) > 110 else ""))
        art = md(p["body"], p["slug"], p["sd"])
        ds = p["d"].strftime("%Y.%m.%d")
        alt = p["meta"].get("alt", p["meta"]["title"])
        cov = f'<div class="cover"><img src="/news/{p["slug"]}/cover.jpg" alt="{e(alt)}" width="{p["cw"][0]}" height="{p["cw"][1]}"></div>' if p["cover"] else ""
        prev_ = posts[i + 1] if i + 1 < len(posts) else None
        next_ = posts[i - 1] if i > 0 else None
        pn = '<div class="pn"><span>' + (f'<a href="/news/{prev_["slug"]}/">← {e(prev_["meta"]["title"])}</a>' if prev_ else "") + '</span><span>' + (f'<a href="/news/{next_["slug"]}/">{e(next_["meta"]["title"])} →</a>' if next_ else "") + "</span></div>"
        cta = ('<div class="go"><a class="f" href="https://ig.me/m/cafeandrestaurant_pool" target="_blank" rel="noopener">DMで予約</a>'
               '<a href="tel:0742426430">0742-42-6430</a><a href="/news/">NEWS一覧へ</a></div>')
        body_html = f'<div class="meta"><time datetime="{p["d"].isoformat()}">{ds}</time><span class="tg">{e(p["tag"])}</span></div><h1>{e(p["meta"]["title"])}</h1>{cov}{art}{pn}{cta}'
        title = p["meta"]["title"] + "｜NEWS｜CAFE & RESTAURANT POOL 奈良"
        path = f'/news/{p["slug"]}/'
        og = f'/og/{p["slug"]}.jpg' if p["cover"] else "/og/top.jpg"
        art_ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["meta"]["title"], "description": p["desc"],
                  "datePublished": p["d"].isoformat(), "dateModified": p["d"].isoformat(), "inLanguage": "ja", "mainEntityOfPage": URL + path,
                  "image": [URL + og], "author": {"@type": "Organization", "name": "CAFE & RESTAURANT POOL"},
                  "publisher": {"@type": "Organization", "name": "CAFE & RESTAURANT POOL", "logo": {"@type": "ImageObject", "url": URL + "/img/logo-d.png"}}}
        page = finalize(tpl.replace("{{BODY}}", body_html), title, p["desc"], path, og,
                        [art_ld, crumbs([("トップ", "/"), ("NEWS", "/news/"), (p["meta"]["title"], path)])], "article")
        os.makedirs(os.path.join(OUT, "news", p["slug"]), exist_ok=True)
        open(os.path.join(OUT, "news", p["slug"], "index.html"), "w", encoding="utf-8").write(page)
    cards = ""
    for p in posts:
        im = f'<div class="im"><img src="/news/{p["slug"]}/cover.jpg" alt="{e(p["meta"].get("alt", p["meta"]["title"]))}" width="{p["cw"][0]}" height="{p["cw"][1]}" loading="lazy"></div>' if p["cover"] else ""
        cards += f'<a href="/news/{p["slug"]}/">{im}<div class="tx"><time datetime="{p["d"].isoformat()}">{p["d"].strftime("%Y.%m.%d")}</time><h2>{e(p["meta"]["title"])}</h2><p>{e(p["excerpt"])}</p></div></a>'
    lst = f'<p class="en">NEWS</p><h1>お知らせ・NEWS</h1><div class="cards">{cards or "<p>まだお知らせはありません。</p>"}</div>'
    page = finalize(tpl.replace("{{BODY}}", lst), "お知らせ・NEWS｜CAFE & RESTAURANT POOL 奈良・船橋町",
                    "奈良市船橋町のカフェ＆レストランPOOLのお知らせ。新しい料理、お店の様子、営業のご案内を、写真と一緒にお届けします。", "/news/", "/og/top.jpg",
                    [crumbs([("トップ", "/"), ("NEWS", "/news/")])])
    os.makedirs(os.path.join(OUT, "news"), exist_ok=True)
    open(os.path.join(OUT, "news", "index.html"), "w", encoding="utf-8").write(page)
    # 固定ページ
    JP = {}
    fixed = {"history.html": ("お店の想い｜CAFE & RESTAURANT POOL 奈良・船橋町", "もとは下駄屋だった一戸建てをリノベーションした、奈良・船橋町のカフェ＆レストランPOOL。お店の想いと、空間のこと。", "/og/top.jpg"),
             "message.html": ("料理へのこだわり｜CAFE & RESTAURANT POOL 奈良・船橋町", "奈良野菜と旬の素材を使ったカジュアルフレンチと、ナチュラルワイン。コース料理、メッセージプレートのご案内も。", "/og/message.jpg")}
    for f, (t, d, o) in fixed.items():
        frag = open(os.path.join(BASE, f), encoding="utf-8").read()
        name = "お店の想い" if f.startswith("history") else "料理へのこだわり"
        pg = finalize(frag, t, d, "/" + f, o, [crumbs([("トップ", "/"), (name, "/" + f)])])
        JP[f.split(".")[0]] = pg
    # トップ
    top = open(os.path.join(BASE, "index.template.html"), encoding="utf-8").read()
    li = "".join(f'<li class="rvl in"><a href="/news/{p["slug"]}/"><time datetime="{p["d"].isoformat()}">{p["d"].strftime("%Y.%m.%d")}</time><span class="tg">{e(p["tag"])}</span><span class="tt">{e(p["meta"]["title"])}</span></a></li>' for p in posts[:5])
    top = re.sub(r"<!--NEWS_LIST-->.*?<!--/NEWS_LIST-->", lambda m: li, top, flags=re.S)
    JP["top"] = finalize(top, TOP_TITLE, TOP_DESC, "/", "/og/top.jpg", [RESTAURANT])
    langurls = langs.build(JP, OUT, URL)
    for k, fn in (("top", "index.html"), ("history", "history.html"), ("message", "message.html")):
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(JP[k])
    # sitemap / robots
    today = dt.date.today().isoformat()
    urls = [("/", today), ("/news/", posts[0]["d"].isoformat() if posts else today), ("/history.html", today), ("/message.html", today)] + [(u, today) for u in langurls] + [(f"/news/{p['slug']}/", p["d"].isoformat()) for p in posts]
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{URL}{u}</loc><lastmod>{m}</lastmod></url>" for u, m in urls) + "</urlset>")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")
    print("posts:", len(posts), "->", OUT)


main()
