#!/usr/bin/env python3
"""表示を速くするための仕上げ（make_site.py の最後に自動で呼ばれる）。

1. site/ の写真（JPG）ごとに、同じ画素数・同じ縦横比の WebP 版を、別ファイルで作る。
   - 写真の中身・構図・色味は変えない（縮小・トリミング・加工はしない。保存形式を変えるだけ）。
   - 元の JPG はそのまま残す（src/base/img と site/img の両方）。OGP画像（site/og）は対象外。
2. HTML の写真の参照を、WebP 版に切りかえる（デザイン・文字はそのまま）。
3. トップページの、ファーストビューより下の写真に loading="lazy" を付ける。
4. 写真に width・height（元の画素数）を付け、読み込み中のずれを防ぐ。
   ただし表示の大きさが変わる恐れがあるロゴなど（NO_SIZE）には付けない。
"""
import os, re
from PIL import Image

QUALITY = 82          # WebP の画質（0〜100）。82 は見た目で差が分からない範囲
NO_SIZE = ("logo-d.png", "logo-w.png")   # 高さだけ CSS で決めている画像には width/height を付けない


def make_webp(site):
    """site/img と site/news/*/ の JPG から WebP 版を作る。{jpgの相対パス: (w, h)} を返す。"""
    made = {}
    for d in [os.path.join(site, "img")] + [os.path.join(site, "news", s) for s in sorted(os.listdir(os.path.join(site, "news")))
                                             if os.path.isdir(os.path.join(site, "news", s))]:
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.lower().endswith((".jpg", ".jpeg")):
                continue
            src = os.path.join(d, f)
            dst = os.path.splitext(src)[0] + ".webp"
            im = Image.open(src)
            im.load()
            kw = {"quality": QUALITY, "method": 6}
            if im.info.get("icc_profile"):
                kw["icc_profile"] = im.info["icc_profile"]   # 色の情報があれば、そのまま引きつぐ
            im.convert("RGB").save(dst, "WEBP", **kw)
            if os.path.getsize(dst) >= os.path.getsize(src):   # 軽くならなければ使わない
                os.remove(dst)
                continue
            made[os.path.relpath(src, site).replace(os.sep, "/")] = im.size
    return made


def sizes_of(site):
    """画像の画素数（width/height 用）。"""
    out = {}
    for r, _, fs in os.walk(site):
        for f in fs:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and os.sep + "og" + os.sep not in r + os.sep:
                p = os.path.join(r, f)
                with Image.open(p) as im:
                    out[os.path.relpath(p, site).replace(os.sep, "/")] = im.size
    return out


def resolve(page_rel, ref):
    """HTML 内の参照 → site/ からの相対パス。"""
    ref = ref.split("?")[0].split("#")[0]
    if ref.startswith(("http:", "https:", "data:", "//")):
        return None
    if ref.startswith("/"):
        return ref.lstrip("/")
    return os.path.normpath(os.path.join(os.path.dirname(page_rel), ref)).replace(os.sep, "/")


REF = re.compile(r"""(?P<ref>(?:\.\./)*/?(?:img|news/[\w.-]+)/[\w.-]+)\.(?:jpg|jpeg)(?=["')\s])""", re.I)


def rewrite(html, page_rel, made):
    # 2. 参照を WebP に（HTML属性・CSS の url()・スクリプト内の 'img/'+名前+'.jpg'）
    def sub(m):
        target = resolve(page_rel, m.group(0))
        return m.group("ref") + ".webp" if target in made else m.group(0)
    html = REF.sub(sub, html)
    # トップの canvas スライドは、スクリプトが data-n の名前から 'img/名前.jpg' を読む
    names = [x for s in re.findall(r'data-n="([^"]+)"', html) for x in s.split(",")]
    if names and all(f"img/{x}.jpg" in made for x in names):
        html = re.sub(r"(m\.src='/?img/'\+n\+')\.jpg'", r"\1.webp'", html)
    return html


def add_attrs(html, page_rel, sizes):
    # <template>（トップの動くスライド）の中は触らない
    spans = [(m.start(), m.end()) for m in re.finditer(r"<template\b.*?</template>", html, re.S)]
    in_tpl = lambda i: any(a <= i < b for a, b in spans)
    is_top = os.path.basename(page_rel) == "index.html" and 'id="brand"' in html and 'id="fxr"' in html
    fold_end = html.find('id="brand"') if is_top else -1

    def tag(m):
        t, i = m.group(0), m.start()
        if in_tpl(i):
            return t
        src = re.search(r'\ssrc="([^"]+)"', t)
        if not src:
            return t
        target = resolve(page_rel, src.group(1))
        name = os.path.basename(target or "")
        add = ""
        # 3. ファーストビューより下（トップの BRAND 以降）を遅延読み込み
        if is_top and i > fold_end and " loading=" not in t:
            add += ' loading="lazy" decoding="async"'
        # 4. width・height
        if target in sizes and " width=" not in t and " height=" not in t and name not in NO_SIZE:
            w, h = sizes[target]
            add += f' width="{w}" height="{h}"'
        return t[:-1].rstrip("/").rstrip() + add + ">" if add else t
    return re.sub(r"<img\b[^>]*>", tag, html)


def run(site):
    made = make_webp(site)
    sizes = sizes_of(site)
    n = 0
    for r, _, fs in os.walk(site):
        for f in fs:
            if not f.endswith(".html") or f.startswith("google"):
                continue
            p = os.path.join(r, f)
            rel = os.path.relpath(p, site).replace(os.sep, "/")
            h0 = open(p, encoding="utf-8").read()
            h = add_attrs(rewrite(h0, rel, made), rel, sizes)
            if h != h0:
                open(p, "w", encoding="utf-8").write(h)
                n += 1
    before = sum(os.path.getsize(os.path.join(site, k)) for k in made)
    after = sum(os.path.getsize(os.path.join(site, os.path.splitext(k)[0] + ".webp")) for k in made)
    if made:
        print(f"WebP: {len(made)}枚 {before/1048576:.1f}MB → {after/1048576:.1f}MB（-{100 - after * 100 / before:.0f}%）、HTML {n}件を更新")


if __name__ == "__main__":
    import sys
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "site"))
