# 週1回のSEO・集客の手順（3サイトまとめて）

対象（PPPデザインの制作物 `homepage`・`sitebrief-app` は対象外）：
| サイト | リポジトリ | 公開アドレス |
|---|---|---|
| Allons Bien（焼き菓子・通販） | allonsbien-nara | https://cafeandrestaurantpool-arch.github.io/allonsbien-nara/ |
| POOL（カフェ＆レストラン） | pool-site | https://cafeandrestaurantpool-arch.github.io/pool-site/ |
| POOL ウェディング二次会 | pool-nara-wedding | https://cafeandrestaurantpool-arch.github.io/pool-nara-wedding/ |

記録はすべて、このリポジトリ（pool-site）の `seo/` に残す。
- `seo/ranks.csv` … 検索順位の記録（毎週、行を足す）
- `seo/reports/YYYY-MM-DD.md` … 週ごとのレポート
- 各リポジトリの `SEO_FOCUS.md` … 「今週ねらうテーマ」。毎日の記事担当が、書く前に読む

## 1. アクセス・検索の状況を集める
1. **Google アナリティクス（GA4）**：3サイトとも測定ID `G-MOR6JDYLBK`（同じプロパティ。ページのアドレスの `/allonsbien-nara/`・`/pool-site/`・`/pool-nara-wedding/` でサイトを見分ける）。記録しているクリック：予約 reservation_click、電話 phone_click、楽天市場 shop_click、Instagram instagram_click、二次会サイトへ wedding_click、姉妹店へ sister_click。
   Googleドライブで、名前に「GA4」「アナリティクス」を含むスプレッドシート（オーナーが「GA4 Reports Builder」で毎週自動更新にしたもの）を探し、あれば、サイトごとの 表示回数・ユーザー数・流入元（organic＝検索から、など）・よく見られたページ・クリック数 をまとめ、先週と比べる。
2. **本当のデータ（Search Console）**：Googleドライブで、名前に「Search Console」「検索パフォーマンス」「アナリティクス」「Analytics」を含むファイル（オーナーが書き出して置いたCSV・スプレッドシート）を `search_files` で探す。直近のものがあれば読み、クリック数・表示回数・平均掲載順位・よく使われた検索語・よく見られたページを、サイトごとにまとめる。
3. **検索順位のチェック**：下の「ねらう言葉」を WebSearch（standard）で1つずつ検索し、結果の上位に自分のサイト（3つの公開アドレス）が何番目に出るかを記録する。出なければ「圏外」。あわせて、上位に出ている競合ページの「タイトルの付け方・中身の切り口」をメモする。
   - 注意：WebSearch はGoogleそのものではなく、場所も日本ではないので、**目安**として扱う。レポートにもそう書く。
4. **インデックスの確認**：店名＋「公式」（例「アロンビアン 公式」「POOL 奈良 船橋町 公式」「POOL 奈良 二次会」）で検索し、公式サイトが出るか確認する。
5. `seo/ranks.csv` に `date,site,keyword,position,top_url` の形で追記する（position は数字か「圏外」）。

## 2. サイトの点検（技術面）
- pool-site：`python3 tools/make_site.py && python3 tools/check_site.py`（エラー0）
- pool-nara-wedding：`python3 tools/make_site.py --src src --out site`
- allonsbien-nara：HTMLを直接点検
- AI検索向け：`llms.txt`（allonsbien-nara は直下、pool-site・pool-nara-wedding は `src/base/llms.txt`）の内容が、facts.md や商品ページと食い違っていないか。食い違っていたら llms.txt を直す（facts.md が正）。
- 3サイトとも、次を確認する：title（全角30字前後）・description（80〜120字）・h1が1つ・canonical・OGP・JSON-LD・画像alt・sitemap.xml に全ページが入っているか・リンク切れ・同じtitleのページがないか・姉妹サイト同士のリンクが生きているか。

## 3. 改善する（1週間に、サイトごと1〜3か所まで）
優先順位：
1. 技術的なミスを直す（上の点検で見つかったもの）。
2. 表示はされているがクリックされないページ（Search Console のデータがある場合）→ title と description を、検索した人に中身が伝わる言葉に書き直す。
3. 順位が11〜30位あたりの言葉 → そのページの本文に、その言葉で探す人の疑問に答える段落を足す。関連記事どうしの内部リンクを足す。
4. 「圏外」の大事な言葉 → 次の週の `SEO_FOCUS.md` に「この言葉に答える記事を書く」と入れる（記事そのものは毎日の記事担当が書く）。
守ること：
- お店の事実は、各リポジトリの `src/facts.md`（Allons Bien は既存ページと毎日の記事担当の指示にある事実）だけ。価格・実績・お客様の声などを作らない。
- キーワードを不自然に詰め込まない。読む人の役に立つことを最優先にする。
- 固定ページ（トップの文章、お店の想い、料理へのこだわり、多言語ページ）の**文章**は書き換えない。直してよいのは title・description・alt・構造化データ・内部リンク・記事ページ。
- `.github/workflows/pages.yml`、`tools/pages_fix.py`、`googlef67383f62743634e.html`、`src/base/_redirects` は変えない・消さない。
- 毎日・3日ごとの記事担当と同じ日に push がぶつからないよう、push 前に必ず `git fetch origin main && git rebase origin/main`。

## 4. `SEO_FOCUS.md` を更新する（各リポジトリ）
「今週ねらうテーマ」を3〜5個、具体的に書く（例：「『カヌレ 日持ち』で探す人に、保存方法と食べごろを伝える記事」）。過去記事と重ならないものにする。毎日の記事担当が、これを見て話題を選ぶ。

