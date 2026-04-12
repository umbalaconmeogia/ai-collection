---
name: trans-md
description: Translate Markdown documents to multiple languages, including mapping back to a base file (reverse translation).
---
# `trans-md` Skill

This skill allows Antigravity to translate one or more Markdown files from a source language to one or more target languages while managing filenames and creating a language switcher navigation bar.

## Trigger

This skill is triggered when:

1. The user starts a request with the `/trans-md` command.
2. The user requests to translate a Markdown document and create language variants or update the base file.

## Command Syntax

```
/trans-md <source-lang> <target-lang-1> [<target-lang-2> ...] [<path-to-file.md>]
```

- `<source-lang>`: Source language code (e.g., `vi`, `en`).
- `<target-lang>`: Target language code (e.g., `ja`, `en`) OR the special keyword **`base`**.
- `<path-to-file.md>`: (Optional) Path to file. Defaults to `README.md` if omitted.

### Special Keyword `base`

The keyword `base` is used to translate back to the "original" or "default" file (the one without a language suffix).

- If the input is `mydoc.vi.md` and the target is `base`, the output will be `mydoc.md`.
- The content will be translated into the project's primary language (defaults to English).

## Workflow

1. **Argument Parsing**:

   - Identify the source file and source language.
   - Iterate through target languages. If `base` is requested, resolve the target filename by stripping the language suffix from the source filename (e.g., `.vi.md` -> `.md`).
2. **Translation**:

   - Translate content into each target language.
   - **Preservation**: Strictly maintain Markdown structure, including tables, lists, and **code blocks**. Do NOT translate content inside code fences (```) unless explicitly requested.
   - **Terminology**: Keep standard technical terms in English if commonly used in the local developer community (e.g., JavaScript, API).
3. **File Writing**:

   - For language codes (e.g., `ja`): `[Name].[code].md`.
   - For `base` keyword: `[Name].md`.
   - Write files to the same directory as the source.
4. **Language Nav (Language Switcher)**:

   - Insert a navigation line at the top of each file (after Front Matter).
   - Format: `[Tiếng Việt](README.md) | [English](README.en.md) | [日本語](README.ja.md)`
   - Ensure the `base` file and all variants are updated to include links to all currently generated versions.
5. **Internal Link Update**:

   - Update internal links to other `.md` files to point to their corresponding language versions if they exist.

## Important Notes

- Maintain the original document's tone and formatting.
- Do not break URLs or image links.
- Summarize the final list of created or updated files.
