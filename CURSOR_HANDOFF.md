# RV BASE Lab — Cursor 引き継ぎ

更新日: 2026-10-23（日本時間）

## 現在の状態

- キャンピングカー整備工場「RV BASE Lab」のサイト。これまでの依頼は公開済み。
- 公開 URL: https://rv-base-lab-camp-repair.laplus3.chatgpt.site/
- このフォルダが公開サイトのソース。別プロジェクトを新規作成しない。
- FV更新前の公開コミット: `996d4dd1536482597dec5dd8e651d4984000e529`。最新ソースは Git 履歴で確認。
- 現時点で未実装の追加依頼はない。次の指示を受けて、この状態から編集する。

## 編集とプレビュー

静的 HTML / CSS / JavaScript サイト。npm ビルドは不要。

- `build_story_layout.py`: 現在のビルド入口。以前のビルダーを順番に呼び、最終ページを作る。
- `dist/index.html`: ビルド出力。直接編集すると次回ビルドで消えるため、HTML の変更はビルダーや下記の部品へ。
- `dist/*.css` と `dist/*.js`: 配信するスタイルと動作。直接編集する。
- `dist/assets/`: 使用中の画像、公式ロゴ等。
- `camp-about.html`: 私たちについて・経験・3つの強み。
- `flow-accordion.html`: ご相談の流れの4ステップ。
- `fixed-camper.html`: 右下の固定キャンピングカー。

HTML を変更したらプロジェクトルートで:

```sh
/Users/kasaikyohei/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 build_story_layout.py
```

この Python 環境には lxml が入っている。別の環境を使う場合も lxml が必要。
ローカル確認は `dist` を静的配信する。以前のプレビューは http://127.0.0.1:8846/ 。既存サーバーが動いていれば再利用する。

## 直近の変更

### FV主人公の画風（2026-10-26）

- 添付の漫画を参考に、FVの整備士を丸みのある顔立ち、大きく表情豊かな目、明るい笑顔に変更。カメラ目線・黒い作業着・2台のキャンピングカーとキャンプの構図は維持。
- 最新画像は `dist/assets/hero-camper-family-v3.png`、生成条件は `hero-tone-generation.json`。


### FVのキャンプイラスト（2026-10-23）

- `hero-scene.html` / `dist/hero-scene.css`: FVの文字と画像の配置。
- `dist/assets/hero-camper-family-v3.png`: 新しく生成した完成イラスト。
- `hero-scene-generation.json`: 内蔵画像生成ツールのプロンプトと参照元。
- `apply_hero_scene.py`: FVのみを置き換える処理。`build_story_layout.py` の最後から呼ばれる。
- スマホLPとして端末幅に追従し、PCでは最大430px幅で中央配置。`dist/mobile-lp.css` でFV・余白・文字・固定CTAを調整。


### 画面下の固定相談ボタン

- 電話リンクに受話器の SVG アイコンを追加。表示文言は「電話で相談」。
- LINE の表示は「今すぐLINEで」「チャット相談」の2行。
- 左右の幅は文字数に影響されない `minmax(0,1fr) minmax(0,1.8fr)` の比率。高さは両方64px。
- 実装: `build_story_layout.py` の `mobile_line` / `mobile_phone` 周辺、`dist/layout-polish.css` の `.mobile-contact` 周辺。

### 相談セクションの「お問い合わせフォーム」

- ユーザー希望で削除。相談窓口は LINE と電話のみ。
- 実装: `build_story_layout.py` で `#contact` 内の `a.contact-form` を `drop_tree()`。

### ヘッダー

- ヘッダーだけ LINE アイコンを削除。「LINEで相談 ↗」の文字ボタン。
- スマホでも文字を表示。他の LINE ボタンの公式アイコンは残す。

### 右下の固定キャンピングカー

- 吹き出しは現在読んでいるセクションに合わせて切り替わる。ご相談の流れは4ステップに対応。
- スクロールを戻した場合も更新。画像の読み込み、画面サイズ変更、アコーディオン開閉にも追従。
- 「動きを止める」ボタンはユーザー希望で削除。
- 車は左向き。タイヤ全体を `rotate(-360deg)` で前進方向へ回転させる。車体の上下動あり。
- 最後の相談セクション（`#contact`）の上端が画面の60%まで来るか、ページ最下部に達すると、吹き出しを消して左へ走り去る（クラス `is-departed`）。スクロールを戻すと右から走って戻る。
- OS の `prefers-reduced-motion` 設定は尊重する（走り去りはアニメーションせず非表示）。
- 実装: `fixed-camper.html`、`dist/fixed-camper.css`、`dist/fixed-camper.js`。

