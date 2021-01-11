﻿$Env:Path = $Env:Path + ";C:\Program Files\git\bin"
function prompt {
  $cur_dir = get-location
  $esc = [char]27
  "$esc[42;30m$env:username@$env:computername $esc[44;32m$esc[44;30m $cur_dir $esc[40;34m$esc[0m $ "
}

function ln($target, $link) {
  new-item -path $link -itemType SymbolicLink -value $target
}

function ll($parms) {
  get-childitem -force $parms
}