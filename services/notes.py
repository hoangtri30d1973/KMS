# services/notes.py

from database.db import execute, fetch_one, fetch_all


# ==================================================
# CREATE
# ==================================================

def create_folder(title, parent_id=None):
    """
    Tạo thư mục mới.
    """

    return execute(
        """
        INSERT INTO nodes (
            parent_id,
            type,
            title
        )
        VALUES (?, 'folder', ?)
        """,
        (parent_id, title)
    )


def create_note(title, content="", parent_id=None):
    """
    Tạo note mới.
    """

    return execute(
        """
        INSERT INTO nodes (
            parent_id,
            type,
            title,
            content
        )
        VALUES (?, 'note', ?, ?)
        """,
        (
            parent_id,
            title,
            content
        )
    )


# ==================================================
# READ
# ==================================================

def get_node(node_id):
    """
    Lấy thông tin node theo id.
    """

    return fetch_one(
        """
        SELECT *
        FROM nodes
        WHERE id = %s
        """,
        (node_id,)
    )


def get_children(parent_id):
    """
    Lấy danh sách node con.
    Folder được sắp trước Note.
    """

    return fetch_all(
        """
        SELECT *
        FROM nodes
        WHERE parent_id = %s
        ORDER BY
            CASE
                WHEN type = 'folder' THEN 0
                ELSE 1
            END,
            title
        """,
        (parent_id,)
    )


def get_root_nodes():
    """
    Lấy các node gốc.
    """

    return fetch_all(
        """
        SELECT *
        FROM nodes
        WHERE parent_id IS NULL
        ORDER BY
            CASE
                WHEN type = 'folder' THEN 0
                ELSE 1
            END,
            title
        """
    )


# ==================================================
# UPDATE
# ==================================================

def update_node(node_id, title=None, content=None):
    """
    Cập nhật title và content.
    """

    node = get_node(node_id)

    if not node:
        return False

    title = title if title is not None else node["title"]
    content = content if content is not None else node["content"]

    execute(
        """
        UPDATE nodes
        SET
            title = ?,
            content = ?
        WHERE id = %s
        """,
        (
            title,
            content,
            node_id
        )
    )

    return True


def rename_node(node_id, new_title):
    """
    Đổi tên folder hoặc note.
    """

    execute(
        """
        UPDATE nodes
        SET title = ?
        WHERE id = %s
        """,
        (
            new_title,
            node_id
        )
    )

    return True


def move_node(node_id, new_parent_id):
    """
    Di chuyển node sang thư mục khác.
    """

    execute(
        """
        UPDATE nodes
        SET parent_id = ?
        WHERE id = %s
        """,
        (
            new_parent_id,
            node_id
        )
    )

    return True


# ==================================================
# DELETE
# ==================================================

def delete_node(node_id):
    """
    Xóa node.
    Nếu SQLite bật foreign keys thì
    cây con sẽ bị xóa theo cascade.
    """

    execute(
        """
        DELETE FROM nodes
        WHERE id = %s
        """,
        (node_id,)
    )

    return True


# ==================================================
# SEARCH
# ==================================================

def search_notes(keyword):
    """
    Tìm kiếm theo title hoặc content.
    """

    like_keyword = f"%{keyword}%"

    return fetch_all(
        """
        SELECT *
        FROM nodes
        WHERE
            title LIKE ?
            OR content LIKE ?
        ORDER BY title
        """,
        (
            like_keyword,
            like_keyword
        )
    )


# ==================================================
# TREE
# ==================================================

def build_tree(parent_id=None):
    """
    Xây dựng cây thư mục đệ quy.
    """

    if parent_id is None:

        nodes = fetch_all(
            """
            SELECT *
            FROM nodes
            WHERE parent_id IS NULL
            ORDER BY
                CASE
                    WHEN type = 'folder' THEN 0
                    ELSE 1
                END,
                title
            """
        )

    else:

        nodes = fetch_all(
            """
            SELECT *
            FROM nodes
            WHERE parent_id = %s
            ORDER BY
                CASE
                    WHEN type = 'folder' THEN 0
                    ELSE 1
                END,
                title
            """,
            (parent_id,)
        )

    result = []

    for node in nodes:

        node_data = {
            "id": node["id"],
            "title": node["title"],
            "type": node["type"],
            "children": []
        }

        if node["type"] == "folder":
            node_data["children"] = build_tree(node["id"])

        result.append(node_data)

    return result


# ==================================================
# UTILITIES
# ==================================================

def is_folder(node_id):
    """
    Kiểm tra node có phải folder không.
    """

    node = get_node(node_id)

    return (
        node is not None
        and node["type"] == "folder"
    )


def is_note(node_id):
    """
    Kiểm tra node có phải note không.
    """

    node = get_node(node_id)

    return (
        node is not None
        and node["type"] == "note"
    )

def get_breadcrumb(node_id):
    """
    Trả về breadcrumb của node hiện tại.

    Ví dụ:
    Main / Python / SQLAlchemy
    """

    breadcrumb = []

    current = get_node(node_id)

    while current:

        breadcrumb.append(current["title"])

        parent_id = current["parent_id"]

        if parent_id is None:
            break

        current = get_node(parent_id)

    breadcrumb.reverse()

    return breadcrumb
