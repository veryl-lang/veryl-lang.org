# vhs recordings

GIF/MP4 demos used on the homepage are produced with [`charmbracelet/vhs`](https://github.com/charmbracelet/vhs).
Each subdirectory is a self-contained recipe (tape + minimal Veryl project) for one demo.

## Why vhs

Tapes are reproducible: re-record on every Veryl release, and the demo stays in sync
with the actual tool output. Editing copy or extending a sequence is a text diff,
not a screen recording session.

## Requirements

- `vhs` (v0.11+)
- `ffmpeg`
- `ttyd`
- `nvim` (built-in LSP client; no plugins required)
- `veryl` and `veryl-ls` on `PATH`

The recipes load [`recording-init.lua`](recording-init.lua) instead of the user's
own `init.lua`, so the recording is independent of personal plugins
(lualine, telescope, etc.). The init starts `veryl-ls` via `vim.lsp.start`,
borrows SystemVerilog syntax for highlighting, and trims away the cmdline /
statusline / mode indicator chrome.

## Running a recipe

From this directory:

```bash
make              # record every recipe
make diagnostics  # record only the diagnostics recipe
make install      # copy generated gifs into ../../static/img/
make clean        # delete generated gifs
```

The Makefile sets `ROD_BROWSER_FLAGS="--no-sandbox --disable-gpu"` for you,
which is required because `vhs` launches a headless Chromium via `go-rod` —
it fails in many sandboxed environments without those flags.

Each recipe writes its `.gif` next to its tape file. `make install`
copies them into `static/img/` for publication.

## Adding a new recipe

1. Create `scripts/vhs/<name>/` containing:
   - `<name>.tape`
   - `demo/Veryl.toml` and `demo/src/*.veryl.template` (or whatever the recipe needs)
   - `demo/.gitignore` for build artefacts (`target/`, generated sources)
2. Drive the demo from a clean state by copying the template into the live source file
   inside a `Hide` block, so re-running is idempotent.
3. Hide nvim startup and any plugin setup (e.g. `:lua require'lualine'.hide()`) inside
   the same `Hide` block, so the recording starts on the editor itself.
4. Keep `Sleep` values long enough that LSP diagnostics, hover popups, etc. are visible
   to the viewer — short Sleeps look fine while authoring but feel rushed on playback.

## Recipes

- [`diagnostics/`](diagnostics/) — `Real-time diagnostics` section on the homepage.
  Type a new `let` binding, watch the unused warning appear, fix it with a `_` prefix.
- [`format/`](format/) — `Auto formatting` section on the homepage.
  Open a poorly-formatted file, trigger `vim.lsp.buf.format()`, watch the source get reformatted.
- [`synth/`](synth/) — `Logic synthesis support` section on the homepage.
  Show a counter module, run `veryl synth`, watch the gate-level area / timing / power report.
- [`translate/`](translate/) — `SystemVerilog translation` section on the homepage.
  Show a SystemVerilog counter, run `veryl translate`, then show the generated Veryl source.
