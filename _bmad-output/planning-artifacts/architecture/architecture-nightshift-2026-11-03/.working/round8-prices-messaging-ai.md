# Round 8 prices: messaging, voice, Bedrock, GPU power (checked 2026-11-11; research agent, primary sources; USD)

## SMS per message (Twilio per segment)

| Country | AWS End User Messaging | Twilio |
|---|---|---|
| Germany | 0.10719 | 0.112 |
| France | 0.07401 | 0.0798 |
| UK | 0.05 | 0.056 |
| US | 0.00774 + carrier fee about 0.0042, ≈ 0.012 | 0.0083 + carrier fee 0.0035–0.005 |

- **AWS source:** the CSV linked from aws.amazon.com/end-user-messaging/pricing. Carrier fees are listed only for the US; for DE, FR and UK they are unverified.
- **Twilio source:** twilio.com/en-us/sms/pricing/{de,fr,gb,us} ("current as of October 2026"; additional carrier fees may apply; $0.001 per failed message).

## Twilio voice to mobile, per minute
- **Germany:** 0.3763 standard, 0.0420 when the call comes from the EEA (depends on origin).
- **UK:** 0.0305 (some subcategories higher).
- **US:** 0.0140.

## Bedrock, eu-central-1, per 1M tokens
Source: AWS Price List API, offer AmazonBedrockFoundationModels, published 2026-11-09.

| Model | Input, regional | Input, global | Output, regional | Output, global |
|---|---|---|---|---|
| Haiku 4.5 | 1.10 | 1.00 | 5.50 | 5.00 |
| Sonnet 4.6 | 3.30 | 3.00 | 16.50 | 15.00 |

**Confirms round 4:** regional prices are exactly 10% above global, also for cache, batch and reserved prices.

## Bedrock custom (fine-tuned) models
- **On-demand custom model deployment:** US East and US West only, Nova and Llama 3.3 70B only, no Claude, no EU.
- **Otherwise Provisioned Throughput:** billed per Model Unit per hour, no commitment, 1 month or 6 months. The price per Model Unit is unverified ("contact your AWS account manager").
- The prov-throughput page still says customized models need Provisioned Throughput, which conflicts with the newer on-demand page.

## NVIDIA L4
- Max power 72 W (nvidia.com/en-us/data-center/l4).
