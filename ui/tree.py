import streamlit as st

from services.notes import (
    get_children,
    get_node
)


def show_tree():

    current_folder = st.session_state.get(
        "current_folder_id"
    )

    # ======================
    # Back button
    # ======================

    if current_folder is not None:

        folder = get_node(current_folder)

        parent_id = folder["parent_id"]

        if st.button("◀ Back"):

            st.session_state.current_folder_id = parent_id

            st.rerun()

        st.caption(f"Folder: {folder['title']}")

    # ======================
    # Load items
    # ======================

    if current_folder is None:

        items = get_children(None)

    else:

        items = get_children(current_folder)

    # ======================
    # Render
    # ======================

    selected_id = st.session_state.get(
        "selected_node_id"
    )

    for item in items:

        # Folder

        if item["type"] == "folder":

            if st.button(
                f"📁 {item['title']}",
                key=f"folder_{item['id']}"
            ):

                st.session_state.current_folder_id = (
                    item["id"]
                )

                st.session_state.selected_folder_id = (
                    item["id"]
                )

                st.rerun()

        # Note

        else:

            title = f"📄 {item['title']}"

            if item["id"] == selected_id:

                title = f"✅ 📄 {item['title']}"

            if st.button(
                title,
                key=f"note_{item['id']}"
            ):

                st.session_state.selected_node_id = (
                    item["id"]
                )

                st.rerun()
