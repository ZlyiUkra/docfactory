"""Читач обговорень GitHub: кожен issue репозиторію разом з усіма коментарями — документ.

`ghissues` — `url` — перелік issues через API
             (…/repos/ВЛАСНИК/РЕПО/issues?state=all&per_page=100); сторінки гортаються
             параметром page, доки не прийде неповна. API віддає в тому ж переліку й
             pull request-и — вони відкидаються: беруться лише issues. `label` — назва
             в заголовку документа («WebAssembly spec issue»). У `within`, крім самої
             адреси переліку, — тека «…/issues/»: звідти беруться коментарі.

Навіщо. Специфікація каже, як є, а issues — чому саме так: тут питання про
неоднозначні місця тексту, відповіді редакторів, помилки, знайдені реалізаціями, і
пропозиції, що так і не стали нормою. Для питання «чому це правило таке» чи «це баг
специфікації чи реалізації» відповідь часто лише тут.

Документ: шапка (хто й коли відкрив, стан, мітки), текст issue і кожен коментар
окремим розділом «## Comment by АВТОР, ДАТА» — так пошук повертає саме ту репліку, що
відповідає, а не весь тред. Коментарі тягнуться під час запису документа, лише для
issues, у яких вони є. Версії в обговорення немає: воно стосується специфікації
загалом, а не одного її видання.
"""

import json
import re
from urllib.parse import parse_qs, urlsplit

from engine.readers import Item, _markup, register

_ISSUES = re.compile(r"^/repos/([^/]+)/([^/]+)/issues$")


def _json(ctx, url: str):
    try:
        return json.loads(ctx.text(url))
    except ValueError as exc:
        raise SystemExit(f"{url}: відповідь не JSON ({exc}) — перелік не складено.")


def _pages(ctx, base: str, per_page: int) -> list:
    out: list = []
    for page in range(1, 1001):
        url = base if page == 1 else f"{base}{'&' if '?' in base else '?'}page={page}"
        batch = _json(ctx, url)
        if not isinstance(batch, list):
            raise SystemExit(f"{url}: очікував список.")
        out.extend(batch)
        if len(batch) < per_page:
            break
    return out


def _who(obj: dict) -> str:
    return str((obj.get("user") or {}).get("login") or "?")


@register("ghissues")
def ghissues(source: dict, ctx) -> list[Item]:
    base = source["url"]
    if not _ISSUES.match(urlsplit(base).path):
        raise SystemExit(f"{base}: очікував адресу /repos/ВЛАСНИК/РЕПО/issues.")
    per_page = int((parse_qs(urlsplit(base).query).get("per_page") or ["30"])[0])
    label = source.get("label", "Issue")
    items = []
    for issue in _pages(ctx, base, per_page):
        if not isinstance(issue, dict) or issue.get("pull_request") or not issue.get("number"):
            continue
        # Лише потрібне: повний запис issue великий, а тисяча таких у пам'яті зайві.
        meta = {
            "number": issue["number"], "title": str(issue.get("title") or ""),
            "url": str(issue.get("html_url") or ""), "who": _who(issue),
            "opened": str(issue.get("created_at") or "")[:10],
            "closed": str(issue.get("closed_at") or "")[:10],
            "state": str(issue.get("state") or ""),
            "reason": str(issue.get("state_reason") or ""),
            "labels": [str(lb.get("name")) for lb in issue.get("labels") or []
                       if isinstance(lb, dict)],
            "body": str(issue.get("body") or ""),
            "comments": int(issue.get("comments") or 0),
            "comments_url": str(issue.get("comments_url") or ""),
        }

        def make(m=meta):
            state = m["state"] + (f" ({m['reason']})" if m["reason"] else "")
            if m["closed"]:
                state += f" on {m['closed']}"
            head = [f"Issue #{m['number']}, opened by {m['who']} on {m['opened']}, {state}."]
            if m["labels"]:
                head.append("Labels: " + ", ".join(m["labels"]) + ".")
            parts = [" ".join(head), "", _markup.markdown_body(m["body"]) or "(no description)"]
            if m["comments"] and m["comments_url"]:
                # Тихо пропустити коментарі — це записати тред без відповідей, що
                # виглядає як повний: заборонена адреса — збій документа.
                if not ctx.allowed(m["comments_url"]):
                    raise SystemExit(f"{m['comments_url']}: коментарі поза білим списком — "
                                     f"додайте теку …/issues/ у within.")
                for c in _pages(ctx, f"{m['comments_url']}?per_page=100", 100):
                    if not isinstance(c, dict):
                        continue
                    text = _markup.markdown_body(str(c.get("body") or ""))
                    if not text:
                        continue
                    day = str(c.get("created_at") or "")[:10]
                    parts += ["", f"## Comment by {_who(c)}, {day}", "", text]
            title = f"{label} #{m['number']}: {m['title']}"
            return _markup.document(title, m["url"], ctx.stamp, "\n".join(parts).strip() + "\n")

        items.append(Item(id=f"{source['id']}/{meta['number']}",
                          file=f"{source['id']}--{meta['number']:05d}.txt", make=make))
    if not items:
        raise SystemExit(f"{base}: жодного issue.")
    return items
