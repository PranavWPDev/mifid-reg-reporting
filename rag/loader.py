def load_mifid_rules():
    """
    Load rules and convert into structured chunks with metadata
    """
    with open("data/mifid_rules.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = []

    for block in text.split("\n---\n"):
        lines = block.strip().split("\n")

        metadata = {}
        content = []

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip().lower()] = value.strip()
            else:
                content.append(line.strip())

        chunk_text = " ".join(content)

        if chunk_text:
            chunks.append({
                "text": chunk_text,
                "metadata": metadata
            })

    return chunks