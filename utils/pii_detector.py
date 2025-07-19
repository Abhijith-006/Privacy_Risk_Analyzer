import re

# Regex


PII_PATTERNS={
    "Email":r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "Phone Number":r"\+?\d[\d\s.-]{8,}",
    "Card/Bank Number":r"\b\d{12,16}\b",
    "Postal Code":r"\b\d{6}\b",
    "Address":r"\d{1,5}\s\w+\s\w+"
}

def regex_pii_check(text):
    findings=[]
    for label,pattern in PII_PATTERNS.items():
        if re.search(pattern,text):
            findings.append(label)
    return findings

def redact_text(text,highlight=False):
    """
    If highlight=True,wraps PII with <span> and colors.
    If highlight=False,replaces with [REDACTED].
    """
    highlighted_text=text
    for label,pattern in PII_PATTERNS.items():
        if highlight:
            highlighted_text=re.sub(pattern,lambda m:f"<span style='background-color:yellow;color:red;'>[{label}] {m.group()}</span>",highlighted_text)
        else:
            highlighted_text=re.sub(pattern, "[REDACTED]",highlighted_text)
    return highlighted_text
