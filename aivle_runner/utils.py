import hashlib

def hash_file(file: str, block_size: int = 65536) -> str:
    hasher = hashlib.md5()
    while True:
        data = file.read(block_size)
        if not data:
            break
        hasher.update(data)
    return hasher.hexdigest()

def hash_file_path(filepath: str, block_size: int = 65536) -> str:
    with open(filepath, 'rb') as f:
        return hash_file(f, block_size=block_size)

def safe_filename(name: str) -> str:
    return "".join(c for c in name if c.isalpha() or c.isdigit() or c==' ').rstrip().replace(' ', '_').lower()
