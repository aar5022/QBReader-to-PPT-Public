import re


def split_tossup(tossup: str) -> list[str]:
    titles = ["Dr", "Mr", "Mrs", "Prof", "Ms", "Sir", "Jr", "Sr", "Esq", "St", "Mt", "v"]
    title_pattern = r"\b(" + "|".join(titles) + r")\.(?=\s|$)"
    tossup_with_placeholders = re.sub(
        title_pattern,
        lambda match: match.group(0).replace(".", "<TITLE_PERIOD>"),
        tossup,
    )
    end_pattern = r"(?<!\b[A-Z])[\.\?\!](?![A-Za-z]\b)"
    tossup_with_placeholders = (
        tossup_with_placeholders
        .replace("<b>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )
    parts = tossup_with_placeholders.split("(*)")
    if len(parts) > 1:
        parts[0] = parts[0] + "(*)"

    processed_parts = []
    for part in parts:
        sentences = re.split(end_pattern, part)
        sentences = [sentence.replace("<TITLE_PERIOD>", ".") for sentence in sentences]
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        processed_parts.extend(sentences)

    return [part for part in processed_parts if part not in ("", "'", '"')]


def after_substring(text: str, sub: str) -> str:
    index = text.find(sub)
    if index != -1:
        return text[index + 1:]
    return text


def ensure_sentence_end(text: str) -> str:
    if text.endswith((".", "?", "!", ":", ";", "(*)")):
        return text
    return text + "."

def strip_answer_guidance(answer: str) -> str:
    visible_answer = re.sub(r"\[[^\]]*\]", "", answer) # removed bracketed section
    visible_answer = re.sub(r"\s+", " ", visible_answer).strip(" ;,.") #remove leading and trailing punctuation
    return visible_answer or answer.strip()