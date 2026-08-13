import re

from database.db import (
    execute,
    fetch_one,
    fetch_all
)


# ==================================================
# REGEX
# ==================================================

WIKI_PATTERN = re.compile(
    r"\[\[(.*?)\]\]"
)


# ==================================================
# EXTRACT LINKS
# ==================================================

def extract_wiki_links(content):
    """
    Tìm tất cả [[Note Name]]
    """

    links = WIKI_PATTERN.findall(content)

    return sorted(set(links))


# ==================================================
# SYNC DATABASE
# ==================================================

def sync_wiki_links(
    source_note_id,
    content
):
    """
    Đồng bộ wiki links của 1 note.
    """

    # Xóa liên kết cũ

    execute(
        """
        DELETE FROM wiki_links
        WHERE source_note_id = ?
        """,
        (source_note_id,)
    )

    targets = extract_wiki_links(content)

    for title in targets:

        target = fetch_one(
            """
            SELECT id
            FROM nodes
            WHERE
                title = ?
                AND type = 'note'
            """,
            (title,)
        )

        if not target:
            continue

        execute(
            """
            INSERT OR IGNORE
            INTO wiki_links(
                source_note_id,
                target_note_id
            )
            VALUES (?, ?)
            """,
            (
                source_note_id,
                target["id"]
            )
        )


# ==================================================
# OUTGOING LINKS
# ==================================================

def get_outgoing_links(note_id):
    """
    Các note mà note hiện tại đang tham chiếu tới.
    """

    return fetch_all(
        """
        SELECT
            n.id,
            n.title
        FROM wiki_links wl

        JOIN nodes n
            ON n.id = wl.target_note_id

        WHERE wl.source_note_id = ?

        ORDER BY n.title
        """,
        (note_id,)
    )


# ==================================================
# BACKLINKS
# ==================================================

def get_backlinks(note_id):
    """
    Các note đang tham chiếu tới note hiện tại.
    """

    return fetch_all(
        """
        SELECT
            n.id,
            n.title
        FROM wiki_links wl

        JOIN nodes n
            ON n.id = wl.source_note_id

        WHERE wl.target_note_id = ?

        ORDER BY n.title
        """,
        (note_id,)
    )


# ==================================================
# NOTE EXISTENCE
# ==================================================

def get_note_by_title(title):
    """
    Tìm note theo title.
    """

    return fetch_one(
        """
        SELECT *
        FROM nodes
        WHERE
            title = ?
            AND type = 'note'
        """,
        (title,)
    )