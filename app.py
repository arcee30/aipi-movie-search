import streamlit as st

from movie_search import database, load_model, semantic_search

st.title("Movie plot search")
client = database()
available = {collection.name for collection in client.list_collections()}
indexes = sorted(name for name in available if name.startswith("movie_plots_"))
if not indexes:
    st.info("Run the notebook to index the movie plots first.")
    st.stop()

name = st.selectbox("Movie index", indexes) if len(indexes) > 1 else indexes[0]
with st.form("search"):
    query = st.text_input("Describe a movie plot", placeholder="A train robbery")
    submitted = st.form_submit_button("Search")

if submitted and query.strip():
    model = st.cache_resource(load_model)()
    metadata, excerpt = semantic_search(query.strip(), model, client.get_collection(name))
    st.subheader(f"{metadata['title']} ({metadata['year']})")
    st.write(excerpt)
