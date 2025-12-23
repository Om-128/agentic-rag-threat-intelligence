import json

'''  -------- NVD --------  '''
def parse_nvd(file_path : str):
    texts = []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data.get("vulnerabilities", []):
        cve = item.get("cve", {})

        # Skip rejected CVEs
        if cve.get("vulnStatus") == "Rejected":
            continue

        for d in cve.get("descriptions", []):
            if d.get("lang") == "en":
                texts.append(d.get("value", "").strip())
                break

    return texts

'''  -------- MITRE --------  '''
def parse_mitre(file_path):
    texts = []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for obj in data.get("objects", []):
        if obj.get("type") == "attack_pattern":
            text = obj.get("description", "").strip()
            if text:
                texts.append(text)

    return texts

'''  -------- CISA --------  '''
def parse_cisa(file_path):
    texts = []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for v in data.get("vulnerabilities", []):
        text = v.get("shortDescription", "").strip()
        if text:
            texts.append(text)

    return texts
