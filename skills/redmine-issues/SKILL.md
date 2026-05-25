---
name: redmine-issues
description: Creates and updates Redmine issues via the REST API (JSON), including child issues under a parent, default assignee (owner) from .env (login or id), assigned_to, UTF-8-safe payloads on Windows to avoid mojibake for Japanese/Vietnamese text. Use when the user mentions Redmine, Redmine API, tasks/tickets/issues, parent tasks, assignee, owner, trackers, UTF-8, encoding, or mojibake (文字化け) on Redmine.
---

# Redmine issues (REST API)

## Configuration

Resolve **`REDMINE_BASE_URL`** and **`REDMINE_API_KEY`** in this order:

1. **Process environment** — if both variables are set and non-empty, use them.
2. **Skill `.env` file** — if any required key is missing from the environment, read the file **`.env`** in the same directory as this skill’s `SKILL.md` (typical path: `~/.cursor/skills/redmine-issues/.env` on macOS/Linux, `%USERPROFILE%\.cursor\skills\redmine-issues\.env` on Windows). Parse the keys below; merge with env so **process env wins** for any key already set.
3. **Still missing** (only `REDMINE_BASE_URL` / `REDMINE_API_KEY`) — ask the user once per session; never guess values.

**`.env` format:** one `KEY=value` per line; UTF-8; ignore blank lines and lines whose first non-space character is `#`; trim spaces around `=`; strip one pair of surrounding `"` from values if present.

| Variable | Required | Meaning |
|----------|----------|---------|
| `REDMINE_BASE_URL` | yes | Origin only, no trailing slash (e.g. `https://redmine.example.com`) |
| `REDMINE_API_KEY` | yes | **My account** → **API access key** (authentication only; never commit `.env` or paste keys into a repo) |
| `REDMINE_DEFAULT_ASSIGNED_TO_LOGIN` | no | Default **owner / 担当者** — Redmine login (e.g. `thanh_tt`). Resolved to `assigned_to_id` before POST/PUT. |
| `REDMINE_DEFAULT_ASSIGNED_TO_ID` | no | Default assignee as numeric user id (e.g. `7`). If set, used **instead of** `REDMINE_DEFAULT_ASSIGNED_TO_LOGIN` (no login lookup). |

**API key vs assignee:** `REDMINE_API_KEY` identifies who **calls** the API (issue **author** on create, **journal updater** on PUT). It does **not** set the assignee unless you also set default assignee vars or pass assignee in the user request. Do **not** call `GET /users/current.json` on every issue solely to pick an assignee when `.env` already defines one.

All requests:

- Header: `X-Redmine-API-Key: $REDMINE_API_KEY`
- Header: `Content-Type: application/json; charset=utf-8` (include `charset=utf-8` whenever the body may contain non-ASCII text)
- Accept JSON: append `.json` to resource paths or send `Accept: application/json`

## UTF-8 / mojibake (Japanese, Vietnamese, etc.)

Redmine expects **UTF-8** JSON bodies. On **Windows**, OEM/ANSI code pages (e.g. CP932) often corrupt Unicode if the HTTP client re-encodes the body or the shell mangles literals — symptoms: Unicode replacement characters (U+FFFD), wrong kanji, or “random” Latin mojibake in **issue subject/description in the browser**.

### Before POST/PUT (agent checklist)

- [ ] JSON serialized as UTF-8 **bytes** on the wire (not CP932/1252).
- [ ] Header includes **`charset=utf-8`** whenever `subject`, `description`, `notes`, or custom text fields may be non-ASCII.
- [ ] Scripts that build JSON from files: read sources with **UTF-8** (`Get-Content -Encoding UTF8`, editor “UTF-8”).
- [ ] After create/update, if unsure: **GET** `/issues/{id}.json` and compare `subject` to the user’s expected string (quick verification).

### PowerShell (mandatory pattern on Windows for non-ASCII)

Build the JSON string first, then send **UTF-8 bytes** (works on **5.1** and **7+**):

