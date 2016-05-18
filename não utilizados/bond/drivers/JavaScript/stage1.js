/// bond Javascript interface setup
/// NOTE: use /// for comments *only*, as this code is transformed into a
///       single line to be injected into the interpreter *without parsing*.
var fs = require("fs");

/// Define some constants/methods that will be used also in stage2
var __BOND_STDIN = fs.openSync("/dev/stdin", "r");

function __BOND_getline()
{
  var line = "";
  var buf = new Buffer(1);
  while(fs.readSync(__BOND_STDIN, buf, 0, 1) > 0)
  {
    if(buf[0] == 10) break;
    line += buf;
  }
  return line.trimRight();
}


/// Actual loader
(function()
{
  console.log("stage2".toUpperCase());
  var line;
  while((line = __BOND_getline()).length == 0);
  var stage2 = JSON.parse(line);
  eval.call(null, stage2.code);
  __BOND_start.apply(null, stage2.start);
}).call(null);
