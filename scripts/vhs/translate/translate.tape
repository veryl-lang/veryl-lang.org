Output "translate.gif"

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
Type "rm -f counter.veryl"
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

Type@30ms "cat counter.sv"
Enter
Sleep 3500ms

Type@30ms "veryl translate counter.sv"
Enter
Sleep 2000ms

Type@30ms "cat counter.veryl"
Enter
Sleep 4500ms
