import gdown

file_id = "1XBzwyjXHMlTLVrcSaCMdLwuUoQrqFdPs"
url = f"https://drive.google.com/uc?id={file_id}"

# Download the file to the current directory
gdown.download(url, quiet=False)