"""Читач історії сторінок man у форматі Perl POD з багатьох тегів одного репозиторію (OpenSSL).

`ghdocs-history-pod` — файли `.pod` і `.pod.in` з багатьох тегів разом. Поля ті самі, що в `ghdocs-history`
                      (`url`, `tags`, `folders`, `recursive`, `extensions`, `exclude`, `name_prefix` …). Текст
                      кожного такого файла перед звичайним розбором стає markdown.

Навіщо. Документація OpenSSL — сторінки man у POD: `=head1 NAME`, `=over`/`=item`/`=back`, відступлені абзаци
коду, вбудовані коди `B<-in>`, `I<файл>`, `C<…>`, `L<…>`, `E<lt>`. Спільні читачі markdown цього не знають: файл
лягав би текстом із сирими `B<` і `=head1`. У 3.x сторінки команд — шаблони `.pod.in`, де Perl вставляє частину
тексту (`{- … -}`); ці вставки лишаються поза текстом, бо без збирання проєкту їх не обчислити.

Що виходить. Заголовок документа — перше ім'я з розділу NAME і короткий опис; `=head1` стає «##», `=head2` —
«###», пункти `=item` — жирним рядком (опції команд) чи пунктом переліку (`*`), абзац з відступом — блоком коду.

Чому окремий модуль, а не поле в `ghdocs-history`: спільний читач звірено в багатьох готових примірниках, а тут
досить підмінити текст файла, перш ніж читач його розбере.
"""

import re

from engine.readers import register
from engine.readers.ghhistory import ghdocs_history

_PERL = re.compile(r"\{-.*?-\}", re.S)
_ENTITY = {"lt": "&lt;", "gt": "&gt;", "sol": "/", "verbar": "|", "quot": '"', "amp": "&amp;",
           "apos": "'", "lbrace": "{", "rbrace": "}", "num": "#", "percnt": "%", "nbsp": " ",
           "copy": "(c)", "reg": "(R)", "ndash": "-", "mdash": "—", "eacute": "é", "oacute": "ó",
           "uuml": "ü", "ouml": "ö", "auml": "ä", "szlig": "ß", "ccedil": "ç", "aacute": "á",
           "iacute": "í", "uacute": "ú", "ntilde": "ñ", "egrave": "è", "agrave": "à",
           "ecirc": "ê", "ocirc": "ô", "acirc": "â", "Oslash": "Ø", "oslash": "ø", "aring": "å",
           "Aring": "Å", "Eacute": "É", "Ouml": "Ö", "Uuml": "Ü", "Auml": "Ä", "zcaron": "ž",
           "scaron": "š", "ccaron": "č"}
_SIMPLE = re.compile(r"\b([BICFSXZEL])<([^<>]*)>")
_DOUBLE = re.compile(r"\b([BICFSXZEL])<<+\s+(.*?)\s+>>+", re.S)


def _code(m) -> str:
    kind, body = m.group(1), m.group(2)
    if kind == "B":
        return f"**{body}**" if body.strip() else ""
    if kind == "I":
        return f"*{body}*" if body.strip() else ""
    if kind in ("C", "F"):
        return f"`{body}`" if body.strip() else ""
    if kind == "S":
        return body.replace(" ", " ") if False else body
    if kind in ("X", "Z"):
        return ""
    if kind == "E":
        if body in _ENTITY:
            return _ENTITY[body]
        if body.isdigit():
            return chr(int(body))
        if re.fullmatch(r"0x[0-9a-fA-F]+", body):
            return chr(int(body, 16))
        return body
    if kind == "L":
        # L<текст|ціль> → текст; L<ім'я(3)> → ім'я; L<https://…> → адреса
        if "|" in body:
            return body.split("|", 1)[0]
        return re.sub(r"^\"|\"$", "", body.split("/", 1)[-1] if "/" in body and not "://" in body
                      else body)
    return body


def _inline(text: str) -> str:
    """Вбудовані коди POD, найвужчі першими: `B<-I<digest>>` розкривається зсередини."""
    for _ in range(6):
        new = _DOUBLE.sub(_code, text)
        new = _SIMPLE.sub(_code, new)
        if new == text:
            break
        text = new
    return text


