from huggingface_hub import hf_hub_download
import joblib
from transformers import AutoModelForCausalLM, AutoModel
import tempfile
import os

def d():
    REPO_ID = "nari-labs/Dia-1.6B"
    FILENAME = "sklearn_model.joblib"
    x = hf_hub_download(repo_id=REPO_ID, filename='dia-v0_1.pth', local_dir="/tmp")

print("Download a model from Hugging Face Hub")
#model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
model = AutoModel.from_pretrained("biomistral/biomistral-7b")
print("Save the model to a local directory")
with tempfile.TemporaryDirectory() as tmp_dir:
    model.save_pretrained(tmp_dir, max_shard_size="5GB")
    print(sorted(os.listdir(tmp_dir)))
print("done")
print("done")