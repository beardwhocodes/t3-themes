# Agent guide: T3 Code themes

This repo holds custom themes for T3 Code. Use this guide to apply a theme to a user's T3 Code, or to add a new theme.

## Layout

Each theme has its own folder:

```
themes/<id>/
  <id>.json       The theme file. T3 Code uses the file name as the theme id.
  <id>.css        The theme's CSS only, for reading and review. Keep it the same as the "css" field.
  README.md       What the theme does, with screenshots or GIFs.
  *.png, *.gif    Previews.
```

## Apply a theme

Use one of these methods. Each one publishes the theme into the T3 Code data folder (`~/.t3/userdata/themes/<id>.json`) and makes it the active theme.

1. **T3 Code CLI (preferred).** From the repo root, run `t3 theme set themes/<id>/<id>.json`. Run `t3 theme show` to confirm the active theme.
2. **T3 MCP tool.** If you run inside T3 Code and have the `t3_theme_set` tool, call it with `themeId: "<id>"` and `theme:` the parsed contents of `<id>.json`.

To switch back to a theme that is already published, run `t3 theme set <id>`. To remove the environment theme, run `t3 theme clear`. The user can also pick a theme in **Settings > Appearance > Colors & themes**.

Some themes show effects only in dark mode. Read the theme's README and tell the user.

## Theme file rules

T3 Code rejects a theme that breaks these rules:

- `version` must be `1`.
- `colors` must be present. To keep the default look, copy `T3_CODE_LIGHT_THEME_COLORS` and `T3_CODE_DARK_THEME_COLORS` from `packages/shared/src/themePalettes.ts` in the T3 Code source. Put the dark palette in `variants.dark`.
- `css` must be 20,000 characters or fewer.
- The CSS must not use `@import` or external URLs. `url()` works only with `data:` URIs. Encode `#` as `%23` and `%` as `%25` in an inline SVG.

## CSS hooks

Theme CSS cannot run JavaScript. It can read only the DOM. The T3 MCP tool `t3_theme_read` returns the current list of stable selectors. These are the ones the themes here use:

- `[data-slot="sidebar-inner"]`: the sidebar surface.
- `[data-chat-header]`: the chat header.
- `.messages-timeline-scroll`: the chat scroller, above the area background.
- `[data-slot="composer-host"]`: the composer card.
- `[data-thread-item]`: a sidebar thread row.

These hooks also work, but they are not on the stable list, so a T3 Code update can break them:

- `[data-workspace-area="conversation"]`: the thread timeline area. Put backgrounds here, on `::before` and `::after` with `z-index: -1` and `isolation: isolate` on the area.
- `[data-sidebar-row]`: a sidebar thread row. Its `aria-label` is `"<title>, <status>, <project>"`. The open thread has `aria-current="page"`.
- Statuses: `Working`, `Connecting`, `Completed`, `Failed`, `Pending Approval`, `Awaiting Input`, `Plan Ready`.
- Example: `.dark:has([data-sidebar-row][aria-current="page"][aria-label*=", Working"])` matches while the open thread works.
- `.dark` on the root element marks dark mode.
- `var(--sidebar)` is the sidebar color from the theme palette.

To stay under the 20,000-character limit, put colors in the palette, not in CSS. Palette roles cost no CSS characters.

Keep text readable. Keep effects behind the timeline, and respect `prefers-reduced-motion`.

## Add a theme

1. Make the folder and files that the layout above shows.
2. Capture previews on a mock T3 Code page. The script needs Google Chrome and ffmpeg:
   `scripts/capture.sh themes/<id>/<id>.json idle 6 themes/<id>/preview`
   Use `working` in place of `idle` to show the effect for a working thread. The third argument speeds up the animations so the GIF shows motion. Say in the README if a GIF is sped up.
3. Add a row to the table in the root `README.md`.
