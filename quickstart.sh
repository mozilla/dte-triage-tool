#!/bin/sh

if ! uv sync; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv sync
fi

export NVM_DIR="$HOME"/.nvm
if ! . "${NVM_DIR}/nvm.sh"; then
    if ! bash --help; then
        echo "Please install nvm and restart."
        echo "https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating"
        exit 2
    fi
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
fi
nvm use

cd src/UI || (echo "Error changing directories, please install manually" && exit 2)
npm run build
cd - || (echo "Error changing directories, please launch app manually" && exit 2)
uv run streamlit run main.py
