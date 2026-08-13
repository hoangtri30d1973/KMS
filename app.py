import streamlit as st

from services.notes import (
    create_folder,
    create_note,
    get_node,
    rename_node,
    delete_node,
    search_notes
)

from ui.tree import show_tree
from ui.editor import show_editor


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Knowledge Management System",
    layout="wide"
)

st.markdown("""
<style>

.selected-node {
    color: navy;
    font-weight: 700;
}

.breadcrumb {
    font-size: 0.9rem;
    color: gray;
    margin-bottom: 0.5rem;
    border-bottom: 1px dashed #CCC;
}

.note-panel {
    border: 1px solid #d0d7de;
    border-radius: 8px;
    padding: 20px;
    background-color: whitesmoke;
    margin-bottom: 20px;
    text-align: justify;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================

if "selected_node_id" not in st.session_state:
    st.session_state.selected_node_id = None

if "selected_folder_id" not in st.session_state:
    st.session_state.selected_folder_id = None


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("My Knowledge Management System")

    st.divider()

    # ----------------------------------------------
    # SEARCH
    # ----------------------------------------------

    st.subheader("🔍 Search")

    keyword = st.text_input(
        "Keyword",
        label_visibility="collapsed",
        placeholder="Search..."
    )

    if keyword:

        results = search_notes(keyword)

        for note in results:

            if st.button(
                f"📄 {note['title']}",
                key=f"search_{note['id']}"
            ):
                st.session_state.selected_node_id = note["id"]

    st.divider()

    # ----------------------------------------------
    # CREATE FOLDER
    # ----------------------------------------------

    st.subheader("📁 New Folder")

    folder_name = st.text_input(
        "Folder Name",
        key="folder_name"
    )

    if st.button("Create Folder"):

        if folder_name.strip():

            create_folder(
                title=folder_name.strip(),
                parent_id=st.session_state.selected_folder_id
            )

            st.success("Folder created")
            st.rerun()

    st.divider()

    # ----------------------------------------------
    # CREATE NOTE
    # ----------------------------------------------

    st.subheader("📄 New Note")

    note_title = st.text_input(
        "Note Title",
        key="note_title"
    )

    if st.button("Create Note"):

        if note_title.strip():

            create_note(
                title=note_title.strip(),
                parent_id=st.session_state.selected_folder_id
            )

            st.success("Note created")
            st.rerun()


# ==================================================
# MAIN LAYOUT
# ==================================================

left, right = st.columns([1, 5])

# ==================================================
# TREE VIEW
# ==================================================

with left:

    st.subheader("💫 Main")

    show_tree()

# ==================================================
# EDITOR
# ==================================================

with right:

    node_id = st.session_state.selected_node_id

    if "current_folder_id" not in st.session_state:
        st.session_state.current_folder_id = None

    else:
        
    if not node_id:

        st.info("Select a note from the tree.")

    else:

        node = get_node(node_id)

        if not node:

            st.warning("Node not found.")

        elif node["type"] == "note":

            show_editor(node_id)

        elif node["type"] == "folder":

            st.subheader("📁 Folder")

            st.write(f"ID: {node['id']}")

            new_name = st.text_input(
                "Folder Name",
                value=node["title"]
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("Rename Folder"):

                    rename_node(
                        node["id"],
                        new_name
                    )

                    st.success("Folder renamed")
                    st.rerun()

            with col2:

                confirm = st.checkbox(
                    "Confirm delete",
                    key="delete_folder_confirm"
                )

                if confirm:

                    if st.button(
                        "Delete Folder",
                        type="primary"
                    ):

                        delete_node(node["id"])

                        st.session_state.selected_node_id = None

                        st.success("Folder deleted")

                        st.rerun()
