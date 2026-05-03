import json
import os
from dotenv import load_dotenv
import anthropic
from portfolio_service import view_portfolio
from alerts_service import get_alerts

load_dotenv()

# Defined at module level so the prompt is stable across calls — Anthropic caches it server-side to avoid reprocessing the same instructions on every request
SYSTEM_PROMPT = """You are a financial portfolio assistant for a stock dashboard application.
You will be given a user's portfolio holdings and price alerts as JSON data.
Return your response as a JSON object with exactly two keys:
- "portfolio": a short paragraph summarizing the portfolio holdings, shares, and average buy prices
- "alerts": a short paragraph summarizing alert status, which are active, and which have triggered

Do not include any text outside the JSON object. Keep each section under 100 words."""

def get_ai_summary():
    portfolio = [dict(row) for row in view_portfolio()]
    alerts = [dict(row) for row in get_alerts()]

    data = {
        "portfolio": portfolio,
        "alerts": alerts
    }

    client = anthropic.Anthropic()

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": f"Here is my current portfolio and alerts data:\n\n{json.dumps(data, indent=2)}\n\nPlease provide a summary."
                }
            ]
        )

        for block in response.content:
            if block.type == "text":
                text = block.text.strip()
                # Strip markdown code fences — the model sometimes wraps JSON in ```json blocks despite being instructed not to
                if text.startswith("```"):
                    text = text.split("```")[1]
                    if text.startswith("json"):
                        text = text[4:]
                    text = text.strip()
                return json.loads(text)

        return {"error": "No response received from the API."}

    except anthropic.RateLimitError:
        return {"error": "Rate limit reached. Please try again in a few minutes."}
    except anthropic.APIStatusError as e:
        return {"error": f"API error {e.status_code}: {e.message}"}
    except json.JSONDecodeError:
        return {"error": "Could not parse the AI response. Please try again."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
