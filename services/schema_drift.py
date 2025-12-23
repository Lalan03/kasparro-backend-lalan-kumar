#services/schema_drift.py

from difflib import SequenceMatcher




def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()




def detect_drift(old_fields, new_fields, threshold=0.7):
    warnings = []
    for nf in new_fields:
        matches = [similarity(nf, of) for of in old_fields]
        if not matches or max(matches) < threshold:
            warnings.append({"field": nf, "confidence": max(matches) if matches else 0})
    return warnings