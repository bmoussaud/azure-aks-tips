import os
import time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import logging
from bitnet import load_model, save_model, use_model, download_snapshot

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("app")

app = FastAPI()

@app.post("/write-content/{target}")
async def write_content(target: str):
    try:
        dir_path = f"/mnt/{target}"
        os.makedirs(dir_path, exist_ok=True)
        # Test if the directory exists
        if not os.path.exists(dir_path):
            raise HTTPException(status_code=500, detail=f"Directory does not exist : {dir_path}")
        file_path = os.path.join(dir_path, "output.txt")
        now = datetime.now(timezone.utc).isoformat()
        logger.info(f"Timestamp {now} write to {file_path}")
        with open(file_path, "a") as f:
            f.write(now + "\n")
        logger.info(f"Timestamp {now} written to {file_path}")
        return JSONResponse({"message": f"Timestamp written {now} to {file_path}"})
    except Exception as e:
        logger.error(f"Error writing timestamp: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/write-content/{target}/file/{model}/size/{size}")
async def write_model_file(target: str, model: str, size: int):
    """
    Create a file named {model} of {size} MB in /mnt/{target}
    """
    start_time = time.time()
    try:
        dir_path = f"/mnt/{target}"
        os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(dir_path):
            raise HTTPException(status_code=500, detail=f"Directory does not exist : {dir_path}")
        file_path = os.path.join(dir_path, model)
        bytes_to_write = size * 1024 * 1024
        logger.info(f"Writing file {file_path} of size {size} MB ({bytes_to_write} bytes)")
        with open(file_path, "wb") as f:
            chunk_size = 1024 * 1024  # 1MB
            written = 0
            while written < bytes_to_write:
                write_now = min(chunk_size, bytes_to_write - written)
                random_chunk = os.urandom(write_now)
                f.write(random_chunk)
                written += write_now
        elapsed = time.time() - start_time
        logger.info(f"File {file_path} written successfully in {elapsed:.2f} seconds")
        return JSONResponse({
            "message": f"File '{model}' of size {size} MB written to {file_path}",
            "elapsed_time_seconds": round(elapsed, 3)
        })
    except Exception as e:
        logger.error(f"Error writing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/write-content/{target}/file/{model}")
async def load_model_file(target: str, model: str):
    """
    Load the file named {model} of {size} MB from /mnt/{target} into memory and return its size in bytes and elapsed time.
    """
    import time
    start_time = time.time()
    try:
        dir_path = f"/mnt/{target}"
        file_path = os.path.join(dir_path, model)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File does not exist: {file_path}")
        with open(file_path, "rb") as f:
            content = f.read()
        elapsed = time.time() - start_time
        return JSONResponse({
            "message": f"File '{model}' loaded from {file_path}",
            "file_size_bytes": len(content),
            "elapsed_time_seconds": round(elapsed, 3)
        })
    except Exception as e:
        logger.error(f"Error loading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
def get_cache_dir(target: str):
    """
    Create a cache directory in /mnt/{target}
    """
    dir_path = f"/mnt/{target}/cache"
    os.makedirs(dir_path, exist_ok=True)
    if not os.path.exists(dir_path):
        raise HTTPException(status_code=500, detail=f"Directory does not exist : {dir_path}")
    return dir_path

def get_save_model_dir(target: str, model_id: str):
    """
    Create a save directory in /mnt/{target}
    """
    dir_path = f"/mnt/{target}/models/{model_id}"
    os.makedirs(dir_path, exist_ok=True)
    if not os.path.exists(dir_path):
        raise HTTPException(status_code=500, detail=f"Directory does not exist : {dir_path}")
    return dir_path

@app.get("/download/model/{model}/target/{target}")
async def download_hf_model(model: str, target: str):
 
    import time
    start_time = time.time()
    try:
        model_id= model.replace("_", "/")
        save_model_dir = get_save_model_dir(target, model_id)

        download_snapshot(model_id, save_model_dir)
        logger.info(f"Model {model_id} loaded successfully")
        elapsed = time.time() - start_time
       
        return JSONResponse({
            "message": f"Model '{model_id}' loaded",
            "save_model_dir": save_model_dir,
            "elapsed_time_seconds": round(elapsed, 3)
        })
    except Exception as e:
        logger.error(f"Error downloading model: {e}",   stack_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/load/model/{model}/target/{target}")
async def load_hf_model(model: str, target: str):
 
    import time
    start_time = time.time()
    try:
        cache_dir = get_cache_dir(target)
        model_id= model.replace("_", "/")
        tokenizer, model = load_model(model_id,cache_dir) 
        logger.info(f"Model {model_id} loaded successfully")
        elapsed = time.time() - start_time
       
        return JSONResponse({
            "message": f"Model '{model_id}' loaded",
            "cache_dir": cache_dir,
            "elapsed_time_seconds": round(elapsed, 3)
        })
    except Exception as e:
        logger.error(f"Error loading model: {e}",   stack_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/save/model/{model}/target/{target}")
async def save_hf_model(model: str, target: str):
    import time
    start_time = time.time()
    try:
        cache_dir = get_cache_dir(target)
        model_id= model.replace("_", "/")
        save_model_dir = get_save_model_dir(target, model_id)
        tokenizer, model = load_model(model_id, cache_dir)
        logger.info(f"Model {model_id} loaded successfully")
        save_model(model, save_model_dir)
        logger.info(f"Model {model_id} saved successfully")
        elapsed = time.time() - start_time
        
        return JSONResponse({
            "message": f"Model '{model_id}' loaded",
            "cache_dir": cache_dir,
            "save_model_dir": save_model_dir,
            "elapsed_time_seconds": round(elapsed, 3)
        })
    except Exception as e:
        logger.error(f"Error save model: {e}", stack_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/use/model/{model}/target/{target}")
async def use_hf_model(model: str, target: str):
    import time
    start_time = time.time()
    try:
        cache_dir = get_cache_dir(target)
        model_id= model.replace("_", "/")
        save_model_dir = get_save_model_dir(target, model_id)

        tokenizer, model = load_model(save_model_dir, cache_dir)
        elapsed_load = time.time() - start_time
        logger.info(f"Model {model_id} loaded successfully")

        start_time = time.time()
        response = use_model(model, tokenizer)
        logger.info(f"Model {model_id} used successfully")
        elapsed_use= time.time() - start_time

        return JSONResponse({
            "model": f"'{model_id}' loaded",
            "save_model_dir": save_model_dir,
            "cache_dir": cache_dir,
            "response": response,
            "elapsed_time_seconds_load": round(elapsed_load, 3),
            "elapsed_time_seconds_use": round(elapsed_use, 3)
        })
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
