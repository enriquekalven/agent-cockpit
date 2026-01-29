import asyncio
import json
import uuid
import os
from typing import Any, Callable
from datetime import datetime

class ShadowRouter:
    """
    Shadow Mode Router: Orchestrates Production (v1) and Shadow (v2) agent calls.
    Logs comparisons for production confidence.
    """
    def __init__(self, v1_func: Callable, v2_func: Callable):
        self.v1 = v1_func
        self.v2 = v2_func

    async def route(self, query: str, **kwargs):
        trace_id = str(uuid.uuid4())
        
        # 1. Primary Call (Production v1) - Sequential/Blocking
        start_v1 = datetime.now()
        v1_resp = await self.v1(query, **kwargs)
        v1_latency = (datetime.now() - start_v1).total_seconds()

        # 2. Shadow Call (Experimental v2) - Asynchronous/Non-blocking
        # We fire and forget this, or use a background task
        asyncio.create_task(self._run_shadow(trace_id, query, v1_resp, v1_latency, **kwargs))

        return {
            "response": v1_resp,
            "trace_id": trace_id,
            "latency": v1_latency
        }

    async def _run_shadow(self, trace_id: str, query: str, v1_resp: Any, v1_latency: float, **kwargs):
        """
        Runs the v2 agent in the 'shadow' without user impact.
        Logs the comparison to BigQuery/Cloud Logging.
        """
        try:
            start_v2 = datetime.now()
            v2_resp = await self.v2(query, **kwargs)
            v2_latency = (datetime.now() - start_v2).total_seconds()

            comparison = {
                "traceId": trace_id,
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "production": {
                    "response": v1_resp,
                    "latency": v1_latency,
                    "model": "gemini-1.5-flash"
                },
                "shadow": {
                    "response": v2_resp,
                    "latency": v2_latency,
                    "model": "gemini-1.5-pro-experimental"
                }
            }
            
            # In production, this goes to GCP BigQuery or Cloud Logging
            # For now, we simulate a 'Comparison Event'
            print(f"🕵️ [SHADOW MODE] Comparison Logged: {trace_id}")
            # Mock: save to a local json for the 'Flight Recorder' UI to consume
            self._mock_save_trace(comparison)
            
        except Exception as e:
            print(f"❌ [SHADOW ERROR] {str(e)}")

    def _mock_save_trace(self, data):
        # Local file store for demonstration replay UI
        os.makedirs("traces", exist_ok=True)
        with open(f"traces/{data['traceId']}.json", "w") as f:
            json.dump(data, f)
