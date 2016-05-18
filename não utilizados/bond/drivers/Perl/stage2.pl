# bond Perl interface setup
use strict;
use warnings;
require IO::Handle;
require IO::String;
require Data::Dump;
require JSON;
require Scalar::Util;


# Channels and buffers
my %__BOND_BUFFERS =
(
  "STDOUT" => IO::String->new(),
  "STDERR" => IO::String->new()
);

my %__BOND_CHANNELS =
(
  "STDIN" => *STDIN,
  "STDOUT" => *STDOUT,
  "STDERR" => *STDERR
);


# Our minimal exception signature
{
  package _BOND_SerializationException;

  use overload '""' => sub { __PACKAGE__ . ': ' . ${shift()} . '\n' };

  sub new
  {
    my ($self, $message) = @_;
    return bless \$message, $self;
  }
}


# Serialization methods
my $__BOND_JSON = JSON->new()->allow_nonref();

sub __BOND_dumps
{
  my $data = shift;
  my $code = eval { $__BOND_JSON->encode($data) };
  die _BOND_SerializationException->new("cannot encode $data") if $@;
  return $code;
}

sub __BOND_loads
{
  return $__BOND_JSON->decode(@_);
}


# Define our own i/o methods
sub __BOND_getline()
{
  my $stdin = $__BOND_CHANNELS{STDIN};
  my $line = <$stdin>;
  chomp($line) if defined($line);
  return $line;
}

sub __BOND_sendline
{
  my $line = shift // "";
  my $stdout = $__BOND_CHANNELS{STDOUT};
  print $stdout "$line\n";
}


# Recursive repl
my $__BOND_TRANS_EXCEPT;

sub __BOND_remote($$)
{
  my ($name, $args) = @_;
  my $code = __BOND_dumps([$name, $args]);
  __BOND_sendline("CALL $code");
  return __BOND_repl();
}

sub __BOND_eval
{
  # we use a stub function to reset Perl and hide our local scope
  no strict;
  no warnings;
  eval shift;
}

sub __BOND_repl()
{
  my $SENTINEL = 1;
  while(my $line = __BOND_getline())
  {
    my ($cmd, $args) = split(/ /, $line, 2);
    $args = __BOND_loads($args) if defined($args);

    my $ret = undef;
    my $err = undef;
    if($cmd eq "EVAL")
    {
      # force evaluation in array context to avoid swallowing lists
      $ret = [__BOND_eval($args)];
      $err = $@;
      $ret = $ret->[0] if @$ret == 1;
    }
    elsif($cmd eq "EVAL_BLOCK")
    {
      # discard return, as with Perl it would most likely be a CODE ref
      __BOND_eval($args);
      $err = $@;
    }
    elsif($cmd eq "EXPORT")
    {
      my $code = "sub $args { __BOND_remote('$args', \\\@_) }";
      $ret = eval $code;
      $err = $@;
    }
    elsif($cmd eq "CALL")
    {
      # NOTE: note that we use "dump" to evaluate the command as a pure string.
      #       This allows us to execute *most* perl special forms consistenly.
      # TODO: special-case builtins to allow transparent invocation and higher
      #       performance with regular functions.
      my $name = $args->[0];
      my @args = @{$args->[1]};
      my $args_ = Data::Dump::dump(@args);
      $args_ = "($args_)" if @args == 1;
      $ret = [__BOND_eval("$name $args_")];
      $err = $@;
      $ret = $ret->[0] if @$ret == 1;
    }
    elsif($cmd eq "XCALL")
    {
      my $name = $args->[0];
      my @xargs;
      for my $el(@{$args->[1]})
      {
	my $val = (!$el->[0]? $el->[1]: __BOND_eval($el->[1]));
	push(@xargs, Data::Dump::dump($val));
      }
      my $xargs_ = join(",", @xargs);
      $ret = [__BOND_eval("$name ($xargs_)")];
      $err = $@;
      $ret = $ret->[0] if @$ret == 1;
    }
    elsif($cmd eq "RETURN")
    {
      return $args;
    }
    elsif($cmd eq "EXCEPT")
    {
      die $args;
    }
    elsif($cmd eq "ERROR")
    {
      die _BOND_SerializationException->new($args);
    }
    else
    {
      exit(1);
    }

    # redirected channels
    while(my ($channel, $buffer) = each %__BOND_BUFFERS)
    {
      if(tell($buffer))
      {
	my $output = ${$buffer->string_ref};
	my $code = __BOND_dumps([$channel, $output]);
	__BOND_sendline("OUTPUT $code");
	seek($buffer, 0, 0);
	truncate($buffer, 0);
      }
    }

    # error state
    my $state = "RETURN";
    if($err)
    {
      if(Scalar::Util::blessed($err) && $err->isa('_BOND_SerializationException'))
      {
	$state = "ERROR";
	$ret = $$err;
      }
      else
      {
	$state = "EXCEPT";
	$ret = ($__BOND_TRANS_EXCEPT? $err: "$err");
      }
    }
    my $code = eval { __BOND_dumps($ret) };
    if($@)
    {
      $state = "ERROR";
      $code = __BOND_dumps(${$@});
    }
    __BOND_sendline("$state $code");
  }
  return 0;
}

sub __BOND_start($$)
{
  my ($proto, $trans_except) = @_;

  *STDIN = IO::Handle->new();
  *STDOUT = $__BOND_BUFFERS{STDOUT};
  *STDERR = $__BOND_BUFFERS{STDERR};
  $SIG{__WARN__} = sub
  {
    print STDERR shift;
  };

  $__BOND_TRANS_EXCEPT = $trans_except;
  __BOND_sendline(uc("ready"));
  my $ret = __BOND_repl();
  __BOND_sendline("BYE");
  exit($ret);
}
