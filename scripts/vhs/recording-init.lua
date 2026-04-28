-- Minimal nvim init used only by vhs tape recordings.
-- Launches veryl-ls for *.veryl files via the built-in LSP client,
-- uses the SystemVerilog syntax as a visual fallback for highlighting,
-- and trims away cmdline / statusline / mode indicator chrome so the
-- recorded frame contains only the code and LSP diagnostics.

vim.opt.cmdheight    = 0
vim.opt.laststatus   = 0
vim.opt.showmode     = false
vim.opt.ruler        = false
vim.opt.number       = true
vim.opt.signcolumn   = "yes"
vim.opt.termguicolors = true
vim.opt.background    = "dark"

-- Recording session is throwaway; skip swap / backup / undofile
-- so a previous interrupted recording does not block the next one.
vim.opt.swapfile = false
vim.opt.backup   = false
vim.opt.writebackup = false
vim.opt.undofile = false

-- `sorbet` is built-in since nvim 0.10 (warm dark, readable syntax + diagnostics)
pcall(vim.cmd, "colorscheme sorbet")

vim.filetype.add({ extension = { veryl = "veryl" } })

vim.api.nvim_create_autocmd("FileType", {
  pattern = "veryl",
  callback = function()
    local bufnr = vim.api.nvim_get_current_buf()
    vim.bo[bufnr].syntax = "systemverilog"
    vim.lsp.start({
      name = "veryl-ls",
      cmd  = { "veryl-ls" },
      root_dir = vim.fs.dirname(
        vim.fs.find({ "Veryl.toml" }, { upward = true })[1]
          or vim.fn.getcwd()
      ),
    })
    -- Enable LSP inlay hints (nvim 0.10+) so the type-inference recipe
    -- can show inferred types inline.
    pcall(function()
      vim.lsp.inlay_hint.enable(true, { bufnr = bufnr })
    end)
  end,
})
