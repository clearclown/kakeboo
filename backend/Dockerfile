# backend/Dockerfile

# ベースイメージとしてpython:3.11-slimを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt update && apt -y upgrade && apt -y install \
    sudo \
    curl \
    git \
    vim \
    nano \
    build-essential \
    libpq-dev

# ソースコードをコピー
COPY . .

RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt --no-cache-dir

# pipとpoetryをインストール
# RUN pip install --upgrade pip && \
    # pip install --no-cache-dir poetry psycopg2-binary
# poetryの設定を変更
# RUN poetry config virtualenvs.create false
# poetry lockを実行
# RUN cd /app/backend && poetry lock --no-update
# poetry installを実行
# RUN cd /app/backend && poetry install

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
