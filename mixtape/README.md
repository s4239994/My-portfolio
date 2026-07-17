# Mixtape

A genre hub for original mini-games -- like a streaming service, except
each genre is something you play instead of watch, and each one takes a
familiar genre and inverts one core assumption instead of cloning an
existing game.

## Status

- ✅ **Action -- "Overload"** -- fully working
- ⏳ Comedy, Finance, Horror, Thriller -- in progress, coming one at a time

## The concept

Every genre gets one genuinely different mechanic:

- **Action -- "Overload"** -- your energy bar isn't health, it's fuel.
  Getting hit by an enemy refuels you. Getting hit while you're already
  almost full overloads you -- game over. Pulse attacks (SPACE) clear
  enemies safely but cost the same energy you need to survive, so running
  low forces you back into the exact risk you're avoiding.
- **Comedy -- "Copycat"** *(coming next)* -- mimic an absurd, fast-changing
  pose sequence; failing triggers slapstick ragdoll physics instead of a
  simple miss.
- **Finance -- "Bubble"** *(coming next)* -- watch literal market bubbles
  inflate and pop in real time; profit by timing your cash-out against
  visible herd behavior instead of reading numbers on a chart.
- **Horror -- "Hush"** *(coming next)* -- fear widens your vision but makes
  your movement shakier, inverting the usual "fear impairs you" logic.
- **Thriller -- "Countdown"** *(coming next)* -- bank or borrow time
  between decisions, turning the clock itself into the resource you manage.

## How to play Overload

- **WASD / arrow keys** -- move
- **SPACE** -- pulse attack (clears nearby enemies, costs energy)
- Survive as long as you can. Score comes from defeating enemies and from
  time survived.

## Running it

Needs a JDK (built and tested on JDK 25). No external dependencies --
pure Java Swing.

```
mkdir out
javac -d out $(find src -name "*.java")
java -cp out Main
```

On Windows PowerShell:

```
mkdir out
Get-ChildItem -Recurse -Filter *.java src | ForEach-Object { $_.FullName } | Out-File sources.txt
javac -d out "@sources.txt"
java -cp out Main
```

## How it's organized

- **[src/common/GamePanel.java](src/common/GamePanel.java)** -- shared game-loop, input, and game-over base class every mini-game extends
- **[src/common/HighScores.java](src/common/HighScores.java)** -- local high-score persistence (`data/highscores.properties`, not committed)
- **[src/hub/](src/hub/)** -- the genre-picker menu and the window that hosts whichever game is active
- **[src/games/action/OverloadGame.java](src/games/action/OverloadGame.java)** -- the Action genre's game
- **[src/Main.java](src/Main.java)** -- entry point; this is where new genre entries get registered
