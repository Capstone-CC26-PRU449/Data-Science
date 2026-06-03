# Pantau Pasar - Dashboard ✨

## Setup Environment - Anaconda
conda create --name pantau_pasar python=3.12
conda activate pantau_pasar
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

## Opsi Instalasi Terpisah
# Untuk Dashboard saja: pip install -r dashboard/requirements.txt
# Untuk Notebook saja:  pip install -r notebook/requirements.txt

## Run streamlit app
streamlit run dashboard/dashboard.py

## Run jupyter notebook
jupyter notebook