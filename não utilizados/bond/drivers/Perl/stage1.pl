### bond Perl interface setup
### NOTE: use ### for comments only, as this code is transformed into a single
###       line to be injected into the interpreter *without parsing*.
use strict;
use warnings;
require IO::Handle;

### check external dependencies
require IO::String or die($@);
require Data::Dump or die($@);
require JSON or die($@);

sub
{
  STDOUT->autoflush();
  print(uc("stage2\n"));

  my $line = <STDIN>;
  my $stage2 = JSON::decode_json($line);

  eval $stage2->{code};
  __BOND_start(@{$stage2->{start}});
}->();
