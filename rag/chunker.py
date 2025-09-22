def chunk_by_heading(text, delimiter="###"):
    chunks = text.split(delimiter)
    return [f"{delimiter}{chunk.strip()}" for chunk in chunks if chunk.strip()]