# services/tags.py

import re

from database.db import (
    execute,
    fetch_one,
    fetch_all
)

TAG_PATTERN = re.compile(
    r"#([a-zA-Z0-9_-]+)"
)


def extract_tags(content):

    tags = TAG_PATTERN.findall(content)

    return sorted(set(tags))


def save_note_tags(note_id, tags):

    # Xóa liên kết tag cũ

    execute(
        """
        DELETE FROM note_tags
        WHERE note_id = ?
        """,
        (note_id,)
    )

    # Thêm tag mới

    for tag_name in tags:

        execute(
            """
            INSERT OR IGNORE
            INTO tags(name)
            VALUES(?)
            """,
            (tag_name,)
        )

        tag = fetch_one(
            """
            SELECT id
            FROM tags
            WHERE name = ?
            """,
            (tag_name,)
        )

        if tag:

            execute(
                """
                INSERT OR IGNORE
                INTO note_tags(
                    note_id,
                    tag_id
                )
                VALUES (?, ?)
                """,
                (
                    note_id,
                    tag["id"]
                )
            )


def get_note_tags(note_id):

    return fetch_all(
        """
        SELECT t.*
        FROM tags t

        JOIN note_tags nt
            ON nt.tag_id = t.id

        WHERE nt.note_id = ?

        ORDER BY t.name
        """,
        (note_id,)
    )