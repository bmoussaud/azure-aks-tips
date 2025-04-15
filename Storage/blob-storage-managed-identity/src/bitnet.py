import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import tempfile
from huggingface_hub import snapshot_download
import os

from transformers import AutoTokenizer, AutoModelForCausalLM

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def download_snapshot(model_id, local_dir):
    logger = logging.getLogger("bitnet.download_snapshot")
    logger.info('Snapshot_download model snapshot...')
    logger.info(f"Model ID: {model_id}")
    logger.info(f"Local directory: {local_dir}")
    path = snapshot_download(repo_id=model_id, local_dir=local_dir, local_files_only=False, force_download=True)
    logger.info(f"Model snapshot downloaded successfully {path}.")
    return path

def load_model(model_id, cache_dir):
    logger = logging.getLogger("bitnet.load_model")
    logger.info('Loading tokenizer and model...')
    logger.info(f"Model ID: {model_id}")
    logger.info("AutoTokenizer.from_pretrained")
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=False, cache_dir=cache_dir)
    logger.info("AutoModelForCausalLM.from_pretrained")
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=False, cache_dir=cache_dir)
    return tokenizer, model


def save_model(model, save_model_dir):
    logger = logging.getLogger("bitnet.save_model")
    logger.info(f"Saving model to {save_model_dir} directory...")
    model.save_pretrained(save_model_dir, max_shard_size="1GB")
    logger.info(sorted(os.listdir(save_model_dir)))
    logger.info("Model saved successfully.")

def use_model(model, tokenizer):
    logger = logging.getLogger("bitnet.save_model")
    # Apply the chat template
    logger.info("Apply the chat template")
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "How are you?"},
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    chat_input = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate response
    chat_outputs = model.generate(**chat_input, max_new_tokens=50)
    response = tokenizer.decode(chat_outputs[0][chat_input['input_ids'].shape[-1]:], skip_special_tokens=True)  # Decode only the response part
    logger.info(f"\nAssistant Response: {response}")
    return response

#model_id = "microsoft/bitnet-b1.58-2B-4T"
#cache_dir = "./cache"
#tokenizer, model = load_model(model_id, cache_dir)
#use_model(model, tokenizer)
