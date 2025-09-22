def load_text(file_name):
    path = f"docs/health_guidelines.txt"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()