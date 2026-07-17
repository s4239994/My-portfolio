Title: uvos
Date: 2026-07-18
Tags: python, ai, health
Summary: A Linux-desktop-styled sun exposure monitor using real live government UV data and real dermatological burn-time math.

A Linux-desktop-styled sun exposure monitor -- powered by real, live UV
Index data from ARPANSA (Australia's radiation protection agency), not a
simulation. Tracks your unprotected burn-time budget for your actual skin
type at the actual current UV Index in your city.

## How it works

- Fetches the real, current UV Index for any Australian capital city
  straight from ARPANSA's public monitoring network
- A short skin-type quiz maps you to a real dermatological reference range
  (Minimal Erythema Dose)
- Combines the WHO's own UV Index formula with your MED to calculate real
  unprotected burn time in minutes, not a guess
- Tracks a live sun session against your calculated budget and logs history
- Claude writes a short, terminal-daemon-style advisory grounded only in
  the actual UV reading, skin type, and elapsed time

## Why this project exists

Built with Melbourne's health/AI scene in mind (Heidi Health and the
broader healthtech cluster), pointed at a real, current, local public
health problem: Australia has the highest melanoma rate in the world, and
more than 2 in 3 Australians will be diagnosed with some form of skin
cancer by age 70. Sun-safety advice is everywhere, but almost nothing
turns your specific skin type and today's actual UV reading into a
concrete number: minutes until you burn, right now.

## Stack

Python, Streamlit, SQLite, Claude API, ARPANSA public UV data.
