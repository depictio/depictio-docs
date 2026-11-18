"""Syntax highlighting for Nextflow code blocks (```nextflow, ```nf).

Pygments has no Nextflow lexer. Nextflow is a Groovy DSL, so this one is the
Groovy lexer plus Nextflow's own keywords (process, workflow, include, take,
emit, input, output, ...) and builtins (Channel, params, tuple, path, val, ...).

It is registered in Pygments' lexer table when MkDocs loads the hook, before any
page is rendered, so pymdownx.highlight finds it by name like a bundled lexer.
"""

from __future__ import annotations

from pygments import lexers
from pygments.lexer import inherit, words
from pygments.lexers.jvm import GroovyLexer
from pygments.token import Keyword, Name


class NextflowLexer(GroovyLexer):
    name = "Nextflow"
    aliases = ["nextflow", "nf"]
    filenames = ["*.nf", "nextflow.config"]
    mimetypes: list[str] = []

    tokens = {
        "base": [
            (
                words(
                    (
                        "process", "workflow", "include", "from", "take", "main", "emit",
                        "input", "output", "script", "shell", "exec", "stub", "when",
                        "publish", "onComplete", "onError", "includeConfig", "params",
                        "profiles", "withName", "withLabel",
                    ),
                    suffix=r"\b",
                ),
                Keyword,
            ),
            (
                words(
                    (
                        "Channel", "channel", "tuple", "val", "path", "file", "env", "each",
                        "stdin", "stdout", "task", "log", "projectDir", "launchDir",
                        "moduleDir", "baseDir",
                    ),
                    suffix=r"\b",
                ),
                Name.Builtin,
            ),
            inherit,
        ],
    }


def _register() -> None:
    entry = ("hooks.nextflow_lexer", NextflowLexer.name, tuple(NextflowLexer.aliases),
             tuple(NextflowLexer.filenames), ())
    lexers.LEXERS["NextflowLexer"] = entry
    lexers._lexer_cache[NextflowLexer.name] = NextflowLexer


_register()
