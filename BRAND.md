# SignMatch — Brand identity

**Slug:** `signmatch`  
**Tagline:** Make your business name, address, and phone match everywhere customers look.  
**Local port:** `5102`  
**Status:** Live. Payments processed by Gumroad (Monthly or Quarterly).

## Audience persona
Local business owners who noticed wrong hours, phones, or duplicate listings — especially after a move or rebrand.

Primary personas:
- **Owner-operator:** You need a punch list, not an agency deck.
- **SolvFix scan user:** You already saw exposure gaps and want a fix plan.
- **Office manager:** You can log in — you just need the order of operations.

## Voice & tone
- Clear, encouraging, specific — never hype or fear.
- Honest about limits (No ranking, call, or revenue guarantees. We never auto-edit your listings.).
- Short sentences on landing; checklist language in plans.

## Color palette
Defined in `static/brand.css` (`:root` variables). Accent drives CTAs; background stays calm for long reading.

## Fonts (Google Fonts)
Linked via `https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@…` in templates.

## Logo
`static/logo.svg` — simple wordmark-friendly monogram on rounded square. Use on white/light headers; keep clear space ≈ 0.25× logo height.

## Iconography / illustration
Prefer flat geometric icons, soft corners matching `--radius`, no stock-photo people with fake quotes. Plan peeks use list + accent dots.

## Sample copy lines
- Hero CTA: “Build my visibility plan”
- Honesty: “No ranking, call, or revenue guarantees. We never auto-edit your listings.”
- Paywall: “Start my plan” links to the Gumroad checkout URL.

## Do
- Show Monthly and Quarterly prices, plus the renewal sentence, before checkout.
- Save the customer’s email before sending them to Gumroad.
- Keep disclaimers visible near plans.
- Mobile-first quiz (one question per screen).

## Don’t
- Fake testimonials, stats, or press logos.
- Guarantee results (income, rankings, behavior, bookings).
- Fake urgency (“only 2 spots left”).
- Auto-edit third-party listings (SignMatch) or promise AI magic without saying plans are rule-based in this prototype.

## Explicit palette (hex)

| Token | Hex |
|-------|-----|
| Background | `#F4F7F8` |
| Alt background | `#E8EEF1` |
| Card | `#FFFFFF` |
| Ink | `#0F1C24` |
| Muted | `#5A6B75` |
| Accent | `#0E7C86` |
| Accent hover | `#0A5F67` |
| On-accent | `#F2FFFE` |

**Display font:** Space Grotesk  
**Body font:** IBM Plex Sans

## Logo file
`static/logo.svg`
