# ⚡ Technical Guide: Agent Load Testing (`make load-test`)

The **Load Tester** is a high-concurrency stress tool designed to measure the performance and stability of your agentic endpoints under pressure.

## 🚀 Commands

### Local Installation
```bash
make load-test       # Runs with default parameters
# Custom configuration:
agent-ops load-test --url http://api.agent.com/query --requests 100 --concurrency 10
```

### Portable (Zero-Install)
```bash
uvx agentops-cockpit load-test --url "http://localhost:8000/agent" --requests 20
```

---

## ⚙️ Parameters

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `--url` | `http://localhost:8000/...` | The target endpoint to stress test. |
| `--requests` | `50` | The total number of GET requests to fire. |
| `--concurrency` | `5` | The number of simultaneous connections (Simulated Users). |

---

## 📊 Performance Metrics

After the test, the Cockpit generates a performance table including:

1.  **Success Rate**: The percentage of `200 OK` responses.
2.  **Avg/Min/Max Latency**: The distribution of response times.
3.  **p90 Latency**: The "90th percentile" response time—the most accurate metric for real-world user experience (ignores outliers).
4.  **Error Count**: Total number of non-200 responses captured.

### Use Case
Run this before a production release to ensure your **Cloud Run** or **GKE** scaling parameters are sufficient to handle spikes in agent reasoning requests.
