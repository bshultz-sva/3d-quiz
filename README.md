# 3D QUIZ

A flip-card study game for the After Effects 3D material in Motion Design.

**Play it in your browser:** https://bshultz-sva.github.io/3d-quiz/  (any modern browser on Mac, Windows or Chromebook; the first load takes a few seconds, then click to start)

## Run it on your own computer instead

    pip install pygame-ce
    python3 3d_quiz.py

## How to play

  Press a number to pick a deck:
    1 3D space & layers   2 Cameras   3 Lights & materials   4 Text, keying & tricks
    5 Output & compression   6 Audio react   7 Everything (135 cards)   8 Flagged in class (23 cards)
  Click a deck (or press its number). Click the card or press Space to flip it. Then click Knew it / Study again (or Y / N).
  Missed cards come back a few cards later. Esc goes back to the menu, or quits from the menu.
  Starred cards are things the teacher flagged in class as quiz material.

## Where the cards come from

  The class recordings in Motion Design:
    diorama_export (1): 3D geometry, cameras, lights, Substance materials, Media Encoder
      and compression, Photoshop batch actions
    time travel (and week_8_tunnel_videos_export): 2.5D, 3D layers, lights and material
      options, per-character 3D, keying, Auto-Orient, the photo tunnel, depth of field,
      rack focus
    audio_react_export: Audio Spectrum and Audio Waveform, panning, frequencies and
      bandwidth, Convert Audio to Keyframes, linking properties to sound with expressions
  All the cards are written inside 3d_quiz.py (the CARDS list near the top), so that one
  file is the whole game.

## The web version

`docs/` is the browser build, made with pygbag (`pip install pygbag`, then `pygbag --build` on a folder holding 3d_quiz.py renamed to main.py) and served by GitHub Pages.
