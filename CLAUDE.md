# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Meeting Brick Breaker is a single-file Python/Pygame game where the bricks are calendar meeting blocks from a weekly agenda. Destroying a brick "frees" the meeting.

## Setup and Running

```bash
pip install -r requirements.txt   # installs pygame==2.5.2
python meeting_brick_breaker.py   # launches the game window
```

Controls: `←` / `→` or `A` / `D` to move the paddle. `SPACE` to restart, `ESC` to quit after a game ends.

## Architecture

The entire game lives in `meeting_brick_breaker.py`. There are no tests, no linter config, and no other modules.

**Data layer**
- `MeetingBlock` — a `@dataclass` holding the data for one calendar event: `day`, `title`, `start` (HH:MM string), `duration_minutes`, `location`, `color` (RGB tuple).
- `MEETINGS` — a module-level `List[MeetingBlock]` with hardcoded weekly meeting data. `DAYS` is the ordered list of column headers.

**Game objects**
- `Paddle` — tracks its own `pygame.Rect`, handles keyboard input in `update(delta)`.
- `Ball` — stores position as `pygame.Vector2`, velocity as a vector. `reset()` places it at center with a random upward angle. The `rect` property returns a bounding `pygame.Rect` for collision.
- `Brick` — wraps a `pygame.Rect` and a `MeetingBlock`. Has an `active` flag. Day-label bricks (those whose `title` is in `DAYS`) are decorative and never deactivated.

**Game controller — `MeetingBrickBreaker`**
- `_create_bricks()` lays out bricks in day columns. Column width is computed from `WINDOW_WIDTH` and `len(DAYS)`. Brick height is proportional to `duration_minutes` (capped between 36 and 280 px). Day-label bricks sit at the top of each column.
- `run()` is the main loop at 60 FPS. It delegates to `paddle.update`, `ball.update`, then checks paddle collision (angle-based deflection using normalized overlap), out-of-bounds (loses a life), and brick collisions.
- `_handle_ball_brick_collision()` uses a minimum-overlap method across four sides to determine the correct bounce direction and repositions the ball to avoid tunneling.
- `_render()` draws all objects plus a fixed HUD bar at the bottom showing progress, lives, streak, and last cleared meeting.
- `_render_end_screen()` / `_reset_game()` handle win/loss state.

## Key Constants

| Constant | Value | Purpose |
|---|---|---|
| `WINDOW_WIDTH / HEIGHT` | 1100 × 720 | Fixed window size |
| `FPS` | 60 | Target frame rate |
| `minutes_per_pixel` | 1.3 | Converts meeting duration to brick height |
| `COLUMN_GAP / ROW_GAP` | 6 px | Spacing between bricks |

## Extending the Game

To change the meetings shown as bricks, edit the `MEETINGS` list and/or `DAYS` list at the top of the file. Adding a new `MeetingBlock` to `MEETINGS` with an existing `day` value automatically places it in the correct column in chronological order (sorted by `start` in `_create_bricks`).
