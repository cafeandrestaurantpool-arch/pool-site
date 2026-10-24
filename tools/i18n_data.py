import json
T={}
def a(ja,en,fr,zh,ko): T[ja]={'en':en,'fr':fr,'zh':zh,'ko':ko}
a('奈良・船橋町のカフェ＆レストラン POOL｜ランチ・ディナー・ナチュラルワイン','POOL, a café & restaurant in Funabashi-cho, Nara | Lunch, dinner & natural wine','POOL, café-restaurant à Funabashi-cho, Nara | Déjeuner, dîner et vins nature','POOL｜奈良船桥町的咖啡厅＆餐厅｜午餐・晚餐・自然葡萄酒','POOL｜나라 후나바시초의 카페＆레스토랑｜런치・디너・내추럴 와인')
a('ご予約は、お電話（0742-42-6430）またはInstagramのDMでお願いいたします。','Reservations: please call (0742-42-6430) or send us an Instagram DM.','Réservation : par téléphone (0742-42-6430) ou par message privé Instagram.','预约请致电（0742-42-6430）或通过Instagram私信联系我们。','예약은 전화(0742-42-6430) 또는 인스타그램 DM으로 부탁드립니다.')
a('DMを送る →','Send a DM →','Envoyer un message →','发送私信 →','DM 보내기 →')
a('お知らせ','Latest news','Actualités','最新消息','소식')
a('お店の想い','Our story','Notre histoire','关于小店','가게 이야기')
a('奈良・船橋町の、古い建物の中にあるカフェ＆レストランです。昼は気軽なカフェとして、夜はワインと料理をゆっくり楽しむ場所として、毎日の暮らしの中に「ちょっといい時間」をつくりたい。そんな想いで、お店を続けています。','A café & restaurant inside an old building in Funabashi-cho, Nara. A relaxed café by day, and by night a place to enjoy wine and food slowly. We want to bring a little "good time" into everyday life, and that is why we keep the doors open.','Un café-restaurant installé dans un ancien bâtiment de Funabashi-cho, à Nara. Café décontracté le jour, lieu pour savourer vin et cuisine à son rythme le soir. Nous voulons offrir un petit « bon moment » au quotidien : c’est pour cela que nous continuons.','我们是位于奈良船桥町一栋老建筑里的咖啡厅＆餐厅。白天是轻松的咖啡厅，夜晚则是慢慢享用葡萄酒与料理的地方。我们希望为日常生活带来一段「小小的美好时光」，这份心意支撑着小店一路走来。','나라 후나바시초의 오래된 건물 안에 있는 카페＆레스토랑입니다. 낮에는 편안한 카페로, 밤에는 와인과 요리를 느긋하게 즐기는 곳으로, 일상 속에 「조금 특별한 시간」을 만들고 싶다는 마음으로 가게를 이어가고 있습니다.')
a('料理へのこだわり','Our cooking','Notre cuisine','料理的用心','요리에 대한 마음')
a('料理で、心を動かす時間を。シェフが旬の素材を選び、ひと皿ずつ、ていねいに仕立てます。できたての一皿を、ナチュラルワインと一緒に、ゆっくり味わってください。','Cooking that moves the heart. Our chef chooses seasonal ingredients and prepares each plate with care. Enjoy a freshly made dish slowly, together with natural wine.','Une cuisine qui touche le cœur. Le chef choisit des produits de saison et prépare chaque assiette avec soin. Savourez un plat tout juste préparé, accompagné d’un vin nature.','用料理，打动人心。主厨挑选当季食材，用心制作每一道菜。请搭配自然葡萄酒，慢慢品尝刚做好的美味。','요리로 마음을 움직이는 시간을. 셰프가 제철 재료를 골라 한 접시 한 접시 정성껏 만듭니다. 갓 만든 요리를 내추럴 와인과 함께 천천히 즐겨 주세요.')
a('おすすめの一皿','Recommended dishes','Nos plats à découvrir','推荐料理','추천 요리')
a('本日のお肉料理','Today’s meat dish','Plat de viande du jour','今日的肉类料理','오늘의 고기 요리')
a('コース料理ございます。','Course menus are available.','Des menus en plusieurs services sont proposés.','备有套餐料理。','코스 요리도 준비되어 있습니다.')
a('地元のお野菜をふんだんに','Plenty of local vegetables','Beaucoup de légumes locaux','大量使用本地蔬菜','지역 채소를 듬뿍')
a('メッセージプレート','Message plate','Assiette message','留言盘','메시지 플레이트')
a('メッセージプレートご用意できます。ご予約時にお伝えください。','We can prepare a message plate. Please tell us when you reserve.','Nous pouvons préparer une assiette message. Merci de nous le préciser lors de la réservation.','可为您准备留言盘，预约时请告知。','메시지 플레이트를 준비해 드릴 수 있습니다. 예약 시 말씀해 주세요.')
a('ナチュラルワイン','Natural wine','Vins nature','自然葡萄酒','내추럴 와인')
a('店舗情報','Shop information','Infos pratiques','店铺信息','매장 정보')
a('〒630-8258 奈良県奈良市船橋町7','7 Funabashi-cho, Nara City, Nara 630-8258','7 Funabashi-cho, Nara, 630-8258 Nara','〒630-8258 奈良县奈良市船桥町7','〒630-8258 나라현 나라시 후나바시초 7')
a('ランチ 11:30〜15:00（L.O. 14:30）','Lunch 11:30–15:00 (last order 14:30)','Déjeuner 11h30–15h00 (dernière commande 14h30)','午餐 11:30〜15:00（最后点单 14:30）','런치 11:30~15:00 (라스트 오더 14:30)')
a('ディナー 18:00〜22:00（L.O. 21:30）','Dinner 18:00–22:00 (last order 21:30)','Dîner 18h00–22h00 (dernière commande 21h30)','晚餐 18:00〜22:00（最后点单 21:30）','디너 18:00~22:00 (라스트 오더 21:30)')
a('毎週火曜・第2水曜（そのほか不定休あり）','Every Tuesday and the 2nd Wednesday (irregular closures also occur)','Tous les mardis et le 2e mercredi du mois (fermetures exceptionnelles possibles)','每周二、每月第2个周三（另有不定期休息）','매주 화요일・둘째 주 수요일 (그 외 부정기 휴무 있음)')
a('近鉄奈良駅から徒歩9分','9 min on foot from Kintetsu Nara Station','9 min à pied de la gare Kintetsu Nara','从近铁奈良站步行9分钟','긴테쓰 나라역에서 도보 9분')
a('JR奈良駅から徒歩11分','11 min on foot from JR Nara Station','11 min à pied de la gare JR Nara','从JR奈良站步行11分钟','JR 나라역에서 도보 11분')
a('あり（4台・お店の南30m）。日・祝は終日、平日・土曜は夜のみ。予約はできません。近隣にコインパーキングもあります。','Available (4 spaces, 30 m south of the shop). All day on Sundays and public holidays; evenings only on weekdays and Saturdays. Parking cannot be reserved. Coin parking is also nearby.','Oui (4 places, à 30 m au sud du restaurant). Toute la journée les dimanches et jours fériés ; le soir uniquement en semaine et le samedi. Pas de réservation possible. Parkings payants à proximité.','有（4个车位，店铺以南30米）。周日、节假日全天可用；工作日和周六仅限晚上。不可预约车位。附近也有投币停车场。','있음 (4대, 가게 남쪽 30m). 일요일・공휴일은 종일, 평일・토요일은 저녁만 이용 가능. 주차 예약은 불가합니다. 근처에 동전 주차장도 있습니다.')
a('Googleマップで、お店の場所を見る →','View the shop on Google Maps →','Voir le restaurant sur Google Maps →','在Google地图上查看店铺位置 →','구글 지도에서 위치 보기 →')
for ja,e,f,z,k in [('日','Sun','dim','日','일'),('月','Mon','lun','一','월'),('火','Tue','mar','二','화'),('水','Wed','mer','三','수'),('木','Thu','jeu','四','목'),('金','Fri','ven','五','금'),('土','Sat','sam','六','토')]: a(ja,e,f,z,k)
a('灰色の日は、お休みです（毎週火曜・第2水曜）。','Grey days are closed (every Tuesday and the 2nd Wednesday).','Les jours grisés sont fermés (tous les mardis et le 2e mercredi).','灰色的日期为休息日（每周二、每月第2个周三）。','회색 날짜는 휴무일입니다 (매주 화요일・둘째 주 수요일).')
a('ご予約は、お電話またはInstagramのDMでお願いいたします。貸切・パーティのご相談もお気軽にどうぞ。','Please reserve by phone or Instagram DM. Private hire and party enquiries are also welcome.','Réservation par téléphone ou message privé Instagram. Privatisations et fêtes : n’hésitez pas à nous consulter.','预约请致电或通过Instagram私信联系。包场、聚会也欢迎随时咨询。','예약은 전화 또는 인스타그램 DM으로 부탁드립니다. 대관・파티 문의도 편하게 말씀해 주세요.')
a('DMで予約','Reserve by DM','Réserver par message','私信预约','DM으로 예약')
a('貸切・二次会','Private hire & after-parties','Privatisation & soirées','包场・二次会','대관・2차 모임')
a('予約','Reserve','Réserver','预约','예약')
a('電話','Call','Appeler','电话','전화')
a('地図','Map','Plan','地图','지도')
a('いらっしゃいませ','Welcome!','Bienvenue !','欢迎光临','어서 오세요')
a('トップへ戻る','Back to top','Retour à l’accueil','返回首页','처음으로')
a('古い建物を、生かして','Giving an old building new life','Redonner vie à un ancien bâtiment','让老建筑焕发新生','오래된 건물을 살려서')
a('もとは下駄屋だった一戸建てを、大胆にリノベーションしました。ヴィンテージ感と、現代的な洗練が混ざる空間です。','A detached house that was once a geta (wooden sandal) shop, boldly renovated. A space where vintage character meets modern refinement.','Une maison indépendante, autrefois boutique de geta (sandales en bois), audacieusement rénovée. Un lieu où le charme vintage rencontre le raffinement contemporain.','这里原本是一家木屐店的独栋房屋，经过大胆翻新。复古氛围与现代的精致在这里交融。','예전에 게타(나막신) 가게였던 단독 건물을 과감하게 리노베이션했습니다. 빈티지한 분위기와 현대적인 세련됨이 어우러진 공간입니다.')
a('席のこと','Seating','Les places','座位','좌석 안내')
a('1階には、通りに面した明るいソファー席があります。2階席は吹き抜けになっています。女子会、デート、記念日、ご宴会まで、使い方はいろいろです。','On the 1st floor, bright sofa seats face the street. The 2nd floor is open to a high ceiling. From girls’ nights and dates to anniversaries and banquets, there are many ways to enjoy it.','Au rez-de-chaussée, des banquettes lumineuses donnent sur la rue. L’étage est ouvert sous un haut plafond. Entre amies, en amoureux, pour un anniversaire ou un banquet : à chacun son usage.','1楼有面向街道的明亮沙发座位，2楼为挑高空间。无论是闺蜜聚会、约会、纪念日还是宴会，都能轻松使用。','1층에는 길가에 면한 밝은 소파석이 있고, 2층은 천장이 트여 있습니다. 여자 모임, 데이트, 기념일, 연회까지 다양하게 이용하실 수 있습니다.')
a('昼も、夜も','Day and night','De jour comme de nuit','白天，也在夜晚','낮에도, 밤에도')
a('ランチやカフェとして、気軽にどうぞ。夜は、旬の野菜を使った料理と、料理に合うワインで。','Drop in casually for lunch or café time. In the evening, enjoy dishes with seasonal vegetables and wine to match.','Venez simplement pour le déjeuner ou le café. Le soir, des plats aux légumes de saison et des vins qui les accompagnent.','午餐或咖啡时光，欢迎随时光临。夜晚有使用当季蔬菜的料理，搭配合适的葡萄酒。','런치나 카페로 편하게 들러 주세요. 밤에는 제철 채소 요리와 잘 어울리는 와인을 즐기실 수 있습니다.')
a('奈良で、奈良野菜を','Nara vegetables, in Nara','Des légumes de Nara, à Nara','在奈良，品尝奈良蔬菜','나라에서, 나라 채소를')
a('旬の野菜や果物を使い、食材にこだわっています。地元のお野菜を、ふんだんに。前菜の盛り合わせが、お店の看板の一皿です。','We care about our ingredients, using seasonal vegetables and fruit, with plenty of local produce. The appetizer platter is our signature dish.','Nous soignons nos produits : légumes et fruits de saison, avec beaucoup de produits locaux. L’assortiment d’entrées est notre plat signature.','我们用心挑选食材，使用当季蔬菜和水果，并大量使用本地蔬菜。前菜拼盘是小店的招牌菜。','제철 채소와 과일을 사용하며 식재료에 정성을 다합니다. 지역 채소를 듬뿍 사용하며, 전채 모둠이 가게의 대표 메뉴입니다.')
a('ワインと一緒に','With wine','Avec du vin','搭配葡萄酒','와인과 함께')
a('料理に合うワインを、種類豊富に揃えています。好みや気分を伝えてもらえれば、お選びします。','We keep a wide selection of wines to match the food. Tell us your taste or mood and we will choose for you.','Un large choix de vins s’accorde avec la cuisine. Dites-nous vos goûts ou votre humeur, nous choisirons pour vous.','备有种类丰富、与料理相配的葡萄酒。告诉我们您的口味或心情，我们为您挑选。','요리에 어울리는 와인을 다양하게 준비했습니다. 취향이나 기분을 말씀해 주시면 골라 드립니다.')
a('コース料理','Course menus','Menus en plusieurs services','套餐料理','코스 요리')
a('コース料理もございます。ご予約のときに、お気軽にご相談ください。','Course menus are also available. Please feel free to ask when you reserve.','Des menus en plusieurs services sont aussi proposés. N’hésitez pas à nous demander lors de la réservation.','也备有套餐料理。预约时请随时咨询。','코스 요리도 있습니다. 예약하실 때 편하게 문의해 주세요.')
a('お店の想い | CAFE & RESTAURANT POOL','Our story | CAFE & RESTAURANT POOL','Notre histoire | CAFE & RESTAURANT POOL','关于小店 | CAFE & RESTAURANT POOL','가게 이야기 | CAFE & RESTAURANT POOL')
a('料理へのこだわり | CAFE & RESTAURANT POOL','Our cooking | CAFE & RESTAURANT POOL','Notre cuisine | CAFE & RESTAURANT POOL','料理的用心 | CAFE & RESTAURANT POOL','요리에 대한 마음 | CAFE & RESTAURANT POOL')
ALT={}
def al(ja,en,fr,zh,ko): ALT[ja]={'en':en,'fr':fr,'zh':zh,'ko':ko}
al('厨房で盛りつけるシェフ','The chef plating a dish in the kitchen','Le chef dresse une assiette en cuisine','主厨在厨房摆盘','주방에서 플레이팅하는 셰프')
al('本日のお肉料理','Today’s meat dish','Plat de viande du jour','今日的肉类料理','오늘의 고기 요리')
al('地元のお野菜をふんだんに','Plenty of local vegetables','Beaucoup de légumes locaux','大量使用本地蔬菜','지역 채소를 듬뿍')
al('メッセージプレート','Message plate','Assiette message','留言盘','메시지 플레이트')
al('ナチュラルワイン','Natural wine','Vins nature','自然葡萄酒','내추럴 와인')
al('CAFE & RESTAURANT POOL の外観','Exterior of CAFE & RESTAURANT POOL','Façade de CAFE & RESTAURANT POOL','CAFE & RESTAURANT POOL 外观','CAFE & RESTAURANT POOL 외관')
al('POOLの店内。ソファー席と、壁にたくさんの絵が並ぶ空間','Inside POOL: sofa seats and a wall full of paintings','Intérieur de POOL : banquettes et murs couverts de tableaux','POOL店内：沙发座位与挂满画作的墙面','POOL 내부: 소파석과 그림이 가득한 벽')
al('古い手すりのある、POOLの店内の階段','The staircase with an old handrail inside POOL','L’escalier à l’ancienne rampe, à l’intérieur de POOL','POOL店内带有老扶手的楼梯','오래된 난간이 있는 POOL 내부 계단')
al('青い壁に絵が並ぶ、POOLの店内','Paintings on a blue wall inside POOL','Tableaux sur un mur bleu à l’intérieur de POOL','POOL店内蓝色墙上的画作','푸른 벽에 그림이 걸린 POOL 내부')
al('吹き抜けの高い天井と、ドライフラワー','High open ceiling and dried flowers','Haut plafond ouvert et fleurs séchées','挑高天花板与干花','탁 트인 높은 천장과 드라이플라워')
al('路地の奥にある、青緑のドア','The blue-green door at the end of the alley','La porte bleu-vert au fond de la ruelle','小巷深处的青绿色门','골목 안쪽의 청록색 문')
al('窓辺の席で食事を楽しむ二人','Two people enjoying a meal by the window','Deux personnes dînant près de la fenêtre','在窗边座位用餐的两人','창가 자리에서 식사를 즐기는 두 사람')
al('カウンターの向こうの厨房','The kitchen beyond the counter','La cuisine derrière le comptoir','吧台后的厨房','카운터 너머의 주방')
al('厨房で料理を盛りつけるシェフ','The chef plating food in the kitchen','Le chef dresse les plats en cuisine','主厨在厨房摆盘','주방에서 요리를 담는 셰프')
al('お肉料理の一皿','A meat dish','Un plat de viande','一道肉类料理','고기 요리 한 접시')
al('焼き野菜と帆立の一皿','Grilled vegetables and scallop','Légumes grillés et Saint-Jacques','烤蔬菜与扇贝','구운 채소와 가리비 요리')
al('ハーブと野菜のサラダ','Herb and vegetable salad','Salade d’herbes et de légumes','香草蔬菜沙拉','허브와 채소 샐러드')
al('黄色い縁の皿に盛った、緑のスープ','Green soup in a yellow-rimmed dish','Soupe verte dans une assiette au bord jaune','盛在黄边盘中的绿色汤','노란 테두리 접시에 담긴 초록 수프')
al('チョコレートで描いたメッセージプレート','A message plate written in chocolate','Une assiette message écrite au chocolat','用巧克力书写的留言盘','초콜릿으로 쓴 메시지 플레이트')
al('ナチュラルワインのボトル','A bottle of natural wine','Une bouteille de vin nature','自然葡萄酒瓶','내추럴 와인 병')
LANGS=[('ja','JA'),('en','EN'),('fr','FR'),('zh','中文'),('ko','한국어')]
SWITCH='<div class="lgs" role="group" aria-label="Language">'+''.join(f'<button type="button" data-l="{c}">{n}</button>' for c,n in LANGS)+'</div>'
CSS='''.lgs{display:flex;gap:2px;align-items:center;margin-left:auto;margin-right:10px}.lgs a,.lgs button{background:none;border:0;color:inherit;font:400 11px 'Zen Kaku Gothic New',sans-serif;padding:6px 6px;cursor:pointer;opacity:.6;letter-spacing:.04em;touch-action:manipulation}.lgs a.on,.lgs button.on{opacity:1;border-bottom:1px solid currentColor}
.sh0 .lgs{color:#04486c}@media(max-width:560px){.lgs a,.lgs button{font-size:10px;padding:6px 4px}}'''
JS='(function(){var T='+json.dumps(T,ensure_ascii=False)+',A='+json.dumps(ALT,ensure_ascii=False)+'''
;var N=[],L='ja';function ts(){N=[];var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:function(n){var p=n.parentNode&&n.parentNode.nodeName;if(p==='SCRIPT'||p==='STYLE'||!/\\S/.test(n.nodeValue))return 3;return 1}});var n;while(n=w.nextNode()){if(n._o===undefined)n._o=n.nodeValue;N.push(n)}}
function ap(l){L=l;ts();N.forEach(function(n){var o=n._o,k=o.trim(),t=T[k];n.nodeValue=(l!=='ja'&&t&&t[l])?o.replace(k,t[l]):o});
document.querySelectorAll('img[alt]').forEach(function(i){if(i._a===undefined)i._a=i.getAttribute('alt');var t=A[i._a];i.setAttribute('alt',(l!=='ja'&&t&&t[l])?t[l]:i._a)});
if(document._t===undefined)document._t=document.title;var tt=T[document._t.replace(/&amp;/g,'&')];document.title=(l!=='ja'&&tt&&tt[l])?tt[l]:document._t;
document.documentElement.lang=l;document.querySelectorAll('.lgs button').forEach(function(b){b.classList.toggle('on',b.dataset.l===l)});try{localStorage.setItem('pool-lang',l)}catch(e){}}
document.querySelectorAll('.lgs button').forEach(function(b){b.onclick=function(){ap(b.dataset.l)}});
var s='ja';try{s=localStorage.getItem('pool-lang')||''}catch(e){}if(!s){var nl=(navigator.language||'ja').toLowerCase();s=nl.indexOf('en')===0?'en':nl.indexOf('fr')===0?'fr':nl.indexOf('zh')===0?'zh':nl.indexOf('ko')===0?'ko':'ja'}
setTimeout(function(){ap(s)},60);window.addEventListener('load',function(){setTimeout(function(){ap(L)},200)})})();'''
