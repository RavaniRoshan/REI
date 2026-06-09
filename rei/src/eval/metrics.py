from typing import List, Dict


def top5_accuracy(predictions: List[str], actual: List[str]) -> float:
    pred_top5 = predictions[:5]
    return 1.0 if any(p in actual for p in pred_top5) else 0.0


def precision_at_k(predictions: List[str], actual: List[str], k: int = 5) -> float:
    hits = len(set(predictions[:k]) & set(actual))
    return hits / k if k > 0 else 0.0


def recall_at_k(predictions: List[str], actual: List[str], k: int = 5) -> float:
    if not actual:
        return 0.0
    hits = len(set(predictions[:k]) & set(actual))
    return hits / len(actual)


def compute_all_metrics(results: List[Dict]) -> Dict:
    if not results:
        return {"top5_acc": 0.0, "precision5": 0.0, "recall5": 0.0, "sample_count": 0}
    accs = [top5_accuracy(r["predictions"], r["actual"]) for r in results]
    precisions = [precision_at_k(r["predictions"], r["actual"], 5) for r in results]
    recalls = [recall_at_k(r["predictions"], r["actual"], 5) for r in results]
    return {
        "top5_acc": sum(accs) / len(accs),
        "precision5": sum(precisions) / len(precisions),
        "recall5": sum(recalls) / len(recalls),
        "sample_count": len(results),
    }
