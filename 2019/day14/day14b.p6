#!/usr/bin/env perl6

use v6;

grammar Chemistry {
    rule TOP { <input>+ % ',' \=\> <output> }
    rule input { <nchemical> }
    rule output { <nchemical> }
    rule nchemical { (\d+) (<:Lu>+) }
}

class Chemistry-actions {
    method nchemical ($/) {
        make ($/[0].Int, $/[1].Str)
    }
    method TOP ($/) {
        make {
            inputs => $<input>.map({$_<nchemical>.made}),
            output => $<output><nchemical>.made
        }
    }
}

sub count(%rules, @needs) {
    my %spare;
    my $ore = 0;

    while (@needs) {
        my ($q, $mineral) = @needs.pop;
        if ($mineral eq "ORE") {
            $ore += $q;
            next;
        }
        my $spare = %spare{$mineral} || 0;
        if ($spare > $q) {
            %spare{$mineral} -= $q;
            next;
        } elsif ($spare > 0) {
            $q -= $spare;
            %spare{$mineral} = 0;
        }
        my $tmp = %rules{$mineral};
        my $out = $tmp[0];
        my @next-needs = $tmp[1];
        my $n = $q / $out;
        @needs.append: @next-needs.map({
            my ($x, $name) = $_;
            ($x*$n, $name)
        });
    }
    $ore
}

if ($*IN.t) {
    say "this thing expects things to be piped into it"
} else {
    my %rules;
    for lines() -> $line {
        my $parsed = Chemistry.parse($line, actions => Chemistry-actions.new).made;
        my (@in) = $parsed<inputs>;
        my $out = $parsed<output>;
        %rules{$out[1]} = ($out[0], @in);
    }
    #say %rules;
    my @needs = %rules<FUEL>[1];
    my $fuel = (1000000000000 / count(%rules, @needs)).floor;

    say $fuel;
}
