Title: Server & System Health Monitor
Date: 2026-07-04
Tags: python, systems, cli
Summary: A lightweight live terminal dashboard for CPU, memory, disk, and local open ports.

A background-friendly terminal dashboard that watches system vitals and
local network ports in real time, with color-coded health status and sound
alerts -- no browser, no heavy dependencies.

## How it works

- `psutil` reads CPU, memory, and disk usage every few seconds
- A threaded TCP connect-scan checks common ports on localhost
- `rich` draws a live-updating, color-coded terminal dashboard (green/yellow/red)
- A distinct sound plays whenever the overall health status changes -- not on
  every refresh, since a continuous hum in a background tool gets old fast
- Alerts are logged to a file so there's a record of what happened and when

## Stack

Python, psutil, rich, winsound.
