import requests
import os
import uuid
import json
import time

API_BASE_URL = "https://api.fakeyou.com"
PUBLIC_BUCKET_BASE_URL = "https://storage.googleapis.com/vocodes-public"

def download_audio_file(file_path, public_audio_url):
    response = requests.get(public_audio_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

def check_and_download_file(output_dir, index, public_audio_url):
    audio_filename = f"{index}.wav"
    output_file_path = os.path.join(output_dir, audio_filename)

    if os.path.exists(output_file_path):
        print(f"File for index {index} already exists")
        return
    
    response = requests.head(public_audio_url)
    if response.status_code != 200:
        print(f"File for index {index} not found")
        return

    download_audio_file(output_file_path, public_audio_url)
    print(f"Downloaded file for index {index}")

def poll_tts_status(inference_job_token):
    headers = {
        "Accept": "application/json",
    }
    response = requests.get(f"{API_BASE_URL}/tts/job/{inference_job_token}", headers=headers)
    return response.json()

def generate_tts_audio(model_token, text):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "uuid_idempotency_token": str(uuid.uuid4()),
        "tts_model_token": model_token,
        "inference_text": text,
    }
    response = requests.post(f"{API_BASE_URL}/tts/inference", headers=headers, data=json.dumps(data))
    return response.json()

def send_messages(model_token, messages, rate_limit_interval, output_dir):
    downloaded_files = set(os.listdir(output_dir))

    for index, message in enumerate(messages, start=1):
        audio_filename = f"{index}.wav"
        if audio_filename in downloaded_files:
            print(f"File for index {index} already exists")
            continue
        
        message_parts = message.strip().split("|")
        message_text = message_parts[1]
        
        response = generate_tts_audio(model_token, message_text)
        inference_job_token = response["inference_job_token"]

        while True:
            status = poll_tts_status(inference_job_token)
            job_status = status["state"]["status"]

            if job_status == "complete_success":
                print(f"Message '{message_text}' processed successfully")

                audio_path = status["state"]["maybe_public_bucket_wav_audio_path"]
                public_audio_url = f"{PUBLIC_BUCKET_BASE_URL}{audio_path}"
                check_and_download_file(output_dir, index, public_audio_url)
                downloaded_files.add(audio_filename)
                break
            elif job_status in {"complete_failure", "dead"}:
                print(f"Message '{message_text}' failed to process")
                break
            else:
                time.sleep(rate_limit_interval)
        
        # Exit the loop if there are no more files to download
        if len(downloaded_files) == len(messages):
            break

    return len(downloaded_files)



if __name__ == "__main__":
    
    model_token = "TM:43c7p13p3z5c"  # Replace with the desired model_token
    rate_limit_interval = 15  # Adjust according
    output_dir = "wavs"  # Replace with the desired output directory

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open("text.txt", "r", encoding="utf-8") as f:
        messages = f.readlines()


    last_processed_index = send_messages(model_token, messages, rate_limit_interval, output_dir)

    print(f"Processed {last_processed_index + 1} messages")