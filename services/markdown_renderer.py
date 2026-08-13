import re

from markdown_it import MarkdownIt

md = (
    MarkdownIt(
        "commonmark",
        {
            "html": True
        }
    )
    .enable("table")
)

WIKI_PATTERN = re.compile(r"\[\[(.*?)\]\]")
TAG_PATTERN = re.compile(r"#([a-zA-Z0-9_-]+)")


def process_wiki_links(content: str) -> str:

    def replace(match):
        title = match.group(1)

        return (
            f'?note={title}'
        )

    return WIKI_PATTERN.sub(replace, content)


def extract_tags(content: str):

    tags = TAG_PATTERN.findall(content)

    return sorted(set(tags))


def render_markdown(content: str) -> str:

    content = process_wiki_links(content)

    return md.render(content)