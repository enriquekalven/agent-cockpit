# Problem Description: High-Fidelity PII & Secret Heuristics

## Objective
Discover a optimal, high-fidelity set of Regex patterns to populate the `PIIScrubber.PATTERNS` dictionary to accurately detect and mask leaked PII and Cloud/LLM API credentials in codebase strings and agent chat traces.

## Supported Labels
- **EMAIL**: Email addresses
- **PHONE**: North American phone numbers
- **CREDIT_CARD**: Visa/Mastercard credit card patterns
- **SSN**: Social Security Numbers
- **IPV4**: IPv4 addresses
- **AWS_KEY**: Amazon Web Services Access Keys (starting with AKIA)
- **STRIPE_KEY**: Stripe Live Secret API keys (starting with sk_live_)
- **GCP_KEY**: Google Cloud Service Account JSON private key indicators
- **OPENAI_KEY**: OpenAI secret API keys (starting with sk-)

## Hard Constraints
- Must output valid Python `re` module Regex patterns.
- Must achieve **1.0 Precision** on benign variable names (must NOT cross-trigger on code variable names like `aws_key_path`, `openai_token_index`, etc.).
