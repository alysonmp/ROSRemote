///<?php
/// bond PHP interface loader
/// NOTE: use /// for comments *only*, as this code is transformed into a
///       single line to be injected into the interpreter *without parsing*.

/// PHP has limited control over eval's execution context. We cannot call eval
/// from within an anonymous scope as this would obliterate our global
/// definitions in stage2. As such, just prefix all global variables. We use
/// our own "eval" wrapper to control this behavior, but it's defined later.
echo strtoupper("stage2\n"); flush();
$__BOND_STDIN = fopen("php://stdin", "r");
$__BOND_STAGE2 = json_decode(rtrim(fgets($__BOND_STDIN)));
eval($__BOND_STAGE2->code);
call_user_func_array('__BOND_start', $__BOND_STAGE2->start);
