Title: Flow
Date: 2026-07-18
Tags: threejs, javascript, 3d
Summary: A 3D live venue capacity map concept for ROLLER -- explore a whole theme park's wait times as an interactive 3D scene.

Instead of a table of wait times, Flow renders a whole venue as an
explorable 3D space -- each attraction is a tower whose height and color
show its current wait time at a glance, from across the whole map at once.

## How it works

- Built with Three.js -- drag to orbit the camera, scroll to zoom
- A live simulation drifts each attraction's wait time every few seconds,
  clamped to a realistic range, with towers animating smoothly to match
- Click any tower, or any row in the sidebar, for that attraction's exact
  wait time and capacity in a detail panel
- A top-bar stat shows overall venue capacity, averaged live across all
  eight attractions

Modeled on a trampoline park / family entertainment center, with eight
attractions: Main Arena Trampolines, Ninja Warrior Course, Foam Pit,
Dodgeball Court, Toddler Zone, Climbing Wall, Battle Beam, and Arcade.

## Why this project exists

ROLLER is a Melbourne-built venue management platform used by theme parks,
waterparks, and family entertainment centers -- their real product already
does live capacity management through an admin dashboard. Flow explores a
different, spatial way to show the same information: glancing at a 3D map
and immediately seeing which attraction is backed up, without reading a
single number on a table.

## Stack

Three.js, HTML, CSS, JavaScript -- no build step, no framework.