```powershell
$json = $bodyObject | ConvertTo-Json -Depth 10 -Compress
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
Invoke-RestMethod -Uri "$base/issues.json" -Method Post `
  -ContentType 'application/json; charset=utf-8' `
  -Headers @{ 'X-Redmine-API-Key' = $apiKey } `
  -Body $bytes
```

Same for **`PUT /issues/{id}.json`**. Do **not** rely on `-Body $json` as a **string** on Windows PowerShell 5.1 for Japanese/Vietnamese-heavy payloads.

**Avoid:** embedding large scripts in `powershell -Command "..."` from another shell — `$` and quotes are often stripped or altered, producing silent logic errors or wrong encoding paths. Prefer a **`.ps1` file** saved as UTF-8 and `powershell -File script.ps1`.

### curl.exe (Windows)

Write `payload.json` as **UTF-8** (prefer **without BOM**). Then:

```text
curl.exe -sS -X POST "%REDMINE_BASE_URL%/issues.json" ^
  -H "X-Redmine-API-Key: %REDMINE_API_KEY%" ^
  -H "Content-Type: application/json; charset=utf-8" ^
  --data-binary "@payload.json"
```

Avoid piping non-UTF-8 console text into `-d`.

### `.env` and literals

- Load skill `.env` with **`Get-Content -Encoding UTF8`** (see **Configuration**).
- Pasting Japanese/Vietnamese into a **non-UTF-8** cmd window before it reaches a file can corrupt text; prefer editing `payload.json` / `.ps1` in the editor with UTF-8.

### Terminal display vs stored data

If **Redmine in the browser** is correct but **terminal output** is garbled: the API payload is likely fine — adjust **console UTF-8** (e.g. `chcp 65001`, Windows Terminal, `[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)` for display only).

### Other stacks

Any HTTP client is safe if it sends the raw JSON **octets as UTF-8** and sets **`Content-Type: application/json; charset=utf-8`**. (Example: Laravel `Http::withBody($json, 'application/json; charset=utf-8')` with `$json` built as UTF-8 string from UTF-8 source files.)

## Assignee (owner / 担当者)

Redmine stores the assignee as **`assigned_to_id`** (numeric user id). The REST API has **no** “assign by login” field — resolve login to id once, then send `assigned_to_id`.

### Priority when choosing `assigned_to_id`

1. **User request** in the prompt — numeric id or login (e.g. `assigned to thanh_tt`, `担当 thanh_tt`).
2. Else **`REDMINE_DEFAULT_ASSIGNED_TO_ID`** from process env or skill `.env`.
3. Else **`REDMINE_DEFAULT_ASSIGNED_TO_LOGIN`** → resolve to id (see below).
4. Else **omit** `assigned_to_id` (Redmine default / unassigned).

Prefer **login in `.env`** for readability; use **id** when you want zero lookup. If both id and login are set in config, **id wins**.

### Resolve login → `assigned_to_id`

- **Already numeric** (user id or env `REDMINE_DEFAULT_ASSIGNED_TO_ID`) → use as `assigned_to_id`.
- **Login `me`** (or user says “assign to me”) → `GET /users/current.json` with the API key and use `user.id`; or send `assigned_to_id` as the string `"me"` where your Redmine version accepts it for create.
- **Other login** (e.g. `thanh_tt`), after `project_id` is known:
  - **Non-admin API key:** `GET /projects/{project_id}/memberships.json` (paginate with `offset` / `limit`). For each membership with a `user` object, match `user.login`; use `user.id`. Groups are not valid assignees as users — skip or expand group members if needed.
  - **Admin API key:** `GET /users.json?status=1&limit=100` (paginate) and match `login`; or `GET /users/{id}.json` if id is already known.

If no match or user is not a project member, creation/update may return **422** — report the error and ask the user to fix login or project membership.

### Unassign

Only when the user asks to clear the assignee: set `assigned_to_id` to `""` in JSON (per Redmine wiki).

### Author and updater (not assignee)

- **Author** on create = user owning `REDMINE_API_KEY` (unless admin uses `X-Redmine-Switch-User`).
- **Updater** on PUT (journal) = same API user. Optional discovery: `GET /users/current.json` — do not confuse with assignee defaults.

## Resolve IDs before creating issues

When the user gives **names** instead of numeric IDs, query first:

- **Project**: `GET /projects/{identifier}.json` — `identifier` can be project key (e.g. `myapp`) or numeric id.
- **Trackers** for a project: `GET /projects/{identifier}.json` includes `project.trackers[]` with `id` and `name`.
- **Statuses / priorities**: `GET /issues/statuses.json`, or known IDs from the user.
- **Assignee**: follow **Assignee (owner / 担当者)** above (not from API key by default).

## Create an issue

`POST {REDMINE_BASE_URL}/issues.json`

Body shape:

```json
{
  "issue": {
    "project_id": 1,
    "tracker_id": 2,
    "subject": "Short title",
    "description": "Optional longer text",
    "status_id": 1,
    "priority_id": 2,
    "assigned_to_id": 3
  }
}
```

Omit fields the user did not specify; Redmine applies defaults where allowed. Include **`assigned_to_id`** when resolved from user request or default assignee config.

## Child issue (parent task)

Set **`parent_issue_id`** inside `issue` (integer id of the existing parent issue):

```json
{
  "issue": {
    "project_id": 1,
    "tracker_id": 2,
    "subject": "Sub-task under #1234",
    "parent_issue_id": 1234
  }
}
```

**Note:** Parent and child are usually in the same project; if creation fails, confirm project/tracker compatibility with the parent.

## Update, read, list

- **Read:** `GET /issues/{id}.json`
- **Update:** `PUT /issues/{id}.json` with `{ "issue": { ...partial fields... } }` — apply the same **UTF-8 / mojibake** rules as POST when updating text fields. Include `assigned_to_id` to change assignee; journal author remains the API key user unless using admin impersonation headers.
- **List/filter:** `GET /issues.json?project_id=1&parent_id=1234` (query params vary by Redmine version/plugins; adjust if empty)

## Example (curl)

Replace placeholders; on Windows PowerShell use `curl.exe` or `Invoke-RestMethod`.

```bash
curl -sS -X POST "${REDMINE_BASE_URL}/issues.json" \
  -H "X-Redmine-API-Key: ${REDMINE_API_KEY}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{"issue":{"project_id":1,"tracker_id":2,"subject":"New task","assigned_to_id":7,"parent_issue_id":1234}}'
