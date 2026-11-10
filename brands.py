"""Brand configs, quiz questions, and deterministic plan generators."""
from __future__ import annotations

from typing import Any


def _label(options, aid):
    for o in options:
        if o["id"] == aid:
            return o["label"]
    return aid or "your selection"


def _labels_multi(options, ids):
    if not ids:
        return "your selections"
    return ", ".join(_label(options, i) for i in ids)


# ---------- ShelfSpeak ----------
SS_Q = [
    {"id": "biz_type", "type": "choice", "prompt": "What kind of local business do you run?",
     "options": [
         {"id": "salon", "label": "Salon / barber / spa", "hint": "Beauty & wellness"},
         {"id": "restaurant", "label": "Restaurant / cafe / food", "hint": "Hospitality"},
         {"id": "clinic", "label": "Clinic / wellness practice", "hint": "Appointments"},
         {"id": "contractor", "label": "Home services / contractor", "hint": "Jobs & quotes"},
         {"id": "retail", "label": "Retail / boutique", "hint": "Products & drops"},
         {"id": "other", "label": "Other local business"},
     ]},
    {"id": "city", "type": "text", "prompt": "What city or neighborhood do you serve?", "placeholder": "e.g. San Francisco Mission"},
    {"id": "platforms", "type": "choice", "multi": True, "prompt": "Where do you want to post?",
     "help": "Select all that apply.",
     "options": [
         {"id": "ig", "label": "Instagram"},
         {"id": "fb", "label": "Facebook"},
         {"id": "tiktok", "label": "TikTok"},
         {"id": "google", "label": "Google Business updates"},
         {"id": "linkedin", "label": "LinkedIn"},
     ]},
    {"id": "capacity", "type": "choice", "prompt": "How many posts can you realistically publish per week?",
     "options": [
         {"id": "1", "label": "1 post / week", "hint": "Sustainable starter"},
         {"id": "2", "label": "2–3 posts / week"},
         {"id": "4", "label": "4–5 posts / week"},
         {"id": "daily", "label": "Almost daily", "hint": "High capacity"},
     ]},
    {"id": "offer", "type": "text", "prompt": "What’s your main offer or service right now?", "placeholder": "e.g. balayage, lunch specials, roof repair"},
    {"id": "voice", "type": "choice", "prompt": "What voice fits your brand?",
     "options": [
         {"id": "friendly", "label": "Friendly & warm"},
         {"id": "pro", "label": "Professional & clear"},
         {"id": "witty", "label": "Witty & playful"},
         {"id": "bold", "label": "Bold & direct"},
     ]},
    {"id": "goal", "type": "choice", "prompt": "What’s the #1 goal for the next 30 days?",
     "options": [
         {"id": "bookings", "label": "More bookings / appointments"},
         {"id": "awareness", "label": "Local awareness"},
         {"id": "trust", "label": "Build trust with reviews & proof"},
         {"id": "consistency", "label": "Just stay consistent"},
     ]},
    {"id": "assets", "type": "choice", "prompt": "What content assets do you already have?",
     "options": [
         {"id": "phone", "label": "Phone photos only"},
         {"id": "phone_video", "label": "Phone photos + short video"},
         {"id": "pro", "label": "Pro photos / brand kit"},
         {"id": "none", "label": "Almost nothing yet"},
     ]},
    {"id": "blocker", "type": "choice", "prompt": "What usually stops you from posting?",
     "options": [
         {"id": "ideas", "label": "I don’t know what to say"},
         {"id": "time", "label": "I run out of time"},
         {"id": "fear", "label": "I overthink / fear judgment"},
         {"id": "inconsistent", "label": "I start strong then stop"},
     ]},
    {"id": "promo", "type": "choice", "prompt": "Any seasonal or promo angle this month?",
     "options": [
         {"id": "none", "label": "No special promo"},
         {"id": "discount", "label": "Discount / bundle"},
         {"id": "new", "label": "New service or product"},
         {"id": "event", "label": "Local event / holiday"},
     ]},
]


