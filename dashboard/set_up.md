## Pantau Pasar - Dashboard

### Setup Environment - Anaconda

Create virtual environment
conda create --name dashboard python=3.14
conda activate dashboard
conda install -r requirements.txt

### Setup Environment - Shell/Terminal

mkdir dashboard
cd dashboard
conda create --name dashboard python=3.14
conda activate dashboard
conda install -r requirements.txt

### Run Dashboard
streamlit run dashboard/dashboard.py