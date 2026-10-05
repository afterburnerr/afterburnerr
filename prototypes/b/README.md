# afterburnerr / night shift

This is a deliberately strange profile concept: a 03:17 night-shift janitor is physically sorting four stubborn code windows. `aftsync`, `TownyRaids`, `FreeDeepSeekAPI`, and `warehouse-dashboards` are props in the story, not a statistics wall. Every ten seconds the worker patrols left-to-right, reaches for a window, and nudges it into a crooked archive. The dust, cursor, blinking eyes, and moon flicker make the loop feel like a tiny place with a routine.

## Preview

Open `index.html` in a browser through a local server (for example `python3 -m http.server`) and use the two native buttons. `freeze the worker` applies a visible still state; `resume shift` restores the animation. GitHub itself will render the SVG animation, but cannot run the preview page's JavaScript controls.

## Embedding

For a profile README, use the standalone asset directly:

```html
<img src="./prototypes/b/scene.svg" alt="afterburnerr's 03:17 night shift: a tiny janitor sorts floating repository windows." width="1200">
```

An SVG `<img>` is portable and keeps the CSS animation. A GitHub profile README cannot execute arbitrary HTML controls or JavaScript, so the interactive buttons belong only to the local prototype.

## A future Issues mechanism

The scene could become a gentle, opt-in GitHub Issues game: a scheduled workflow would choose one open issue tagged `night-shift` and generate a small, signed `state.json` (window position, shift note, and timestamp). The SVG can consume that state only when a maintainer deliberately republishes the asset; the README would link the issue that supplied the current prop. A `night-shift` issue template could accept a repository name and one-line “what is misplaced?” prompt. No automatic issue creation, commenting, or contributor tracking should happen without explicit opt-in, and the public profile should show only repository names already intended to be public.
