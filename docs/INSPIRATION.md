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

The layout is left aligned. The header scales to its container; the language list remains native, selectable text. The profile has no introductory tagline or project cards. An orange snake visualizes the contribution graph below the wordmark. See [snake setup](SNAKE.md) and [automated activity](ACTIVITY.md).

The previous design is retained in Git history.

## Editing

Edit `README.md` to change the visible profile content. Edit the two files in `assets/` together to change the wordmark. A new project can be pinned on GitHub when it is ready; this README does not need a placeholder portfolio.
