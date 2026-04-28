Output "synth.gif"

Set Shell bash
Set FontSize 14
Set Width 920
Set Height 700
Set Padding 22
Set TypingSpeed 60ms
Set Theme "GitHub Dark"

Hide
Type "cd demo && PS1='$ '"
Enter
Sleep 100ms
Type "export BAT_STYLE=plain BAT_PAGER=cat"
Enter
Sleep 100ms
Type "alias cat='bat --map-syntax=*.veryl:SystemVerilog --map-syntax=*.sv:SystemVerilog'"
Enter
Sleep 100ms
Type "clear"
Enter
Sleep 300ms
Show

Sleep 600ms

Type@30ms "cat src/counter.veryl"
Enter
Sleep 4000ms

Hide
Type "clear"
Enter
Sleep 200ms
Show

Type@30ms "veryl synth --top Counter"
Enter
Sleep 5500ms
