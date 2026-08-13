from platform import node

import streamlit as st

from ui.viewer import get_preview_html

from services.notes import (
    get_node,
    update_node,
    get_breadcrumb
)

from services.tags import (
    extract_tags,
    save_note_tags,
    get_note_tags
)

from services.wiki import (
    sync_wiki_links,
    get_backlinks,
    get_outgoing_links
)


def show_editor(node_id):

    node = get_node(node_id)

    if not node:
        st.info("Chọn một note.")
        return

    if "note_mode" not in st.session_state:
        st.session_state.note_mode = "view"


    breadcrumb = get_breadcrumb(node_id)

    st.markdown(
        f"""
        <div class='breadcrumb'>
            {' / '.join(breadcrumb)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==================================================
    # HEADER
    # ==================================================

    st.title(node["title"])

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "👁 View",
            use_container_width=True
        ):
            st.session_state.note_mode = "view"

    with col2:

        if st.button(
            "✏ Edit",
            use_container_width=True
        ):
            st.session_state.note_mode = "edit"

    st.divider()

    # ==================================================
    # VIEW MODE
    # ==================================================

    if st.session_state.note_mode == "view":

        html = get_preview_html(node["content"])

        st.markdown(
            f"""
            <div class="note-panel">
                {html}
            </div>
            """,
            unsafe_allow_html=True
        )

        tags = get_note_tags(node_id)

        if tags:

            st.divider()

            st.subheader("🏷️ Tags")

            st.write(
                " ".join(
                    f"#{tag['name']}"
                    for tag in tags
                )
            )

        links = get_outgoing_links(node_id)

        st.divider()

        st.subheader("➡️ Links")

        if links:

            for item in links:

                st.write(
                    f"→ {item['title']}"
                )

        else:

            st.caption("No links")

        backlinks = get_backlinks(node_id)

        st.divider()

        st.subheader("🔗 References by")

        if backlinks:

            for item in backlinks:

                if st.button(
                    item["title"],
                    key=f"backlink_{item['id']}"
                ):

                    st.session_state.selected_node_id = item["id"]

                    st.rerun()

        else:

            st.caption("No backlinks")

        return

    # ==================================================
    # EDIT MODE
    # ==================================================

    title = st.text_input(
        "Title",
        value=node["title"]
    )

    content = st.text_area(
        "Markdown",
        value=node["content"],
        height=700
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Save",
            use_container_width=True
        ):

            update_node(
                node_id=node_id,
                title=title,
                content=content
            )

            tags = extract_tags(content)

            save_note_tags(
                node_id,
                tags
            )

            sync_wiki_links(
                node_id,
                content
            )

            st.session_state.note_mode = "view"

            st.success("Saved")

            st.rerun()

    with col2:

        if st.button(
            "❌ Cancel",
            use_container_width=True
        ):

            st.session_state.note_mode = "view"

            st.rerun()
