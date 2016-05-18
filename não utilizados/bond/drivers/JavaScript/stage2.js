// bond Javascript interface setup
var util = require("util");

// Channels and buffers
var __BOND_BUFFERS = {
  "STDOUT": "",
  "STDERR": ""
};

var __BOND_CHANNELS = {
  "STDIN": __BOND_STDIN,
  "STDOUT": fs.openSync("/dev/stdout", "w"),
  "STDERR": fs.openSync("/dev/stderr", "w")
};


// Define our own i/o methods
function __BOND_sendline(line)
{
  if(line == null) line = "";
  var buf = new Buffer(line + "\n");
  fs.writeSync(__BOND_CHANNELS["STDOUT"], buf, 0, buf.length);
}


// Our minimal exception signature
function _BOND_SerializationException(message)
{
  this.message = message;
}

util.inherits(_BOND_SerializationException, TypeError);
_BOND_SerializationException.prototype.name = "_BOND_SerializationException";


// Serialization methods
function __BOND_typecheck(key, value)
{
  if(typeof value === 'function' && value.toJSON == null)
    throw new TypeError("cannot serialize " + Object.getPrototypeOf(value));
  return value;
}

function __BOND_dumps(data)
{
  var ret;
  try { ret = JSON.stringify(data, __BOND_typecheck); }
  catch(e) { throw new _BOND_SerializationException(e.toString()); }
  return ret;
}

function __BOND_loads(string)
{
  return JSON.parse(string);
}


// Recursive repl
var __BOND_TRANS_EXCEPT;

function __BOND_remote(name, args)
{
  var code = __BOND_dumps([name, args]);
  __BOND_sendline("CALL " + code);
  return __BOND_repl();
}

function __BOND_export(name)
{
  global[name] = function()
  {
    return __BOND_remote(name, Array.prototype.slice.call(arguments));
  };
}

function __BOND_repl()
{
  var SENTINEL = 1;
  var line;
  while((line = __BOND_getline()))
  {
    var spc = line.indexOf(" ");
    var cmd = line.substring(0, spc < 0? undefined: spc);
    var args = (spc > 0? __BOND_loads(line.substring(spc + 1)): []);

    var ret = null;
    var err = null;
    switch(cmd)
    {
    case "EVAL":
      try { ret = eval.call(null, "(" + args + ")"); }
      catch(e) { err = e; }
      break;

    case "EVAL_BLOCK":
      try { eval.call(null, args); }
      catch(e) { err = e; }
      break;

    case "EXPORT":
      __BOND_export(args);
      break;

    case "CALL":
      try
      {
	// NOTE: we add an extra set of parenthesis to allow anonymous
	//       functions to be parsed without an assignment
	var func = eval.call(null, "(" + args[0] + ")");
	ret = func.apply(null, args[1]);
      }
      catch(e)
      {
	err = e;
      }
      break;

    case "XCALL":
      try
      {
	var func = eval.call(null, "(" + args[0] + ")");
	var xargs = [];
	for(var i = 0; i != args[1].length; ++i)
	{
	  var el = args[1][i];
	  xargs.push(!el[0]? el[1]: eval.call(null, "(" + el[1] + ")"));
	}
	ret = func.apply(null, xargs);
      }
      catch(e)
      {
	err = e;
      }
      break;

    case "RETURN":
      return args;

    case "EXCEPT":
      throw new Error(args);

    case "ERROR":
      throw new _BOND_SerializationException(args);

    default:
      process.exit(1);
    }

    // redirected channels
    for(var chan in __BOND_BUFFERS)
    {
      var buf = __BOND_BUFFERS[chan];
      if(buf.length)
      {
	var code = __BOND_dumps([chan, buf]);
	__BOND_sendline("OUTPUT " + code);
	__BOND_BUFFERS[chan] = "";
      }
    }

    // error state
    var state = "RETURN";
    if(err != null)
    {
      if(err instanceof _BOND_SerializationException)
      {
	state = "ERROR";
	ret = err.message;
      }
      else
      {
	state = "EXCEPT";
	ret = (__BOND_TRANS_EXCEPT? err: err.toString());
      }
    }
    var code;
    try
    {
      if(ret == null) ret = null;
      code = __BOND_dumps(ret);
    }
    catch(e)
    {
      state = "ERROR";
      code = __BOND_dumps(e.message);
    }
    __BOND_sendline(state + " " + code);
  }
  return 0;
}

function __BOND_start(proto, trans_except)
{
  // TODO: this is a hack
  process.stdout.write = function(buf) { __BOND_BUFFERS["STDOUT"] += buf; };
  process.stderr.write = function(buf) { __BOND_BUFFERS["STDERR"] += buf; };
  process.stdin.read = function() { return undefined; };

  __BOND_TRANS_EXCEPT = trans_except;
  __BOND_sendline("ready".toUpperCase());
  var ret = __BOND_repl();
  __BOND_sendline("BYE");
  process.exit(ret);
}
