Output "diagnostics.gif"

Set Shell bash
Set FontSize 14
Set Width 920
Set Height 320
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

Sleep 800ms

# Open a new line inside the empty module and type a new variable
Type "o"
Type "    let x: logic = 1;"
Escape

# Wait for the unused warning to appear
Sleep 3000ms

# Notice the warning, jump to the variable name and add the `_` prefix
Type "/x"
Enter
Sleep 1500ms
Type "i_"
Escape

# Watch the warning disappear
Sleep 2500ms
