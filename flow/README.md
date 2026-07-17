# Flow

A 3D live venue capacity map -- a concept for ROLLER, the Melbourne-built
venue management platform used by theme parks, waterparks, and family
entertainment centers. Instead of a table of wait times, Flow renders the
whole venue as an explorable 3D space: each attraction is a tower whose
height and color show its current wait time at a glance, from across the
whole map at once.

**[View it locally](index.html)** -- open `index.html` in a browser (needs
WebGL, which every modern browser has).

## Why this project exists

ROLLER's real product already does real-time capacity management --
online, in the admin portal, you can see live capacity for every session
and adjust limits with a few clicks. That's a table/dashboard experience.
Flow explores a different, spatial way to show the same information: a
venue manager (or even a guest-facing kiosk) glancing at a 3D map and
immediately seeing which attraction is backed up, without reading a single
number.

Modeled on a trampoline park / family entertainment center -- one of
ROLLER's real, common customer types -- with eight attractions: Main Arena
Trampolines, Ninja Warrior Course, Foam Pit, Dodgeball Court, Toddler Zone,
Climbing Wall, Battle Beam, and Arcade.

## What it does

- **3D scene** -- built with Three.js; drag to orbit, scroll to zoom
- **Live simulation** -- every ~3 seconds, wait times drift up or down
  (clamped to a realistic 2-55 minute range), and each tower's height and
  color animate smoothly to match
- **Click any tower** -- or any row in the sidebar -- to see that
  attraction's exact wait time and capacity in a detail panel
- **Venue-wide stat** -- the top bar shows overall venue capacity, averaged
  live across all eight attractions

## A note on the data

The wait times are simulated for this demo, not connected to a real venue.
In a real deployment, this would subscribe to ROLLER's actual real-time
capacity API instead of the random-walk simulation in `main.js`.

## Stack

Plain HTML/CSS/JavaScript, [Three.js](https://threejs.org/) (loaded via CDN
import map, no build step, no framework).

## Running it

No build step -- open `index.html` directly, or serve it locally:

```
python -m http.server 8000
```

Then visit `http://localhost:8000`.
