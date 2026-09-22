/**
 * Two-Model Cascade Architecture Pattern
 * 
 * Demonstrates a high-performance, cost-effective hybrid pipeline:
 * 1. Fast, typed classification using TypeSafe Jev (System 1) in ~100ms.
 * 2. Confidence-gated routing: automatic deterministic handling for high confidence.
 * 3. Fallback to a generative frontier LLM (System 2) only when deep reasoning or custom drafting is required.
 */

interface SystemOneResponse {
  model: string;
  answers: {
    category: {
      type: "choice";
      choice: "direct_answer" | "escalate_bug" | "billing_inquiry" | "complex_consultation";
      probabilities: Record<string, number>;
      confidence: number;
    };
    urgency: {
      type: "score";
      score: number;
      legend: Record<string, string>;
      probabilities: Record<string, number>;
      confidence: number;
    };
    needs_human: {
      type: "noul";
      noul: number;
    };
  };
  usage: {
    input_tokens: number;
    output_tokens: number;
  };
}

export async function processCustomerInquiry(customerMessage: string, customerId: string) {
  const apiKey = process.env.TYPESAFE_API_KEY;
  if (!apiKey) {
    throw new Error("Missing TYPESAFE_API_KEY environment variable");
  }

  // Step 1: Execute fast System 1 assessment via Jev in parallel
  const systemOneRes = await fetch("https://api.typesafe.ai/v1/systemone", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "jev-latest",
      state: {
        customer_id: customerId,
        message: customerMessage
      },
      questions: {
        category: {
          type: "choice",
          instructions: "Classify the primary intent of this customer message.",
          criteria: {
            direct_answer: "Standard FAQs, password reset instructions, or documentation links",
            escalate_bug: "Definite software defects, 500 errors, or data synchronization glitches",
            billing_inquiry: "Questions about invoices, subscription charges, or card updates",
            complex_consultation: "Custom enterprise architecture, legal agreements, or ambiguous issues"
          }
        },
        urgency: {
          type: "score",
          instructions: "Rate the operational impact and frustration level.",
          criteria: [
            "Low - General inquiry with no business disruption",
            "Medium - Workflow partially impeded",
            "High - Revenue loss or critical blocking issue"
          ]
        },
        needs_human: {
          type: "noul",
          instructions: "Does this require direct human agent empathy or intervention?"
        }
      }
    })
  });

  if (!systemOneRes.ok) {
    // Graceful degradation: If System 1 API is unavailable, route to standard queue
    console.error(`Jev evaluation failed: HTTP ${systemOneRes.status}`);
    return routeToHumanQueue(customerMessage, "system_fallback");
  }

  const evaluation: SystemOneResponse = await systemOneRes.json();
  const { category, urgency, needs_human } = evaluation.answers;

  console.log(`[System 1 Triage] Category: ${category.choice} (Conf: ${category.confidence}) | Urgency: ${urgency.score.toFixed(2)} | Human Prob: ${needs_human.noul.toFixed(2)}`);

  // Step 2: Apply Confidence-Gated Decision Routing
  
  // Rule A: High confidence direct answer -> deterministic resolution
  if (category.confidence >= 0.85 && category.choice === "direct_answer" && needs_human.noul < 0.20) {
    return handleDeterministicFAQ(customerMessage);
  }

  // Rule B: High urgency or explicit human need -> immediate human escalation
  if (urgency.score >= 1.8 || needs_human.noul >= 0.80) {
    return routeToHumanQueue(customerMessage, `priority_escalation_${category.choice}`);
  }

  // Rule C: Complex or low confidence -> call frontier System 2 LLM with targeted instructions
  return invokeFrontierLLM(customerMessage, category.choice, urgency.score);
}

async function handleDeterministicFAQ(message: string) {
  // Fast path: resolves instantly without burning LLM generation tokens
  return {
    handled_by: "deterministic_engine",
    status: "resolved",
    message: "Here are the relevant self-service documentation links..."
  };
}

async function routeToHumanQueue(message: string, reason: string) {
  return {
    handled_by: "human_queue",
    status: "queued",
    reason
  };
}

async function invokeFrontierLLM(message: string, suggestedCategory: string, urgency: number) {
  // Expensive path: called only for the ~15% of ambiguous or generative cases
  return {
    handled_by: "system_two_frontier_llm",
    status: "generated_reply",
    category: suggestedCategory
  };
}
