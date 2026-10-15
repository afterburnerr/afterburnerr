# Profile direction

Reviewed on 15 October 2026. These are references for restraint, not a ranking.

- [Anthony Fu](https://github.com/antfu): a very compact profile README built around a single line of links.
- [Paco Coursey](https://github.com/pacocoursey): a sparse profile; no profile README at the time of review.
- [Shu Ding](https://github.com/shuding): concise bio and personal links; no profile README at the time of review.
- [Sindre Sorhus](https://github.com/sindresorhus): an intentionally maximalist retro profile. Reviewed as a contrast, not used as a minimalist reference.

## Design

The nickname is the visual anchor. Two slanted strokes suggest an afterburner without turning the profile into a dashboard. Everything else uses GitHub's native text rendering.

The wordmark is original. Its lettering is outlined from Nimbus Sans Bold so it renders consistently without fetching fonts. Light and dark variants have transparent backgrounds and are selected with `<picture>`.

Palette: light ink `#1f2328`, dark ink `#f0f3f6`, light accent `#bc441c`, dark accent `#ff875f`. Backgrounds come from GitHub itself. The accent appears only in the symbol.

The layout is left aligned. The header scales to its container; the sentence and language list remain native, selectable text. No animation, statistics, project cards, external image services, or scheduled jobs are needed.

The previous design is retained in Git history.

## Editing

Edit `README.md` to change the introduction. Edit the two files in `assets/` together to change the wordmark. A new project can be pinned on GitHub when it is ready; this README does not need a placeholder portfolio.
