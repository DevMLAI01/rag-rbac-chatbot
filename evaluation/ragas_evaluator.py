from __future__ import annotations
import asyncio
import logging
import os
from datetime import datetime, timezone
from statistics import mean

from config.settings import settings
# Ragas uses the openai library internally — ensure the key is in the environment
if settings.openai_api_key:
    os.environ.setdefault("OPENAI_API_KEY", settings.openai_api_key)

logger = logging.getLogger(__name__)


async def evaluate_response(
    request_id: str,
    user_id: str,
    role: str,
    query: str,
    answer: str,
    contexts: list[str],
    ground_truth: str = "",
) -> dict:
    """Run Ragas evaluation asynchronously. Stores results in metrics_store."""
    try:
        from ragas import evaluate
        from ragas.metrics import faithfulness
        from datasets import Dataset

        data = Dataset.from_dict({
            "question":     [query],
            "answer":       [answer],
            "contexts":     [contexts],
            "ground_truth": [ground_truth or answer],
        })

        # Only faithfulness is LLM-only; answer_relevancy + context_precision both
        # need OpenAIEmbeddings.embed_query which has an API change in ragas 0.4.x
        result = await asyncio.to_thread(
            evaluate, data, metrics=[faithfulness]
        )

        def _to_float(v) -> float:
            if isinstance(v, (list, tuple)):
                v = v[0] if v else 0.0
            return float(v) if v is not None else 0.0

        scores = {
            "faithfulness":      _to_float(result["faithfulness"]),
            "answer_relevancy":  0.0,
            "context_precision": 0.0,
        }
        scores["overall_score"] = mean(scores.values())

        from monitoring.metrics_store import insert_ragas
        insert_ragas({
            "request_id":        request_id,
            "user_id":           user_id,
            "role":              role,
            "timestamp":         datetime.now(timezone.utc).isoformat(),
            **scores,
        })

        from config.settings import settings
        if scores["faithfulness"] < settings.ragas_faithfulness_min:
            logger.warning("Low faithfulness | request=%s score=%.2f", request_id, scores["faithfulness"])
        if scores["answer_relevancy"] < settings.ragas_relevancy_min:
            logger.warning("Low answer_relevancy | request=%s score=%.2f", request_id, scores["answer_relevancy"])

        return scores

    except Exception as e:
        logger.error("Ragas evaluation failed | %s", e)
        return {}
