from database.db import execute

def create_nodes_table():
    query = """
    CREATE TABLE IF NOT EXISTS nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        parent_id INTEGER,

        type TEXT NOT NULL
            CHECK(type IN ('folder', 'note')),

        title TEXT NOT NULL,

        content TEXT DEFAULT '',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(parent_id)
            REFERENCES nodes(id)
            ON DELETE CASCADE
    );
    """

    execute(query)


def create_tags_table():

    execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS note_tags (
        note_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,

        PRIMARY KEY (note_id, tag_id),

        FOREIGN KEY (note_id)
            REFERENCES nodes(id)
            ON DELETE CASCADE,

        FOREIGN KEY (tag_id)
            REFERENCES tags(id)
            ON DELETE CASCADE
    )
    """)


def create_wiki_links_table():

    execute("""
    CREATE TABLE IF NOT EXISTS wiki_links (

        source_note_id INTEGER NOT NULL,

        target_note_id INTEGER NOT NULL,

        PRIMARY KEY (
            source_note_id,
            target_note_id
        ),

        FOREIGN KEY (source_note_id)
            REFERENCES nodes(id)
            ON DELETE CASCADE,

        FOREIGN KEY (target_note_id)
            REFERENCES nodes(id)
            ON DELETE CASCADE

    )
    """)


def create_indexes():

    execute("""
        CREATE INDEX IF NOT EXISTS idx_nodes_parent
        ON nodes(parent_id)
    """)

    execute("""
        CREATE INDEX IF NOT EXISTS idx_nodes_type
        ON nodes(type)
    """)

    execute("""
        CREATE INDEX IF NOT EXISTS idx_note_tags_note
        ON note_tags(note_id)
    """)

    execute("""
        CREATE INDEX IF NOT EXISTS idx_note_tags_tag
        ON note_tags(tag_id)
    """)

    execute("""
        CREATE INDEX IF NOT EXISTS idx_wiki_source
        ON wiki_links(source_note_id)
    """)

    execute("""
        CREATE INDEX IF NOT EXISTS idx_wiki_target
        ON wiki_links(target_note_id)
    """)


def create_triggers():
    execute("""
        CREATE TRIGGER IF NOT EXISTS update_nodes_updated_at
        AFTER UPDATE ON nodes
        FOR EACH ROW
        BEGIN
            UPDATE nodes
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = OLD.id;
        END;
    """)


def initialize_database():

    create_nodes_table()

    create_tags_table()

    create_wiki_links_table()

    create_indexes()

    create_triggers()

    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()

