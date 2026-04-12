[English](README.md) | [Tiếng Việt](README.vi.md) | [日本語](README.ja.md)

# /trans-md Skill

このSkillは、Markdownドキュメントを複数の言語に自動的かつ専門的に翻訳することをサポートします。順次翻訳（言語バリアントの作成）と逆翻訳（ベースファイルへの復元）の両方をサポートしています。

## 使用方法

スラッシュコマンドまたは直接の依頼でこのSkillを呼び出すことができます：

### 構文
`/trans-md <source-lang> <target-1> [<target-2>] [<file-path>]`

### 1. 順次翻訳（サフィックス付きのサテライトファイルの作成）
あるファイルから他の言語へ、`.[lang].md` サフィックスを付けて翻訳します。
- `/trans-md vi en ja` (README.mdをベトナム語から英語と日本語に翻訳)
- `/trans-md en vi docs/api-guide.md` (api-guide.mdを英語からベトナム語に翻訳)

### 2. 逆翻訳（ベースファイルへ）
**`base`** キーワードを使用して、サフィックスのあるファイルをサフィックスのないベースファイルに翻訳します。
- `/trans-md vi base mydoc.vi.md`
  - 入力: `mydoc.vi.md`
  - 出力: `mydoc.md` (英語/デフォルト案)

### 3. モードの組み合わせ
ベースファイルの更新とサテライトファイルの作成を同時に行うことができます：
- `/trans-md vi base ja mydoc.vi.md`
  - `mydoc.md` と `mydoc.ja.md` の両方を更新します。

## 主な特徴
- **スマート命名 (Smart Naming)**: ファイルサフィックス (`.vi.md`, `.ja.md`, ...) を自動的に検出して処理します。
- **言語スイッチャー (Language Switcher)**: ページ上部に言語ナビゲーションバーを自動的に挿入/更新します。
- **コードの完全性 (Code Integrity)**: コードブロック内の内容は厳密に保持されます。
- **ディープリンク (Deep Linking)**: 対応する翻訳が存在する場合、ドキュメント間のリンクを自動的に更新します。