def ss_plan(a: dict[str, Any]) -> dict:
    biz = _label(SS_Q[0]["options"], a.get("biz_type"))
    city = a.get("city") or "your area"
    offer = a.get("offer") or "your main offer"
    voice = _label(SS_Q[5]["options"], a.get("voice"))
    goal = _label(SS_Q[6]["options"], a.get("goal"))
    cap = a.get("capacity", "2")
    posts = {"1": 1, "2": 3, "4": 4, "daily": 6}.get(cap, 3)
    plats = _labels_multi(SS_Q[2]["options"], a.get("platforms") or ["ig"])
    themes = {
        "salon": ["Before/after craft", "Team tip of the week", "Booking reminder", "Client ritual"],
        "restaurant": ["Signature dish spotlight", "Behind the pass", "Local pairing", "Hours & specials"],
        "clinic": ["What to expect visit", "Myth vs fact", "Staff intro", "Soft CTA to book"],
        "contractor": ["Job site progress", "Material explainer", "Safety tip", "Quote process"],
        "retail": ["Shelf story", "How to style/use", "Restock alert", "Owner note"],
        "other": ["Offer explainer", "Process peek", "Community nod", "Soft CTA"],
    }.get(a.get("biz_type", "other"), ["Offer explainer", "Process peek", "Community nod", "Soft CTA"])
    week1 = [f"Day {i+1}: {themes[i % len(themes)]} — {voice.lower()} caption about {offer}" for i in range(min(posts, 4))]
    return {
        "title": f"30-day ShelfSpeak calendar for {biz} in {city}",
        "summary": f"Built for ~{posts} posts/week on {plats}, aimed at {goal.lower()}. Voice: {voice}. This is a drafting plan — not a promise of reach, followers, or bookings.",
        "preview_sections": [
            {"title": "Your posting cadence", "bullets": [
                f"Target: about {posts} posts per week (adjust down if a week gets busy).",
                f"Primary platforms: {plats}.",
                f"Lead offer to feature: {offer}.",
                "Batch captions in one 45-minute block; schedule or paste later.",
            ]},
            {"title": "Week 1 angles (unlocked)", "bullets": week1},
            {"title": "Caption formula", "body": f"Hook (1 line) → proof or detail about {offer} → soft CTA tied to {goal.lower()}. Keep it {voice.lower()}."},
        ],
        "locked_sections": [
            {"title": "Weeks 2–4 full calendar", "teaser": "Day-by-day angles, photo prompts, and CTA variants for the rest of the month."},
            {"title": "Photo & reel shot list", "teaser": "A checklist matched to the assets you said you have."},
            {"title": "Weekly reflection prompts", "teaser": "Simple process metrics (posts published, replies) — no vanity guarantees."},
            {"title": "Next-month refresh pack", "teaser": "Seasonal swap-ins once checkout is live."},
        ],
    }


# ---------- SignMatch ----------
SM_Q = [
    {"id": "biz_type", "type": "choice", "prompt": "What type of business needs cleaner listings?",
     "options": [
         {"id": "salon", "label": "Salon / spa"},
         {"id": "restaurant", "label": "Restaurant / cafe"},
         {"id": "clinic", "label": "Clinic / practice"},
         {"id": "contractor", "label": "Contractor / trades"},
         {"id": "retail", "label": "Retail"},
         {"id": "other", "label": "Other"},
     ]},
    {"id": "city", "type": "text", "prompt": "City shown on your main listing?", "placeholder": "e.g. Oakland, CA"},
    {"id": "pain", "type": "choice", "prompt": "What’s the biggest listing pain right now?",
     "options": [
         {"id": "wrong_phone", "label": "Wrong phone number somewhere"},
         {"id": "wrong_hours", "label": "Wrong or missing hours"},
         {"id": "missing", "label": "Missing on a major directory"},
         {"id": "name", "label": "Name spelled differently across sites"},
         {"id": "reviews", "label": "Few or unanswered reviews"},
     ]},
    {"id": "dirs", "type": "choice", "multi": True, "prompt": "Which places matter most to you?",
     "options": [
         {"id": "google", "label": "Google Business Profile"},
         {"id": "yelp", "label": "Yelp"},
         {"id": "apple", "label": "Apple Maps"},
         {"id": "facebook", "label": "Facebook"},
         {"id": "bing", "label": "Bing Places"},
         {"id": "industry", "label": "Industry directories"},
     ]},
    {"id": "hours_week", "type": "choice", "prompt": "How many hours per week can you spend fixing listings?",
     "options": [
         {"id": "1", "label": "Under 1 hour"},
         {"id": "2", "label": "1–2 hours"},
         {"id": "4", "label": "3–4 hours"},
         {"id": "6", "label": "5+ hours"},
     ]},
    {"id": "owner", "type": "choice", "prompt": "Who can log into your listings?",
     "options": [
         {"id": "me", "label": "I have access"},
         {"id": "partner", "label": "A partner / manager does"},
         {"id": "mixed", "label": "Mixed / unsure on some"},
         {"id": "none", "label": "I need to reclaim access"},
     ]},
    {"id": "scan", "type": "choice", "prompt": "Have you run a SolvFix free Business Exposure Scan?",
     "options": [
         {"id": "yes", "label": "Yes — I have a scan report"},
         {"id": "no", "label": "Not yet"},
         {"id": "later", "label": "I’ll run one after this plan"},
     ]},
    {"id": "nap_ready", "type": "choice", "prompt": "Do you have one “source of truth” name, address, and phone?",
     "options": [
         {"id": "yes", "label": "Yes, written down"},
         {"id": "almost", "label": "Mostly — a few variants"},
         {"id": "no", "label": "Not yet"},
     ]},
    {"id": "photos", "type": "choice", "prompt": "Are Google / major listing photos up to date?",
     "options": [
         {"id": "yes", "label": "Yes"},
         {"id": "old", "label": "Outdated"},
         {"id": "none", "label": "Barely any photos"},
     ]},
    {"id": "priority", "type": "choice", "prompt": "If you only fix one thing this month, what should it be?",
     "options": [
         {"id": "nap", "label": "Make NAP match everywhere"},
         {"id": "gbp", "label": "Tighten Google Business Profile"},
         {"id": "reviews", "label": "Review request habit"},
         {"id": "dupes", "label": "Find duplicate listings"},
     ]},
]


