# Seedance 2.5 on Higgsfield: official facts

Source: Higgsfield API docs, read 2026-11-05. Only facts stated on those pages are listed as verified. Re-check before relying on them, since docs change.

Sources:
- https://docs.higgsfield.ai/docs/models/seedance-2-5.md
- https://docs.higgsfield.ai/docs/models/seedance-2-5/text-to-video.md
- https://docs.higgsfield.ai/docs/models/seedance-2-5/reference-to-video.md
- https://docs.higgsfield.ai/docs/concepts/billing-and-retention.md

## Verified (stated in the docs)

Workflows (endpoint IDs): text-to-video, image-to-video, reference-to-video, video-edit, video-extend, all under `bytedance/seedance-2.5/`.

**Text-to-video fields** (unlisted fields are rejected):
| Field | Values | Default |
|---|---|---|
| prompt | non-empty string, no maximum stated | none |
| duration | integer 4 to 30 seconds | 5 |
| resolution | 480p, 720p, 1080p | 720p |
| aspect_ratio | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 | 16:9 |
| bitrate_mode | standard, high | high |
| output_format | mp4, mov | mp4 |
| generate_audio | true or false | true |

- Text-to-video "does not use media inputs". Use image-to-video or reference-to-video for images, video, or audio.
- Reference-to-video: 1 to 30 images, 1 to 10 videos, 1 to 10 audio files, up to 50 items in total. At least one reference array is required. Media must be public URLs; `asset://` references are rejected.
- Billing: successful generations are charged. Requests that end `failed` or `nsfw` are not charged. A queued request that is canceled is refunded. Cost depends on model and parameters.
- Cost check: the docs say to use an estimate endpoint with the same parameters before generating. The documented example is `POST /estimate/<endpoint-id>` returning `{"usd": "..."}`. The docs show it only for a Soul model, so confirm it works for Seedance.
- Output files are kept for seven days, so download them.

## Pricing (from the account's own estimate endpoint, 2026-11-05)

`POST https://api.higgsfield.ai/estimate/bytedance/seedance-2.5/text-to-video` works and returned a pricing description (no charge). Quoted figures, for 16:9 video without video input, before any customer discount:

| Resolution | Roughly per second of output |
|---|---|
| 480p | $0.2056 |
| 720p | $0.4622 |
| 1080p | $1.1372 |

Examples at those rates: 4s at 480p about $0.82; 6s at 480p about $1.23; 6s at 720p about $2.77. Treat these as estimates. Check your balance before and after the first few runs to confirm. Other aspect ratios (such as 9:16) may differ slightly because billing uses output pixel size.

## Not documented (do not treat as known)

- Any prompt-writing guidance: structure, length, style, camera wording.
- How to refer to reference images inside the prompt (no tag syntax such as `@image1` or `image_0` is described).
- Audio behavior and its price effect. (The estimate for audio on vs. off was identical, so audio may not change the price. Unconfirmed.)
- What fails often.

Anything on these topics must come from your own tests, labeled `experimental` until repeated.

## Observed in our own tests (unverified until repeated)

- Run 1 (text-to-video, 6s, 720p, 9:16, no audio): a prompt with positive requirements, one camera setup per shot, and a short ban list met every requirement on the first generation (user-reviewed).
