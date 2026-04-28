Output "format.gif"

Set Shell bash
Set FontSize 14
Set Width 920
Set Height 360
Set Padding 22
Set TypingSpeed 70ms
Set Theme "GitHub Dark"

Hide
Type "cd demo && PS1='$ '"
Enter
Sleep 200ms
Type "cp src/example.veryl.template src/example.veryl && rm -f src/.*.swp && clear"
Enter
Sleep 300ms
Type "nvim -u ../../recording-init.lua src/example.veryl"
Enter
Sleep 4s
Show

# Show the messy code first
Sleep 2500ms

# Trigger LSP format directly via the built-in API (visible on the cmdline)
Type ":lua vim.lsp.buf.format()"
Enter

# Watch the file get reformatted
Sleep 2500ms