def sm_plan(a: dict[str, Any]) -> dict:
    city = a.get("city") or "your city"
    pain = _label(SM_Q[2]["options"], a.get("pain"))
    dirs = _labels_multi(SM_Q[3]["options"], a.get("dirs") or ["google"])
    hours = _label(SM_Q[4]["options"], a.get("hours_week"))
    priority = _label(SM_Q[9]["options"], a.get("priority"))
    scan_note = {
        "yes": "Use your SolvFix scan as the starting punch list.",
        "no": "Run the free SolvFix scan at solvfix.onrender.com/audit, then return to this roadmap.",
        "later": "Run the free SolvFix scan after you lock your source-of-truth NAP.",
    }.get(a.get("scan", "no"), "")
    week_hours = {"1": 1, "2": 2, "4": 3, "6": 5}.get(a.get("hours_week", "2"), 2)
    return {
        "title": f"SignMatch visibility roadmap — {city}",
        "summary": f"Priority focus: {priority}. Biggest reported pain: {pain}. Planned effort: {hours}. This plan is educational checklists only — it does not edit listings for you, and it does not promise rankings, calls, or revenue.",
        "preview_sections": [
            {"title": "Source-of-truth NAP", "bullets": [
                "Write one exact business name, street address, and phone (last 10 digits consistent).",
                "Use that string everywhere you can edit — no creative abbreviations.",
                "Store it in a note you can copy-paste.",
                scan_note,
            ]},
            {"title": "Week 1 fix order", "bullets": [
                f"Day 1–2: Confirm access on {dirs}.",
                "Day 3: Align phone and address on your primary Google listing if you control it.",
                "Day 4: Fix the single directory that shows the wrongest detail.",
                f"Day 5: Spend remaining time (budget ~{week_hours}h/week) on hours and categories.",
            ]},
            {"title": "What SignMatch will not do", "body": "We do not auto-edit Google, Yelp, Facebook, or other listings. You (or your manager) make changes inside each platform’s tools."},
        ],
        "locked_sections": [
            {"title": "Days 8–30 checklist", "teaser": "Directory-by-directory steps, duplicate hunt, and photo refresh queue."},
            {"title": "Review-request scripts", "teaser": "Polite templates — no fake reviews, no review gating."},
            {"title": "Monthly re-check ritual", "teaser": "A 30-minute cadence to catch drift after holidays or moves."},
            {"title": "SolvFix re-scan prompts", "teaser": "When to re-run the free exposure scan and what to compare."},
        ],
    }


# ---------- CueTrail ----------
CT_Q = [
    {"id": "dog_name", "type": "text", "prompt": "What’s your dog’s name?", "placeholder": "e.g. Mango"},
    {"id": "age", "type": "choice", "prompt": "How old is your dog?",
     "options": [
         {"id": "puppy", "label": "Puppy (under 6 months)"},
         {"id": "young", "label": "6–18 months"},
         {"id": "adult", "label": "Adult (1.5–7 years)"},
         {"id": "senior", "label": "Senior (7+)"},
     ]},
    {"id": "size", "type": "choice", "prompt": "Rough size?",
     "options": [
         {"id": "small", "label": "Small (under 25 lb)"},
         {"id": "medium", "label": "Medium"},
         {"id": "large", "label": "Large / giant"},
     ]},
    {"id": "home", "type": "choice", "prompt": "Home setup?",
     "options": [
         {"id": "apt", "label": "Apartment"},
         {"id": "house", "label": "House with yard"},
         {"id": "shared", "label": "Shared / multi-pet home"},
     ]},
    {"id": "issues", "type": "choice", "multi": True, "prompt": "Top training goals (pick up to 2–3)",
     "options": [
         {"id": "potty", "label": "Potty training"},
         {"id": "bite", "label": "Puppy biting / nipping"},
         {"id": "pull", "label": "Leash pulling"},
         {"id": "bark", "label": "Barking"},
         {"id": "come", "label": "Recall (come when called)"},
         {"id": "crate", "label": "Crate comfort"},
         {"id": "jump", "label": "Jumping on people"},
     ]},
    {"id": "minutes", "type": "choice", "prompt": "Minutes you can train on most days?",
     "options": [
         {"id": "10", "label": "About 10 minutes"},
         {"id": "20", "label": "15–20 minutes"},
         {"id": "30", "label": "30+ minutes"},
     ]},
    {"id": "experience", "type": "choice", "prompt": "Your training experience?",
     "options": [
         {"id": "new", "label": "First dog / beginner"},
         {"id": "some", "label": "Some experience"},
         {"id": "exp", "label": "Experienced"},
     ]},
    {"id": "equipment", "type": "choice", "prompt": "Gear you already have?",
     "options": [
         {"id": "basic", "label": "Leash + collar/harness"},
         {"id": "crate", "label": "Above + crate"},
         {"id": "full", "label": "Crate, treats, toys, mats"},
         {"id": "unsure", "label": "Not sure / need a list"},
     ]},
    {"id": "aggression", "type": "choice", "prompt": "Has your dog ever bitten a person or dog hard enough to break skin, or shown serious aggression?",
     "help": "If yes, CueTrail is not the right next step — please seek a qualified professional.",
     "options": [
         {"id": "no", "label": "No"},
         {"id": "unsure", "label": "Unsure / mild reactivity only"},
         {"id": "yes", "label": "Yes — bite or serious aggression history"},
     ]},
    {"id": "vet", "type": "choice", "prompt": "Any known medical issues that affect movement or pain?",
     "options": [
         {"id": "no", "label": "None that I know of"},
         {"id": "yes", "label": "Yes — I’ll keep sessions gentle and ask my vet"},
         {"id": "unsure", "label": "Unsure"},
     ]},
]