### テキストと LINE ボタン

- `dist/text-motion.js` / `.css` に見出しのスクロール表示アニメーション。
- ボタン内の文言が消えないようにする。SVG を取り除く際、lxml の `remove()` は後続テキストも落とす場合があるため `drop_tree()` を使用。
- LINE ロゴは公式の透過 PNG `dist/assets/line-brand-icon.png`。画像の背景色を付けない。

## デザインで維持すること

- FV はユーザーの新しい参考画像に合わせて、手前にキャンピングカー2台、中央にカメラ目線の整備士、奥にキャンプと子どもたちを描いたイラストへ更新。文字は絵の上下に配置し、車・顔・背景を隠さない。緑・茶・生成りの配色を維持。
- ブランド公式ロゴは `rv-base-lab-official-logo.png`。車のナンバープレートにも使用。
- 不要な英語の飾り見出しは削除済み。固有名詞 RV BASE Lab / LINE / Google は残す。
- 人物イラストは全員カメラ目線にしない。作業箇所を見る、整備士と利用者が会話する自然な場面。
- サービス下の相談カードはテキストが左、人物が右。
- 経験年数10年・30年のカードは左右の見出し・数字の高さをそろえる。
- 強みの3カードは「タブ見出し → 01などの番号と見出し → 画像 → 説明」の順。
- ご相談の流れは実写風の生成画像4枚。撮影する利用者 / 外装点検 / 電卓による説明 / 運転席のお客様に窓越しで話す整備士。
- 吹き出しで人物の顔や作業箇所を隠さない。
- 店舗欄の Google マップ埋め込みを維持。

## 確認済みの店舗情報

- RV BASE Lab
- 〒292-0455 千葉県君津市俵田729-3
- 電話: `050-5585-9522` / リンク: `tel:05055859522`
- LINE: https://lin.ee/bryjnk0
- 公式アクセス: https://rvbaselab.com/access
- 地図: https://maps.app.goo.gl/UdEobBBbQLo8JsiH7
- 関東運輸局長認証 自動車特定整備事業 第3-5923号
- メカニックのキャンピングカービルダー勤務10年、パートナーの自動車業界経験30年。
- 無料見積もり・料金・即日対応などの未確認情報は追加しない。

## 公開方法と注意

- クライアント共有用: GitHub Pages https://laplus7123-byte.github.io/rv-base-lab-camp-lp/ （公開リポジトリ https://github.com/laplus7123-byte/rv-base-lab-camp-lp ）。`main` に push すると `.github/workflows/pages.yml` が `dist` を自動公開する（数分）。
- 以下は Codex Sites（所有者のみ）の情報。

- ホスティングは Codex の Sites プラグイン。設定は `.openai/hosting.json`。
- 同ファイルの既存 `project_id` と `static.directory: dist` を維持する。
- 現在は所有者のみのアクセス設定。共有範囲を勝手に変えない。
- 公開には Sites の認証情報と公開処理が必要。認証トークンはこのフォルダに保存していない。
- Cursor でのローカル編集だけでは公開サイトは更新されない。公開は Codex の同じチャットに戻し、既存 Sites の更新として行える。
- 公開時は最新版ソースの確認、ビルド、確認、正確なソースの保存、配信用アーカイブ作成、同サイトへのデプロイの順。別の公開先を作らない。

## 検証状況

- 最新のビルド、HTML構造、ボタンの文言とリンク、アイコンの有無を確認済み。公開処理は成功。
- 固定キャンパーの前後スクロール、開閉による位置変更、動きを減らす設定はロジック確認済み。
- Codex のブラウザ操作は環境の制限により使用できず、最新変更の実ブラウザでの表示確認は未実施。Cursor 側では特に320〜430px幅の固定相談ボタンと、キャンパーとの重なりを確認するとよい。