def _name_title(paragraph: str, stem: str = "") -> str:
    """Назва сторінки: ім'я, що збігається з назвою файла, інакше перше з розділу NAME."""
    text = " ".join(_inline(paragraph).split())
    names, _, desc = text.partition(" - ")
    listed = [n.strip().strip("`*") for n in names.split(",")]
    first = listed[0]
    for n in listed:
        if stem and n.lower() == stem.lower():
            first = n
            break
    return f"{first} - {desc}".strip(" -") if desc else first


def pod_to_markdown(src: str, stem: str = "") -> str:
    """POD → markdown з одним заголовком першого рівня (назва сторінки) і розділами «##»."""
    text = _PERL.sub("", src.replace("\r\n", "\n"))
    out: list[str] = []
    verbatim: list[str] = []
    skip_block = False
    in_name, title_done = False, False
    for para in re.split(r"\n[ \t]*\n", text):
        if not para.strip():
            continue
        first = para.lstrip("\n")
        if first.startswith("=") and re.match(r"=[a-zA-Z]", first):
            if verbatim:
                out.extend(["", "```", "\n".join(verbatim).rstrip(), "```", ""])
                verbatim = []
            cmd, _, rest = first.partition("\n")[0].partition(" ")
            rest = (rest + "\n" + first.partition("\n")[2]).strip() if "\n" in first else rest.strip()
            if cmd in ("=begin", "=for"):
                kind = rest.split()[0] if rest.split() else ""
                if cmd == "=begin" and kind in ("comment", "man", "html", "text", "latex", "roff"):
                    skip_block = True
                continue
            if cmd == "=end":
                skip_block = False
                continue
            if skip_block or cmd in ("=pod", "=cut", "=encoding", "=over", "=back"):
                continue
            if cmd.startswith("=head"):
                level = min(int(cmd[5:] or 1), 4)
                head = " ".join(_inline(rest).split())
                in_name = level == 1 and head.upper() == "NAME"
                if level == 1:
                    in_name = head.upper() == "NAME"
                if not in_name or title_done:
                    out.extend(["", "#" * (level + 1) + " " + head, ""])
                continue
            if cmd == "=item":
                item = " ".join(_inline(rest.partition("\n")[0]).split())
                body = _inline(rest.partition("\n")[2]).strip()
                if item in ("*", "-"):
                    out.extend(["", "- " + " ".join(body.split()) if body else "-", ""])
                elif re.fullmatch(r"\[?\d+\.?\]?", item):
                    out.extend(["", f"{item} " + " ".join(body.split()), ""])
                else:
                    out.extend(["", item if item.startswith("**") and item.endswith("**")
                                else f"**{item}**", ""])
                    if body:
                        out.extend([body, ""])
                continue
            continue
        if skip_block:
            continue
        if first[:1] in (" ", "\t"):
            verbatim.extend(first.rstrip().split("\n"))
            verbatim.append("")
            continue
        if verbatim:
            out.extend(["", "```", "\n".join(verbatim).rstrip(), "```", ""])
            verbatim = []
        if in_name and not title_done:
            title = _name_title(para, stem)
            out.insert(0, f"# {title}")
            out.extend(["", "## NAME", "", " ".join(_inline(para).split()), ""])
            title_done = True
            continue
        out.extend(["", _inline(para).strip(), ""])
    if verbatim:
        out.extend(["", "```", "\n".join(verbatim).rstrip(), "```", ""])
    if not title_done:
        out.insert(0, "# manual page")
    return "\n".join(out)


class _Ctx:
    """Той самий контекст завантаження, лише текст файлів POD проходить `pod_to_markdown`."""

    def __init__(self, ctx):
        self._ctx = ctx

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    def text(self, url: str, *args, **kwargs) -> str:
        text = self._ctx.text(url, *args, **kwargs)
        path = url.split("?", 1)[0]
        if not re.search(r"\.pod(\.in)?$", path):
            return text
        stem = re.sub(r"\.pod(\.in)?$", "", path.rsplit("/", 1)[-1])
        return pod_to_markdown(text, stem)


@register("ghdocs-history-pod")
def ghdocs_history_pod(source: dict, ctx):
    return ghdocs_history(source, _Ctx(ctx))