def ct_plan(a: dict[str, Any]) -> dict:
    name = a.get("dog_name") or "your dog"
    age = _label(CT_Q[1]["options"], a.get("age"))
    issues = _labels_multi(CT_Q[4]["options"], a.get("issues") or ["come"])
    mins = _label(CT_Q[5]["options"], a.get("minutes"))
    aggro = a.get("aggression", "no")
    safety = []
    if aggro == "yes":
        safety.append("STOP: Because you reported bite/serious aggression history, do not use online drills for that behavior. Contact a certified trainer or veterinary behaviorist before continuing.")
    elif aggro == "unsure":
        safety.append("If barking/reactivity escalates toward lunging or biting, pause and get in-person professional help.")
    if a.get("vet") in ("yes", "unsure"):
        safety.append("Keep sessions short and pain-aware; ask your veterinarian if anything seems uncomfortable.")
    safety.append("CueTrail is general education, not a substitute for a veterinarian or qualified behavior professional.")
    day1 = [
        f"Name game: say “{name}!” then reward attention (5 × 30s games).",
        "Mark & reward calm feet on the floor (no jumping practice yet).",
        f"Potty or settle: based on goals ({issues}), start with the easiest win indoors.",
    ]
    return {
        "title": f"CueTrail 30-day plan for {name}",
        "summary": f"Age band: {age}. Focus areas: {issues}. Daily budget: {mins}. Force-free, short sessions. No behavior outcome is guaranteed.",
        "preview_sections": [
            {"title": "Safety first", "bullets": safety},
            {"title": "Session shape", "bullets": [
                f"Most days: {mins} total, split into 2–3 mini sessions.",
                "End while your dog is still successful — quit before frustration.",
                "Use soft treats or kibble; skip if your vet advised otherwise.",
            ]},
            {"title": "Days 1–3 (unlocked)", "bullets": day1 + ["Day 2–3: Repeat Day 1 and add a 1-minute leash-in-house walk with rewards for slack leash."]},
        ],
        "locked_sections": [
            {"title": "Days 4–30 protocol", "teaser": "Progressive drills matched to your selected goals."},
            {"title": "Troubleshooting cards", "teaser": "If X happens, try Y — with escalation flags."},
            {"title": "Equipment checklist", "teaser": "Only humane, standard gear suggestions."},
            {"title": "Week 5+ modules", "teaser": "Advanced skills after the founding plan unlocks."},
        ],
    }


# ---------- ReplyPath ----------
RP_Q = [
    {"id": "craft", "type": "choice", "prompt": "What do you mainly sell as a freelancer?",
     "options": [
         {"id": "design", "label": "Design / brand"},
         {"id": "dev", "label": "Development / no-code"},
         {"id": "writing", "label": "Writing / content"},
         {"id": "marketing", "label": "Marketing / ads"},
         {"id": "video", "label": "Video / photo"},
         {"id": "other", "label": "Other specialty"},
     ]},
    {"id": "clients", "type": "choice", "prompt": "How many paying clients did you have last month?",
     "options": [
         {"id": "0", "label": "0"},
         {"id": "1", "label": "1–2"},
         {"id": "3", "label": "3–5"},
         {"id": "6", "label": "6+"},
     ]},
    {"id": "channels", "type": "choice", "multi": True, "prompt": "Which outreach channels will you use?",
     "options": [
         {"id": "email", "label": "Cold or warm email"},
         {"id": "linkedin", "label": "LinkedIn"},
         {"id": "community", "label": "Communities / Slack / Discord"},
         {"id": "referrals", "label": "Referral asks"},
         {"id": "content", "label": "Content → inbound"},
     ]},
    {"id": "ideal", "type": "text", "prompt": "Describe your ideal client in one line", "placeholder": "e.g. Series A SaaS marketing leads"},
    {"id": "capacity", "type": "choice", "prompt": "Hours per week for outreach (not delivery)?",
     "options": [
         {"id": "3", "label": "About 3 hours"},
         {"id": "5", "label": "About 5 hours"},
         {"id": "8", "label": "8+ hours"},
     ]},
    {"id": "portfolio", "type": "choice", "prompt": "Portfolio readiness?",
     "options": [
         {"id": "strong", "label": "Strong case studies"},
         {"id": "ok", "label": "A few samples"},
         {"id": "weak", "label": "Needs work"},
         {"id": "none", "label": "Starting from scratch"},
     ]},
    {"id": "pricing", "type": "choice", "prompt": "Pricing comfort (ranges only — not financial advice)",
     "options": [
         {"id": "hourly", "label": "Mostly hourly"},
         {"id": "project", "label": "Project fees"},
         {"id": "retainer", "label": "Retainers"},
         {"id": "unsure", "label": "Still figuring it out"},
     ]},
    {"id": "blocker", "type": "choice", "prompt": "Biggest pipeline blocker?",
     "options": [
         {"id": "list", "label": "I don’t know who to contact"},
         {"id": "message", "label": "I don’t know what to say"},
         {"id": "followup", "label": "I don’t follow up"},
         {"id": "fear", "label": "Fear of rejection"},
         {"id": "time", "label": "No consistent time block"},
     ]},
    {"id": "offer", "type": "text", "prompt": "Name one clear offer you can pitch this month", "placeholder": "e.g. 3-page landing page redesign"},
    {"id": "tone", "type": "choice", "prompt": "Outreach tone?",
     "options": [
         {"id": "direct", "label": "Direct & brief"},
         {"id": "warm", "label": "Warm & personal"},
         {"id": "expert", "label": "Expert / insight-led"},
     ]},
]


