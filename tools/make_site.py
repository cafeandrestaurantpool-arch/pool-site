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


def prep(src, dst, maxw=1600):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
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
            flush(); out.append(f"<h3>{e(s[3:])}</h3>")
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
    for f in ("history.html", "message.html"):
        shutil.copy(os.path.join(BASE, f), os.path.join(OUT, f))
    tpl = open(os.path.join(BASE, "page.template.html"), encoding="utf-8").read()
    posts = []
    for slug in sorted(os.listdir(SRC)) if os.path.isdir(SRC) else []:
        sd = os.path.join(SRC, slug)
        if not os.path.isfile(os.path.join(sd, "post.md")):
            continue
        meta, body, d = parse(os.path.join(sd, "post.md"), slug)
        cover = meta.get("photo")
        cw = None
        if cover:
            cw = prep(find(sd, cover), os.path.join(OUT, "news", slug, "cover.jpg"))
        posts.append(dict(slug=slug, meta=meta, body=body, d=d, sd=sd, cover=bool(cover), cw=cw, tag=meta.get("tag", "NEWS")))
    posts.sort(key=lambda p: (p["d"], p["slug"]), reverse=True)
    for i, p in enumerate(posts):
        p["excerpt"] = plain(p["body"])[:60] + ("…" if len(plain(p["body"])) > 60 else "")
        art = md(p["body"], p["slug"], p["sd"])
        ds = p["d"].strftime("%Y.%m.%d")
        cov = f'<div class="cover"><img src="/news/{p["slug"]}/cover.jpg" alt="{e(p["meta"].get("alt", p["meta"]["title"]))}" width="{p["cw"][0]}" height="{p["cw"][1]}"></div>' if p["cover"] else ""
        prev_ = posts[i + 1] if i + 1 < len(posts) else None
        next_ = posts[i - 1] if i > 0 else None
        pn = '<div class="pn"><span>' + (f'<a href="/news/{prev_["slug"]}/">← {e(prev_["meta"]["title"])}</a>' if prev_ else "") + '</span><span>' + (f'<a href="/news/{next_["slug"]}/">{e(next_["meta"]["title"])} →</a>' if next_ else "") + "</span></div>"
        cta = ('<div class="go"><a class="f" href="https://ig.me/m/cafeandrestaurant_pool" target="_blank" rel="noopener">DMで予約</a>'
               '<a href="tel:0742426430">0742-42-6430</a><a href="/news/">NEWS一覧へ</a></div>')
        body_html = (f'<div class="meta"><time>{ds}</time><span class="tg">{e(p["tag"])}</span></div><h2 class="t">{e(p["meta"]["title"])}</h2>{cov}{art}{pn}{cta}')
        page = tpl.replace("{{TITLE}}", e(p["meta"]["title"]) + " | CAFE &amp; RESTAURANT POOL").replace("{{DESC}}", e(p["excerpt"])).replace("{{BODY}}", body_html)
        os.makedirs(os.path.join(OUT, "news", p["slug"]), exist_ok=True)
        open(os.path.join(OUT, "news", p["slug"], "index.html"), "w", encoding="utf-8").write(page)
    # list page
    cards = ""
    for p in posts:
        im = f'<div class="im"><img src="/news/{p["slug"]}/cover.jpg" alt="" width="{p["cw"][0]}" height="{p["cw"][1]}" loading="lazy"></div>' if p["cover"] else ""
        cards += f'<a href="/news/{p["slug"]}/">{im}<div class="tx"><time>{p["d"].strftime("%Y.%m.%d")}</time><h3>{e(p["meta"]["title"])}</h3><p>{e(p["excerpt"])}</p></div></a>'
    lst = f'<h1>NEWS</h1><h2>お知らせ</h2><div class="cards">{cards or "<p>まだお知らせはありません。</p>"}</div>'
    page = tpl.replace("{{TITLE}}", "NEWS お知らせ | CAFE &amp; RESTAURANT POOL").replace("{{DESC}}", "CAFE &amp; RESTAURANT POOL のお知らせ").replace("{{BODY}}", lst)
    os.makedirs(os.path.join(OUT, "news"), exist_ok=True)
    open(os.path.join(OUT, "news", "index.html"), "w", encoding="utf-8").write(page)
    # top
    top = open(os.path.join(BASE, "index.template.html"), encoding="utf-8").read()
    li = "".join(f'<li class="rvl in"><a href="/news/{p["slug"]}/"><time>{p["d"].strftime("%Y.%m.%d")}</time><span class="tg">{e(p["tag"])}</span><span class="tt">{e(p["meta"]["title"])}</span></a></li>' for p in posts[:5])
    top = re.sub(r"<!--NEWS_LIST-->.*?<!--/NEWS_LIST-->", lambda m: li, top, flags=re.S)
    if not top.lstrip().lower().startswith("<!doctype"):
        top = '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="description" content="奈良・船橋町のカフェ＆レストラン POOL。昼は気軽なカフェ、夜はワインと料理を。">' + top + "</head></html>"
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(top)
    # sitemap
    base = "https://pool-nara.netlify.app"
    urls = ["/", "/news/", "/history.html", "/message.html"] + [f"/news/{p['slug']}/" for p in posts]
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{base}{u}</loc></url>" for u in urls) + "</urlset>")
    print("posts:", len(posts), "->", OUT)


main()
