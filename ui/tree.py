import streamlit as st

from services.notes import build_tree


def render_tree(nodes):

    selected_id = st.session_state.get(
        "selected_node_id"
    )

    for node in nodes:

        title = node["title"]

        # Folder
        if node["type"] == "folder":

            if node["id"] == selected_id:
                title = f"🔹 📁 {title}"
            else:
                title = f"📁 {title}"

            if st.button(
                title,
                key=f"folder_{node['id']}",
                use_container_width=True
            ):

                st.session_state.selected_node_id = node["id"]
                st.session_state.selected_folder_id = node["id"]

                st.rerun()

            if node["children"]:
                render_tree(node["children"])

        # Note
        else:

            if node["id"] == selected_id:
                title = f"🔹 📄 {title}"
            else:
                title = f"📄 {title}"

            if st.button(
                title,
                key=f"note_{node['id']}",
                use_container_width=True
            ):

                st.session_state.selected_node_id = node["id"]

                st.rerun()


def show_tree():

    tree = build_tree()

    render_tree(tree)