def rp_plan(a: dict[str, Any]) -> dict:
    craft = _label(RP_Q[0]["options"], a.get("craft"))
    ideal = a.get("ideal") or "your ideal client"
    offer = a.get("offer") or "your clear offer"
    channels = _labels_multi(RP_Q[2]["options"], a.get("channels") or ["linkedin"])
    hours = _label(RP_Q[4]["options"], a.get("capacity"))
    blocker = _label(RP_Q[7]["options"], a.get("blocker"))
    tone = _label(RP_Q[9]["options"], a.get("tone"))
    weekly_sends = {"3": 15, "5": 25, "8": 40}.get(a.get("capacity", "5"), 25)
    return {
        "title": f"ReplyPath 30-day client-acquisition system ({craft})",
        "summary": f"Ideal client focus: {ideal}. Offer: {offer}. Channels: {channels}. Time budget: {hours}. This is a process plan only — no income, client-count, or revenue promises.",
        "preview_sections": [
            {"title": "Rules of the road", "bullets": [
                "Track process metrics only: sends, replies, conversations booked — not revenue targets.",
                "No fake scarcity, no fabricated results in outreach.",
                f"Primary blocker to design around: {blocker}.",
                f"Tone: {tone}.",
            ]},
            {"title": "Weekly outreach cadence", "bullets": [
                f"Aim for about {weekly_sends} thoughtful touches/week across {channels} (quality over spray).",
                "Block 2–3 fixed outreach sessions on your calendar.",
                "Same-day note every reply; follow-up #1 on day 3; follow-up #2 on day 7 if silent.",
            ]},
            {"title": "Week 1 focus (unlocked)", "bullets": [
                f"Day 1: Write a 1-sentence offer for “{offer}”.",
                f"Day 2: Build a list of 20 accounts matching “{ideal}”.",
                "Day 3: Draft 3 message variants; send the first 5.",
                "Day 4–5: Send next batch; log replies in a simple sheet.",
            ]},
        ],
        "locked_sections": [
            {"title": "Weeks 2–4 calendar", "teaser": "Daily outreach blocks, referral scripts, and portfolio gap fixes."},
            {"title": "Message swipe file", "teaser": "Templates in your chosen tone — edit heavily; don’t spam."},
            {"title": "Proposal outline", "teaser": "Scope, timeline, and assumptions — not pricing advice."},
            {"title": "Weekly review ritual", "teaser": "Process metrics dashboard prompts."},
        ],
    }


