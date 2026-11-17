FROM python:3.12-slim

RUN useradd --create-home --uid 1000 app
ENV HOME=/home/app
WORKDIR /home/app
COPY requirements.txt .
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.6.0 && \
    pip install --no-cache-dir -r requirements.txt

USER app
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
COPY --chown=app:app app.py movie_search.py ./
COPY --chown=app:app chromadb/ ./chromadb/
EXPOSE 7860
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=7860", "--server.headless=true"]
