"""多言語ページ（/en/ /fr/ /zh/ /ko/）を作る。日本語ページを、辞書（i18n_data.py）で訳して書き出す。"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import i18n_data as D

LOC = {"en": "en_US", "fr": "fr_FR", "zh": "zh_CN", "ko": "ko_KR"}
HL = {"ja": "ja", "en": "en", "fr": "fr", "zh": "zh-Hans", "ko": "ko"}
NAMES = [("ja", "JA"), ("en", "EN"), ("fr", "FR"), ("zh", "中文"), ("ko", "한국어")]
WD = {"en": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], "fr": ["dim", "lun", "mar", "mer", "jeu", "ven", "sam"],
      "zh": ["日", "一", "二", "三", "四", "五", "六"], "ko": ["일", "월", "화", "수", "목", "금", "토"]}
META = {  # ページごとの title / description
 "top": {"en": ("POOL | Café & restaurant in Nara – lunch, dinner, natural wine", "Café & restaurant in an old Nara building. Casual French food with Nara vegetables and natural wine. 9 min from Kintetsu Nara Station."),
         "fr": ("POOL | Café-restaurant à Nara – déjeuner, dîner, vins nature", "Café-restaurant dans un ancien bâtiment de Nara. Cuisine française aux légumes de Nara, vins nature. À 9 min de la gare Kintetsu Nara."),
         "zh": ("POOL｜奈良船桥町的咖啡厅＆餐厅｜午餐・晚餐・自然葡萄酒", "POOL是位于奈良市船桥町老建筑中的咖啡厅＆餐厅。午餐与晚餐供应使用当季奈良蔬菜的轻松法式料理和自然葡萄酒。从近铁奈良站步行9分钟。请通过电话或Instagram私信预约。"),
         "ko": ("POOL｜나라 후나바시초의 카페＆레스토랑｜런치・디너・내추럴 와인", "POOL은 나라시 후나바시초의 오래된 건물을 살린 카페＆레스토랑입니다. 제철 나라 채소를 사용한 캐주얼 프렌치와 내추럴 와인을 런치와 디너로 즐기실 수 있습니다. 긴테쓰 나라역에서 도보 9분. 예약은 전화 또는 인스타그램 DM으로.")},
 "history": {"en": ("Our story | CAFE & RESTAURANT POOL, Nara", "A former geta shop renovated into POOL, a café & restaurant in Funabashi-cho, Nara. Our story and our space."),
             "fr": ("Notre histoire | CAFE & RESTAURANT POOL, Nara", "Une maison autrefois boutique de geta, rénovée en café-restaurant POOL à Funabashi-cho, Nara. Notre histoire et notre espace."),
             "zh": ("关于小店 | CAFE & RESTAURANT POOL 奈良", "由原木屐店的独栋房屋翻新而成的奈良船桥町咖啡厅＆餐厅POOL。介绍小店的故事、空间与座位，欢迎光临。"),
             "ko": ("가게 이야기 | CAFE & RESTAURANT POOL 나라", "예전 게타 가게였던 단독 건물을 리노베이션한 나라 후나바시초의 카페＆레스토랑 POOL. 가게 이야기와 공간 소개.")},
 "message": {"en": ("Our cooking | CAFE & RESTAURANT POOL, Nara", "Casual French cooking with Nara vegetables and seasonal ingredients, plus natural wine. Course menus and message plates available."),
             "fr": ("Notre cuisine | CAFE & RESTAURANT POOL, Nara", "Cuisine française décontractée aux légumes de Nara et produits de saison, vins nature. Menus et assiettes message possibles."),
             "zh": ("料理的用心 | CAFE & RESTAURANT POOL 奈良", "使用奈良蔬菜和当季食材的轻松法式料理与自然葡萄酒。备有套餐料理和留言盘，欢迎预约时咨询。"),
             "ko": ("요리에 대한 마음 | CAFE & RESTAURANT POOL 나라", "나라 채소와 제철 재료를 사용한 캐주얼 프렌치와 내추럴 와인. 코스 요리와 메시지 플레이트도 준비되어 있습니다.")}}
PATH = {"top": "/", "history": "/history.html", "message": "/message.html"}


def lp(page, l):  # ページの住所
    p = PATH[page]
    return p if l == "ja" else ("/" + l + p)


def switch(page, cur):
    return '<div class="lgs" role="group" aria-label="Language">' + "".join(
        f'<a href="{lp(page, c)}" hreflang="{HL[c]}" lang="{HL[c]}"{" class=on aria-current=true" if c == cur else ""}>{n}</a>' for c, n in NAMES) + "</div>"


def alts(page, URL):
    return "".join(f'<link rel="alternate" hreflang="{HL[c]}" href="{URL}{lp(page, c)}">' for c, _ in NAMES) + f'<link rel="alternate" hreflang="x-default" href="{URL}{lp(page, "ja")}">'


def tr(h, page, l, URL):
    T, A = D.T, D.ALT
    def text(m):
        k = html.unescape(m.group(1).strip())
        t = T.get(k)
        return ">" + m.group(1).replace(m.group(1).strip(), html.escape(t[l], quote=False)) + "<" if t else m.group(0)
    h = re.sub(r">([^<>]*[^\s<>][^<>]*)<", text, h)
    def alt(m):
        k = html.unescape(m.group(1)); t = A.get(k)
        return 'alt="' + html.escape(t[l]) + '"' if t else m.group(0)
    h = re.sub(r'alt="([^"]*)"', alt, h)
    ti, de = META[page][l]
    url = URL + lp(page, l)
    h = re.sub(r"<title>.*?</title>", "<title>" + html.escape(ti) + "</title>", h, count=1, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(de), h)
    for p in ("og:title", "twitter:title"):
        h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % p, lambda m: m.group(1) + html.escape(ti), h)
    for p in ("og:description", "twitter:description"):
        h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*' % p, lambda m: m.group(1) + html.escape(de), h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, h)
    h = h.replace('og:locale" content="ja_JP"', 'og:locale" content="%s"' % LOC[l])
    h = h.replace('<html lang="ja">', '<html lang="%s">' % HL[l])
    h = h.replace("</title>", "</title>" + alts(page, URL), 1) if False else h.replace('<link rel="canonical"', alts(page, URL) + '<link rel="canonical"', 1)
    h = h.replace("'<span>'+COPY[k]+'</span><em>'+EN[k]+'</em>'", "'<span>'+EN[k]+'</span>'")
    h = h.replace("(i+1)+'番目のバナー'", {"en": "'Banner '+(i+1)", "fr": "'Bannière '+(i+1)", "zh": "'第'+(i+1)+'张横幅'", "ko": "(i+1)+'번째 배너'"}[l])
    h = h.replace("W='日月火水木金土'", "W=" + str(WD[l]))
    h = re.sub(r"(?<![/\w.-])img/", "/img/", h)
    h = h.replace('href="news/"', 'href="/news/"').replace("'news/'", "'/news/'")
    h = h.replace("<!--LANGSW-->", switch(page, l))
    return h


def build(pages, out, URL):
    """pages = {'top': html, 'history': html, 'message': html}（日本語・完成版）。返り値は、新しいページの住所のリスト。"""
    urls = []
    for page, h in pages.items():
        ja = h.replace('<link rel="canonical"', alts(page, URL) + '<link rel="canonical"', 1).replace("<!--LANGSW-->", switch(page, "ja"))
        ja = re.sub(r"(?<![/\w.-])img/", "/img/", ja) if False else ja
        pages[page] = ja
        for l in ("en", "fr", "zh", "ko"):
            fp = os.path.join(out, l, "index.html" if page == "top" else PATH[page][1:])
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, "w", encoding="utf-8").write(tr(h, page, l, URL))
            urls.append(lp(page, l) if page != "top" else "/" + l + "/")
    return urls