## 5. 集客の文案をつくる（レポートに入れる）
オーナーがそのまま貼れる文を作る（投稿はオーナーがする。こちらからは投稿しない）：
- Instagram 投稿文 × 各サイト1本（今週の記事や季節の話題から。ハッシュタグ5〜8個）
- Googleビジネスプロフィールの「最新情報」投稿文 × POOL・Allons Bien 各1本（150〜300字、公式サイトへのリンク付き）
- Threads 用の短文 × 1〜2本

## 5.5 「今週のMEO」をGoogleドライブに作る（Googleビジネスプロフィール用。オーナーはコピーして貼るだけ）
- 置き場所：Googleドライブのフォルダ「MEO（Googleビジネスプロフィール）」（ID `1zAbp8eETnOiCNiflVQ-tRPiK3czW2Vvf`）。`mcp__Google_Drive__create_file` で、`parentId` にこのID、`contentMimeType: text/plain`、タイトル「今週のMEO YYYY-MM-DD」で作る（Googleドキュメントになる）。
- 形は前回の文書（同じフォルダの最新のもの）にそろえる。中身：
  1. チェックリスト（投稿・写真・口コミ返信、季節の注意。例：年末年始・GWの特別営業時間）
  2. POOLの投稿文（150〜300字。今週のNEWSか季節の話題。「詳細」ボタンのリンクは記事ページ）と、合う写真の候補（「POOL写真」フォルダのリンク）
  3. Allons Bienの投稿文（今週の記事か商品。来店をすすめない。ボタンは記事か楽天市場）
  4. 写真の追加の候補（プロフィールの「写真」には、文字の入っていない写真がよい）
  5. 口コミへの返信例（★5／★3〜4／★1〜2／文章なし／Allons Bien）。毎週少しずつ言い回しを変える
  6. 未完了のお願い（ウェブサイト欄、電話番号 0742-42-6430 の統一など）
- 事実は facts.md と既存ページだけ。価格は書かない。お礼と引き換えに口コミを頼む文は書かない。
- フォルダにオーナーが「パフォーマンス」のスクリーンショットを置いていたら、Readで見て、表示回数・電話・ルート検索・ウェブサイトのクリックをレポートに入れる。
- レポートの最後に、この文書のリンクを入れる。

## 6. レポート
`seo/reports/YYYY-MM-DD.md` に、次をまとめる：
1. 今週の数字（Search Console のデータがあれば。なければ「データ未提供」）
2. 検索順位の表（先週との比較。上がった・下がった・圏外）
3. やった改善（どのページの何を、なぜ）
4. 来週ねらうテーマ
5. 集客の文案（そのままコピーできる形）
6. オーナーにお願いしたいこと（ログインが必要な作業。まだ終わっていないものだけ）
pool-site に commit・push し、最後の返信は、通知で読めるように「順位の変化・やった改善・お願い」を5行以内にまとめる。

## ねらう言葉
### Allons Bien
奈良 カヌレ／カヌレ お取り寄せ／奈良 焼き菓子 お取り寄せ／奈良 お土産 焼き菓子／ならまち 焼き菓子／抹茶 カヌレ／古都華 パウンドケーキ／クッキー缶 奈良／アロンビアン
### POOL
奈良 ランチ フレンチ／近鉄奈良駅 ランチ／奈良 ディナー カジュアルフレンチ／奈良 ナチュラルワイン／ならまち ランチ／奈良 カフェ 船橋町／奈良 記念日 ディナー／POOL 奈良
### POOL ウェディング
奈良 二次会 会場／奈良 結婚式 二次会／奈良 貸切 パーティー／奈良 1.5次会／近鉄奈良 貸切 レストラン／奈良 歓送迎会 貸切

## オーナーにしかできないこと（ログインが必要）
- [x] pool-site の GitHub Pages を有効にする（2026-11-03 済み：gh-pages ブランチ方式で自動公開）
- [ ] Google Search Console に、3つの新しいアドレスを「URLプレフィックス」で登録し、`sitemap.xml` を送信する（確認ファイルは3サイトとも設置済み）
- [ ] Googleビジネスプロフィール（POOL・Allons Bien）の「ウェブサイト」欄を、新しい公式サイトのアドレスに変える ← **地域の検索で一番効く**
- [ ] Instagram のプロフィールのリンクを、公式サイトにする
- [ ] ホットペッパー・ぐるなび・食べログなどの店舗情報に「公式サイト」欄があれば、新しいアドレスを入れる
- [ ] Netlify の古いサイト（pool-nara / pool-nara-wedding）：公開がまた動くようになったら、`_redirects` で新アドレスへ自動転送される。不要なら Netlify 側で削除してもよい
- [ ] **GA4 の数字を毎週自動でドライブに出す**：Googleスプレッドシートを新しく作り、「拡張機能 → アドオン → GA4 Reports Builder for Google Analytics」を入れる → レポートを作成（期間：過去7日、指標：表示回数・ユーザー数・イベント数、ディメンション：ページパス・セッションのデフォルトチャネルグループ・イベント名）→「スケジュール設定」で毎週月曜の朝に自動更新。ファイル名に「GA4」を入れる
- [ ] （任意）月に1回、Search Console の「検索パフォーマンス」をCSVで書き出し、Googleドライブに置く → 本当の数字で解析できる
- [ ] （任意・効果大）独自ドメイン（例 pool-nara.jp）を取る
