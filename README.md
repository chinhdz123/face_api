### I. Environment Installation
Require Anaconda installed:
1. (optional) Create new environment, highly recommmend python 3.8 for stability:

```
conda create --name demo_ai python=3.8 -y && conda activate demo_ai

```
2. install pytorch

```
gpu: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
cpu: pip install torch torchvision torchaudio
```
3. install requirements:

```
pip install -r requirements.txt
```

## II. RUN
1. run api
```
python app.py
```