```

Successful create returns **201** and JSON including `issue.id`.

## Agent workflow

1. Resolve `REDMINE_BASE_URL` and `REDMINE_API_KEY` using **Configuration** (env → skill `.env` → ask user). Load optional `REDMINE_DEFAULT_ASSIGNED_TO_ID` / `REDMINE_DEFAULT_ASSIGNED_TO_LOGIN` from the same sources. Do not store secrets in the workspace repository.
2. When creating/updating issues with **Japanese, Vietnamese, or other non-ASCII** text, follow **UTF-8 / mojibake** so payloads are not corrupted on Windows.
3. Resolve `project_id` / `tracker_id` if the user gave names.
4. Resolve **`assigned_to_id`** per **Assignee (owner / 担当者)** (after `project_id` is known if login lookup is needed).
5. `POST /issues.json` (or `PUT /issues/{id}.json`) with `parent_issue_id` when applicable and `assigned_to_id` when resolved.
6. Report back the new **issue id** and Redmine URL path `/issues/{id}` when useful; optionally verify assignee via `GET /issues/{id}.json` → `assigned_to`.

## Errors

- **401/403**: API key or role permissions (project membership, tracker permissions).
- **422**: Validation — response body lists errors; often wrong `project_id`, read-only status, invalid `assigned_to_id` (user not in project / not assignable), or missing required custom fields. Ask the user or inspect `errors` in JSON.

## Further reading

Official wiki: [Redmine REST API](https://www.redmine.org/projects/redmine/wiki/Rest_api) — issue properties and version differences.
