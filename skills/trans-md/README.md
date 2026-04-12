[English](README.md) | [Tiếng Việt](README.vi.md) | [日本語](README.ja.md)

# /trans-md Skill

This skill helps you translate Markdown documents across multiple languages automatically and professionally, supporting both forward translation (to language variants) and reverse translation (back to the base file).

## Usage

You can invoke this skill using a slash command or via direct request:

### Syntax
`/trans-md <source-lang> <target-1> [<target-2>] [<file-path>]`

### 1. Forward Translation (Create satellite files with suffixes)
Translate from one file to other languages with a `.[lang].md` suffix.
- `/trans-md vi en ja` (Translate README.md from Vietnamese to English and Japanese)
- `/trans-md en vi docs/api-guide.md` (Translate api-guide.md from English to Vietnamese)

### 2. Reverse Translation (To Base file)
Use the **`base`** keyword to translate a file with a suffix back to the base file without a suffix.
- `/trans-md vi base mydoc.vi.md`
  - Input: `mydoc.vi.md`
  - Output: `mydoc.md` (English/Default content)

### 3. Combination
You can update the base file and create satellite files simultaneously:
- `/trans-md vi base ja mydoc.vi.md`
  - Updates both: `mydoc.md` and `mydoc.ja.md`.

## Key Features
- **Smart Naming**: Automatically detects and handles file suffixes (`.vi.md`, `.ja.md`, ...).
- **Language Switcher**: Automatically inserts/updates the language navigation bar at the top.
- **Code Integrity**: Strictly preserves content within code blocks.
- **Deep Linking**: Updates links between documents if corresponding translations exist.
