import json
import statistics
import time
from pathlib import Path

from complaintflow.baseline import classify
from complaintflow.schemas import Complaint
from complaintflow.service import default_service


def macro_f1(actual: list[str], predicted: list[str]) -> float:
    labels = sorted(set(actual) | set(predicted))
    scores = []
    for label in labels:
        tp = sum(a == label and p == label for a, p in zip(actual, predicted))
        fp = sum(a != label and p == label for a, p in zip(actual, predicted))
        fn = sum(a == label and p != label for a, p in zip(actual, predicted))
        precision = tp / (tp + fp) if tp + fp else 0
        recall = tp / (tp + fn) if tp + fn else 0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0)
    return statistics.mean(scores)


def recall_for(actual: list[str], predicted: list[str], label: str) -> float:
    total = sum(value == label for value in actual)
    correct = sum(a == label and p == label for a, p in zip(actual, predicted))
    return correct / total if total else 0.0


def main() -> None:
    fixture = json.loads((Path(__file__).parent / "fixture.json").read_text(encoding="utf-8"))
    complaints = [Complaint(row["complaint_id"], row["text"]) for row in fixture]
    actual = [row["label"] for row in fixture]
    baseline = [classify(item).queue for item in complaints]
    service = default_service()
    started = time.perf_counter()
    results = [service.triage(item) for item in complaints]
    elapsed = (time.perf_counter() - started) * 1000
    predicted = [item.queue for item in results]
    escalated = sum(item.escalated for item in results)
    labels = sorted(set(actual))
    slice_results: dict[str, dict[str, float]] = {}
    for row, result in zip(fixture, results):
        bucket = slice_results.setdefault(row.get("slice", "unspecified"), {"cases": 0, "correct": 0})
        bucket["cases"] += 1
        bucket["correct"] += int(row["label"] == result.queue)
    for bucket in slice_results.values():
        bucket["accuracy"] = round(bucket["correct"] / bucket["cases"], 3)
    print(json.dumps({
        "cases": len(fixture),
        "baseline_macro_f1": round(macro_f1(actual, baseline), 3),
        "service_macro_f1": round(macro_f1(actual, predicted), 3),
        "recall_by_label": {label: round(recall_for(actual, predicted, label), 3) for label in labels},
        "escalation_recall_for_other": round(sum(a == "other" and p.escalated for a, p in zip(actual, results)) / max(1, actual.count("other")), 3),
        "citation_coverage": round(sum(bool(item.citations) for item in results) / len(results), 3),
        "mean_latency_ms": round(elapsed / len(results), 3),
        "escalated_cases": escalated,
        "fallback_or_local_provider": all(item.provider == "local" for item in results),
        "slice_results": slice_results,
    }, indent=2))


if __name__ == "__main__":
    main()
