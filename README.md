# T3 Code themes

Custom themes for [T3 Code](https://github.com/pingdotgg/t3code).

## Deep Field

A slow flight through space behind the open thread: a sun, planets with rings, a moon, an asteroid belt and drifting stars. While the open thread is Working, light streaks race outward and the stars speed up.

The space effects show only in dark mode. The palette is the default T3 Code palette.

- `themes/deep-field.json`: the full theme file.
- `themes/deep-field.css`: the custom CSS only, for reading.

### Install

Copy the theme file into the T3 Code themes folder, then pick **Deep Field** in Settings > Appearance > Colors & themes.

```bash
cp themes/deep-field.json ~/.t3/userdata/themes/deep-field.json
```

### Limits

- Theme CSS cannot run JavaScript. The Working effect reads the thread status from the sidebar, so a T3 Code update can break it.
- The CSS is close to the 20,000-character limit for theme CSS.

## License

MIT
