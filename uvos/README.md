# uvos

A Linux-desktop-styled sun exposure monitor, powered by real, live UV Index
data from ARPANSA (Australia's radiation protection agency) -- not a
simulation. Tracks your unprotected burn-time budget for your actual skin
type at the actual current UV Index in your city, logs sun sessions, and
has Claude write terse, daemon-style advisory messages grounded in the
real numbers.

## Why this project exists

Built with Melbourne's health/biotech scene in mind (Heidi Health and the
broader AI-healthtech cluster), but pointed at a genuinely huge, current,
local public health problem instead of a hypothetical one: Australia has
the highest melanoma rate in the world, more than 2 in 3 Australians will
be diagnosed with some form of skin cancer by age 70, and the UV Index
regularly hits "extreme" (10+) in Australian summer. Sun-safety advice
exists everywhere, but almost nothing turns *your specific skin type* and
*today's actual UV reading in your city* into a concrete number: how many
minutes until you burn, right now.

## What it does

1. **Live UV data** -- fetches the real, current UV Index for any Australian
   capital city straight from ARPANSA's public monitoring network (falls
   back to the most recent available reading if today's data hasn't
   published yet)
2. **Skin profile** -- a short Fitzpatrick-scale quiz maps you to a real
   dermatological reference range (Minimal Erythema Dose)
3. **Burn-time math** -- combines the WHO's own UV Index formula
   (UVI = 40 x erythemal irradiance) with your MED to calculate real
   unprotected burn time in minutes, not a guess
4. **Session tracking** -- start a sun session, track elapsed exposure
   against your calculated budget, log it to a local history
5. **AI advisory** -- Claude writes a short, terminal-daemon-style warning
   grounded only in the actual UV reading, skin type, and elapsed time --
   never an invented medical claim

## On the sources

- Live UV data: [ARPANSA](https://www.arpansa.gov.au/our-services/monitoring/ultraviolet-radiation-monitoring) -- Australia's official radiation protection agency
- UV Index formula: World Health Organization, *Global Solar UV Index: A Practical Guide* (2002)
- Minimal Erythema Dose reference ranges by Fitzpatrick skin type: standard dermatology/sun-safety education references
- Skin cancer statistics: [Cancer Council Australia](https://www.cancer.org.au/cancer-information/causes-and-prevention/sun-safety/uv-index)

This is a sun-safety awareness tool, not a diagnostic or medical device --
it doesn't diagnose anything, only translates public UV data and published
reference ranges into a concrete number.

## Setup

```
pip install -r requirements.txt
```

Get a free Anthropic API key at https://console.anthropic.com/settings/keys,
then copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and
fill in your key. The UV status, burn-time calculation, and session
tracking all work without a key -- only the AI advisory needs it.

## Running it

```
streamlit run app.py
```

## How it's organized

- **[uv_api.py](uv_api.py)** -- live ARPANSA UV Index data, with fallback logic
- **[skin.py](skin.py)** -- the Fitzpatrick quiz and the real burn-time formula
- **[db.py](db.py)** -- SQLite session history
- **[advisory_ai.py](advisory_ai.py)** -- the Claude call that writes the advisory
- **[app.py](app.py)** -- the Linux-desktop-styled dashboard

## Cost

The AI advisory costs a small fraction of a cent per generation. Everything
else -- the live UV data, burn-time math, and session logging -- is
completely free.
