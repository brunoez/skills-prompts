# TypeSafe AI Jev API Reference

Official API specification for interacting with TypeSafe AI's System One evaluation endpoint.

## 1. HTTP Endpoint

```http
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <TYPESAFE_API_KEY>
Content-Type: application/json
```

## 2. Request Payload Schema

```typescript
interface SystemOneRequest {
  // Flagship model name: "jev-latest" or "jev-1.13.0"
  model: string;
  
  // Context to evaluate: string, JSON object, or string array
  state: string | Record<string, any> | string[];
  
  // Map of question ID to Question definition
  questions: Record<string, Question>;
}

type Question = ChoiceQuestion | ScoreQuestion | NoulQuestion;

interface ChoiceQuestion {
  type: "choice";
  instructions: string | Record<string, any> | any[];
  criteria: Record<string, string | Record<string, any> | null>; // max 255 options
}

interface ScoreQuestion {
  type: "score";
  instructions: string | Record<string, any> | any[];
  criteria: (string | Record<string, any>)[]; // 2 to 10 ordered levels
}

interface NoulQuestion {
  type: "noul";
  instructions: string | Record<string, any> | any[];
  criteria?: {
    true?: string | Record<string, any>;
    false?: string | Record<string, any>;
  };
}
```

## 3. Response Payload Schema

```typescript
interface SystemOneResponse {
  model: string; // e.g. "jev-1.13.0"
  answers: Record<string, Answer>;
  usage: {
    input_tokens: number;
    output_tokens: number;
  };
}

type Answer = ChoiceAnswer | ScoreAnswer | NoulAnswer;

interface ChoiceAnswer {
  type: "choice";
  choice: string;                      // Selected key from criteria
  probabilities: Record<string, number>; // Probabilities summing to 1.0
  confidence: number;                  // Derived certainty metric [0.0 - 1.0]
}

interface ScoreAnswer {
  type: "score";
  score: number;                       // Continuous probability-weighted position
  legend: Record<string, string>;      // Index mapped to level label
  probabilities: Record<string, number>; // Distribution across levels
  confidence: number;                  // Derived certainty metric [0.0 - 1.0]
}

interface NoulAnswer {
  type: "noul";
  noul: number;                        // Calibrated probability of truth [0.0 - 1.0]
}
```

## 4. HTTP Status Codes & Error Handling

| Status | Code | Meaning | Recovery Strategy |
|---|---|---|---|
| `200` | `OK` | Request succeeded; answers returned in JSON | Parse answers by question ID |
| `400` | `bad_request` | Malformed JSON or invalid schema in state/questions | Verify JSON syntax and schema requirements |
| `401` | `unauthorized` | Missing, invalid, or expired Bearer token | Check `TYPESAFE_API_KEY` |
| `404` | `not_found` | Model alias does not exist | Use `"jev-latest"` or `"jev-1.13.0"` |
| `422` | `unprocessable_entity` | Question constraints violated (e.g. >255 options, <2 score levels) | Adjust question parameters |
| `429` | `rate_limit_exceeded` | Requests per second or token quota exceeded | Implement exponential backoff retry |
| `500` | `internal_server_error` | Internal service disruption | Retry with fallback policy |
| `529` | `overloaded` | Cluster load threshold exceeded | Back off with jitter; throttle concurrency to <= 16 requests |

## 5. Pricing & Latency Profile

* **Input Tokens:** `$0.042 / MTok` ($42 per 1 Billion tokens).
* **Output Tokens:** `$0.00 / MTok` (Gratis, too cheap to meter).
* **Server Execution Latency:** `75ms to 90ms` p50 (observable via response header `x-envoy-upstream-service-time`).
* **End-to-End Latency & Connection Pooling:**
  * **Warm Keep-Alive Connection:** `~290ms` round-trip (measured across global backbones to AWS `us-west-2`).
  * **Cold Connection:** `~1.2s` (due to TCP 3-way handshake + TLS 1.3 cryptographic setup).
  * **Mandatory Best Practice:** Always reuse persistent HTTP sessions (`httpx.Client()`, `http.Agent({ keepAlive: true })`) to avoid cold connection penalties.

## 6. Concurrency Engineering & Throttling

Empirical stress testing reveals that flooding the endpoint with 100+ simultaneous requests pushes round-trip latency above 2 seconds and triggers `529 Overloaded` response cascades.
* **Optimal Batch Concurrency:** Set a semaphore or concurrency worker limit of **16 parallel requests**.
* At 16 parallel requests, server processing remains locked at ~75-90ms while maximizing aggregate pipeline throughput.