BRANDS = {
    "shelfspeak": {
        "name": "ShelfSpeak",
        "slug": "shelfspeak",
        "tagline": "A 30-day content calendar built for your shop — not a generic template.",
        "eyebrow": "For local businesses who freeze at the caption box",
        "hero_title": "Stop guessing what to post. Get a month of shop-ready content angles.",
        "hero_lede": "Answer a short quiz about your business, platforms, and capacity. ShelfSpeak builds a practical 30-day calendar with caption formulas and photo prompts.",
        "cta_primary": "Build my content calendar",
        "cta_short": "Start quiz",
        "cta_band_title": "Ready for a calmer content month?",
        "cta_band_text": "Three minutes of questions. A plan you can actually execute between customers.",
        "honesty_line": "No follower, viral, or booking guarantees — just a clear posting plan.",
        "audience_line": "Owners and managers of salons, cafes, clinics, contractors, and shops who know they “should post” but stall on what to say.",
        "personas": [
            {"title": "Solo shop owner", "text": "You wear every hat and need a week’s posts in one sitting."},
            {"title": "Front-desk marketer", "text": "You can publish — you just need angles that match the brand voice."},
            {"title": "Multi-location lead", "text": "You want a repeatable cadence staff can follow."},
        ],
        "how_steps": [
            {"title": "Take the quiz", "text": "Tell us your niche, city, platforms, voice, and weekly capacity."},
            {"title": "See your plan", "text": "Get a personalized calendar preview with Week 1 unlocked."},
            {"title": "Join founding list", "text": "Checkout isn’t live yet — save your spot for when subscriptions open."},
        ],
        "features": [
            {"title": "Cadence that fits", "text": "Plans scale from 1 post/week to near-daily without shame."},
            {"title": "Caption formulas", "text": "Hook → proof → soft CTA matched to your voice."},
            {"title": "Asset-aware prompts", "text": "Phone-only? Pro kit? We adjust the shot list."},
            {"title": "Monthly refresh", "text": "Subscription angle: a new calendar pack each cycle."},
        ],
        "sample_peek": [
            "Week 1: offer spotlight + soft booking CTA",
            "Photo prompt: 3 phone shots before open",
            "Caption formula in your chosen voice",
            "Friday: community / local nod post",
        ],
        "trust_points": [
            {"title": "Education, not hype", "text": "We teach a posting system. We don’t promise leads or virality."},
            {"title": "No fake social proof", "text": "No invented testimonials or user counts on this prototype."},
            {"title": "Clear pricing language", "text": "Intro and renewal terms shown before any future checkout."},
        ],
        "faq": [
            {"q": "Will you post for me?", "a": "Not in this version. You get a plan and drafts to publish yourself (or hand to a teammate)."},
            {"q": "Is checkout live?", "a": "No. The paywall is a founding-list flow with no real charges."},
            {"q": "Can I use this with SolvFix?", "a": "Yes — visibility fixes and content cadence pair well, but they are separate products."},
        ],
        "pricing": [
            {"id": "4w", "name": "4-week plan", "intro": "$19.99", "period": "first 4 weeks", "renewal": "$39.99 / 4 weeks",
             "includes": ["30-day calendar", "Caption formulas", "Email plan delivery (when live)"]},
            {"id": "12w", "name": "12-week plan", "intro": "$49.99", "period": "first 12 weeks", "renewal": "$79.99 / 12 weeks", "featured": True,
             "includes": ["3 monthly calendars", "Seasonal swap-ins", "Priority founding access"]},
        ],
        "disclaimer_short": "Educational content planning only. No guarantees of reach, engagement, followers, or revenue.",
        "disclaimer_long": "ShelfSpeak provides educational content calendars and drafting aids. It does not guarantee marketing results. You are responsible for complying with platform rules and advertising laws. This prototype processes no payments.",
        "font_url": "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;700&family=Source+Sans+3:wght@400;600;700&display=swap",
        "questions": SS_Q,
        "generate_plan": ss_plan,
        "secret_env": "SHELFSPEAK_SECRET",
        "admin_env": "SHELFSPEAK_ADMIN_PASSWORD",
        "db_env": "SHELFSPEAK_DB",
        "port": 5101,
        "logo_svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none"><rect width="64" height="64" rx="14" fill="#C45C26"/><path d="M14 40V24h8.5c4.2 0 7 2.4 7 6.1 0 3.8-2.8 6.2-7.1 6.2H20v3.7H14zm6-8.4h2.1c1.8 0 2.9-.9 2.9-2.3s-1-2.2-2.8-2.2H20v4.5zM34.2 40l4.7-16h6.4l4.7 16h-6.1l-.7-2.7h-5.1l-.7 2.7h-3.2zm8.2-7.1l-1.5-5.7-1.5 5.7h3z" fill="#FFF8F1"/></svg>''',
    },
    "signmatch": {
        "name": "SignMatch",
        "slug": "signmatch",
        "tagline": "Make your business name, address, and phone match everywhere customers look.",
        "eyebrow": "Listing consistency for local owners",
        "hero_title": "A clear roadmap to clean up mismatched business listings.",
        "hero_lede": "Quiz your directories, access, and weekly capacity. SignMatch builds a week-by-week NAP and profile checklist — education only, no auto-edits.",
        "cta_primary": "Build my visibility plan",
        "cta_short": "Start quiz",
        "cta_band_title": "Start with one source of truth.",
        "cta_band_text": "Then fix the directories that matter — in an order you can finish.",
        "honesty_line": "No ranking, call, or revenue guarantees. We never auto-edit your listings.",
        "audience_line": "Local business owners who noticed wrong hours, phones, or duplicate listings — especially after a move or rebrand.",
        "personas": [
            {"title": "Owner-operator", "text": "You need a punch list, not an agency deck."},
            {"title": "SolvFix scan user", "text": "You already saw exposure gaps and want a fix plan."},
            {"title": "Office manager", "text": "You can log in — you just need the order of operations."},
        ],
        "how_steps": [
            {"title": "Quiz your footprint", "text": "Pain points, directories, access, and hours available."},
            {"title": "Get the roadmap", "text": "Source-of-truth NAP plus Week 1 unlock."},
            {"title": "Founding list", "text": "No charge today — we’ll email when checkout opens."},
        ],
        "features": [
            {"title": "NAP source of truth", "text": "One copy-paste name, address, phone."},
            {"title": "Effort-aware schedule", "text": "Plans respect 1-hour or 5-hour weeks."},
            {"title": "SolvFix-friendly", "text": "Pairs with the free Business Exposure Scan."},
            {"title": "Monthly re-check", "text": "Subscription: catch drift after holidays and moves."},
        ],
        "sample_peek": [
            "Lock one official NAP string",
            "Week 1: access + phone fixes",
            "Directory priority order",
            "Re-scan reminder tied to SolvFix",
        ],
        "trust_points": [
            {"title": "You stay in control", "text": "Edits happen in each platform’s own tools."},
            {"title": "Honest claims", "text": "Checklists and education — not SEO miracles."},
            {"title": "Privacy-minded prototype", "text": "Local SQLite storage; no analytics wired."},
        ],
        "faq": [
            {"q": "Do you change my Google listing for me?", "a": "No. SignMatch never auto-edits Google, Yelp, Facebook, or other listings."},
            {"q": "Is this the same as SolvFix?", "a": "SolvFix scans exposure. SignMatch is a guided cleanup plan you can use after a scan."},
            {"q": "Will this get me to #1 on Maps?", "a": "We don’t promise rankings or leads."},
        ],
        "pricing": [
            {"id": "4w", "name": "4-week cleanup", "intro": "$24.99", "period": "first 4 weeks", "renewal": "$39.99 / 4 weeks",
             "includes": ["NAP roadmap", "Weekly checklists", "Review-request scripts (ethical)"]},
            {"id": "12w", "name": "12-week consistency", "intro": "$59.99", "period": "first 12 weeks", "renewal": "$79.99 / 12 weeks", "featured": True,
             "includes": ["3 monthly modules", "Re-scan cadence", "Seasonal hours pack"]},
        ],
        "disclaimer_short": "Educational listing checklists only. No auto-edits. No ranking or lead guarantees.",
        "disclaimer_long": "SignMatch provides educational guidance for business listing consistency. It does not modify third-party listings, guarantee search rankings, call volume, or revenue, and is not affiliated with Google, Yelp, or Apple. No payments are processed in this prototype.",
        "font_url": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Space+Grotesk:wght@600;700&display=swap",
        "questions": SM_Q,
        "generate_plan": sm_plan,
        "secret_env": "SIGNMATCH_SECRET",
        "admin_env": "SIGNMATCH_ADMIN_PASSWORD",
        "db_env": "SIGNMATCH_DB",
        "port": 5102,
        "logo_svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none"><rect width="64" height="64" rx="12" fill="#0E7C86"/><path d="M18 38V26h4.2l6.3 8.2V26H33v12h-4.2L22.5 29.7V38H18zM36.5 38l4.2-12h5.2l4.2 12h-4.5l-.7-2.2h-3.3L41 38h-4.5zm6.6-5.3l-1.1-3.7-1.1 3.7h2.2z" fill="#F2FFFE"/></svg>''',
    },
    "cuetrail": {
        "name": "CueTrail",
        "slug": "cuetrail",
        "tagline": "A day-by-day dog training plan shaped by your dog, home, and schedule.",
        "eyebrow": "Force-free · education only",
        "hero_title": "A calmer 30-day training path for real homes — not perfect Instagram dogs.",
        "hero_lede": "Tell us your dog’s age, goals, and how many minutes you have. CueTrail builds short, humane sessions with clear safety flags.",
        "cta_primary": "Build my dog’s plan",
        "cta_short": "Start quiz",
        "cta_band_title": "Short sessions. Clear cues. Safety first.",
        "cta_band_text": "If there’s bite history or medical pain, we point you to a professional — not a downloadable drill.",
        "honesty_line": "General education only — not a vet or behaviorist replacement. No outcome guarantees.",
        "audience_line": "New puppy parents and frustrated dog owners who want a structured plan that fits apartment or house life.",
        "personas": [
            {"title": "New puppy home", "text": "Potty, biting, and crate basics in tiny daily chunks."},
            {"title": "Busy adult-dog home", "text": "Leash manners and recall without hour-long sessions."},
            {"title": "Multi-pet household", "text": "Plans that respect shared space and overstimulation."},
        ],
        "how_steps": [
            {"title": "Quiz your dog", "text": "Age, home, goals, gear, and safety screens."},
            {"title": "Get Days 1–3 free in preview", "text": "See the session shape before any future unlock."},
            {"title": "Founding list", "text": "No payment today — optional notify when subscriptions open."},
        ],
        "features": [
            {"title": "Safety screens", "text": "Aggression and medical flags divert to professionals."},
            {"title": "Minute-aware", "text": "10, 20, or 30+ minute daily budgets."},
            {"title": "Force-free framing", "text": "Reward-based cues; no intimidation protocols."},
            {"title": "Advanced modules later", "text": "Subscription for week 5+ skills."},
        ],
        "sample_peek": [
            "Safety check before drills",
            "Name game + settle starters",
            "Slack-leash indoor walk",
            "When to stop and call a pro",
        ],
        "trust_points": [
            {"title": "Education label", "text": "Not veterinary advice; not guaranteed behavior change."},
            {"title": "Escalate when needed", "text": "Bite history → seek certified help immediately."},
            {"title": "No scare marketing", "text": "We don’t shame owners or invent urgency."},
        ],
        "faq": [
            {"q": "My dog bit someone. Can I use this?", "a": "No online plan is enough. Choose “yes” on the aggression question and contact a qualified professional."},
            {"q": "Do you use punishment-based methods?", "a": "No. CueTrail is framed as force-free education."},
            {"q": "Is this a substitute for a trainer?", "a": "No. It’s a structured practice guide for everyday skills."},
        ],
        "pricing": [
            {"id": "4w", "name": "4-week path", "intro": "$27", "period": "first 4 weeks", "renewal": "$39.99 / 4 weeks",
             "includes": ["30-day protocol", "Troubleshooting cards", "Equipment checklist"]},
            {"id": "12w", "name": "12-week path", "intro": "$59", "period": "first 12 weeks", "renewal": "$79.99 / 12 weeks", "featured": True,
             "includes": ["Advanced modules", "Seasonal packs (e.g. fireworks prep education)", "Progress checklists"]},
        ],
        "disclaimer_short": "General education only. Not a vet/behaviorist. Seek professionals for aggression or medical issues. No outcome guarantees.",
        "disclaimer_long": "CueTrail provides general dog-training education and practice structures. It does not diagnose medical or behavioral disorders, guarantee training outcomes, or replace a veterinarian, certified trainer, or veterinary behaviorist. If your dog shows aggression, bite history, or pain, seek qualified in-person help. This prototype processes no payments.",
        "font_url": "https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800&family=Nunito+Sans:wght@400;600;700&display=swap",
        "questions": CT_Q,
        "generate_plan": ct_plan,
        "secret_env": "CUETRAIL_SECRET",
        "admin_env": "CUETRAIL_ADMIN_PASSWORD",
        "db_env": "CUETRAIL_DB",
        "port": 5103,
        "logo_svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none"><rect width="64" height="64" rx="18" fill="#4F7A4E"/><path d="M20 36c0-6.6 4.2-11 10-11s10 4.4 10 11c0 2.2-.5 4.2-1.5 5.8-.4.6-1.2.7-1.7.2l-1.4-1.4a1 1 0 0 1-.1-1.2c.5-.9.7-1.9.7-3.4 0-4.1-2.6-7-7-7s-7 2.9-7 7c0 1.5.3 2.5.7 3.4a1 1 0 0 1-.1 1.2l-1.4 1.4c-.5.5-1.3.4-1.7-.2C20.5 40.2 20 38.2 20 36z" fill="#F5FFF3"/><circle cx="26" cy="22" r="3" fill="#A7D3A0"/><circle cx="38" cy="22" r="3" fill="#A7D3A0"/><circle cx="22" cy="28" r="2.2" fill="#A7D3A0"/><circle cx="42" cy="28" r="2.2" fill="#A7D3A0"/></svg>''',
    },
    "replypath": {
        "name": "ReplyPath",
        "slug": "replypath",
        "tagline": "A 30-day client outreach system for freelancers — process only, no income promises.",
        "eyebrow": "Pipeline hygiene for independents",
        "hero_title": "Know who to contact, what to say, and when to follow up.",
        "hero_lede": "ReplyPath turns a short quiz into a week-by-week outreach cadence with message frameworks and process metrics — never earnings claims.",
        "cta_primary": "Build my outreach plan",
        "cta_short": "Start quiz",
        "cta_band_title": "Consistency beats spray-and-pray.",
        "cta_band_text": "Get a plan that fits your hours and channels — then track sends and replies, not fantasies.",
        "honesty_line": "No income, client-count, or “land 10 clients” guarantees. Process education only.",
        "audience_line": "Freelancers with real skills and a lumpy pipeline who need an outreach operating system.",
        "personas": [
            {"title": "Feast-or-famine freelancer", "text": "You deliver well but stop prospecting when busy."},
            {"title": "Specialist switching niches", "text": "You need a tighter ideal-client list and offer line."},
            {"title": "Quiet expert", "text": "You dislike hype — you want brief, honest messages."},
        ],
        "how_steps": [
            {"title": "Quiz your pipeline", "text": "Craft, channels, capacity, offer, and blockers."},
            {"title": "Preview Week 1", "text": "List-building and first sends unlocked."},
            {"title": "Founding list", "text": "No charge today when you reserve a future plan tier."},
        ],
        "features": [
            {"title": "Process metrics", "text": "Sends, replies, conversations — not revenue targets."},
            {"title": "Channel-aware", "text": "Email, LinkedIn, community, referrals, content."},
            {"title": "Tone controls", "text": "Direct, warm, or insight-led frameworks."},
            {"title": "Weekly refresh", "text": "Subscription: new scripts and review rituals."},
        ],
        "sample_peek": [
            "1-sentence offer lock",
            "20-account ideal-client list",
            "3 message variants",
            "Day-3 and day-7 follow-ups",
        ],
        "trust_points": [
            {"title": "FTC-sensitive category", "text": "We ban income promises and fake result screenshots."},
            {"title": "No spam playbook", "text": "Thoughtful volume caps based on your hours."},
            {"title": "Clear future billing terms", "text": "Intro vs renewal shown before any live checkout."},
        ],
        "faq": [
            {"q": "Will this make me $10k/month?", "a": "We don’t promise income. ReplyPath is outreach process education only."},
            {"q": "Do you send emails for me?", "a": "No. You send; we provide cadence and frameworks."},
            {"q": "Is pricing advice included?", "a": "Only high-level structure comfort — not financial or pricing advice."},
        ],
        "pricing": [
            {"id": "4w", "name": "4-week sprint", "intro": "$19.99", "period": "first 4 weeks", "renewal": "$39.99 / 4 weeks",
             "includes": ["30-day cadence", "Message frameworks", "Process tracker prompts"]},
            {"id": "12w", "name": "12-week system", "intro": "$49.99", "period": "first 12 weeks", "renewal": "$79.99 / 12 weeks", "featured": True,
             "includes": ["Weekly script packs", "Referral module", "Proposal outline"]},
        ],
        "disclaimer_short": "Process education only. No income, client-count, or revenue guarantees.",
        "disclaimer_long": "ReplyPath provides educational outreach and pipeline process materials for freelancers. It does not guarantee clients, income, or business results, and does not provide financial, legal, or tax advice. Do not use templates to spam or misrepresent your work. This prototype processes no payments.",
        "font_url": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Syne:wght@600;700;800&display=swap",
        "questions": RP_Q,
        "generate_plan": rp_plan,
        "secret_env": "REPLYPATH_SECRET",
        "admin_env": "REPLYPATH_ADMIN_PASSWORD",
        "db_env": "REPLYPATH_DB",
        "port": 5104,
        "logo_svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none"><rect width="64" height="64" rx="10" fill="#F0B429"/><path d="M16 40V24h6l8 10.5V24h5v16h-6l-8-10.5V40H16zM40 40V24h12v4.2H45.2v2.4H51V35h-5.8v5H40z" fill="#1A1405"/></svg>''',
    },
}
