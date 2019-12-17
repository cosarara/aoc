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

if ($*IN.t) {
    say "this thing expects things to be piped into it"
} else {
    my %rules;
    for lines() -> $line {
        #say $line;
        my $parsed = Chemistry.parse($line, actions => Chemistry-actions.new).made;
        my (@in) = $parsed<inputs>;
        my $out = $parsed<output>;
        %rules{$out[1]} = ($out[0], @in);
    }
    say %rules;
    my @needs = %rules<FUEL>[1];
    #my @needs = $(5, "NZVS");
    say @needs;
    my %have;
    my %spare;

    my $ore = 0;

    #}
    #for @needs -> ($q, $mineral) {
    while (@needs) {
        my ($q, $mineral) = @needs.pop;
        if ($mineral eq "ORE") {
            $ore += $q;
            next;
        }
        say "needs $q, $mineral";
        my $spare = %spare{$mineral} || 0;
        say "spare $spare";
        if ($spare > $q) {
            %spare{$mineral} -= $q;
            %have{$mineral} += $q;
            next;
        } elsif ($spare > 0) {
            $q -= $spare;
            %spare{$mineral} = 0;
        }
        my $tmp = %rules{$mineral};
        my $out = $tmp[0];
        my @next-needs = $tmp[1];
        # THIS DOES'T WORK because @next-needs ends up as a one-element array
        # with the other array inside
        #my ($out, @next-needs) = %rules{$mineral};
        #say "next-needs: ", $pls;
        say "next-needs: ", @next-needs;
        #say "next-needs: ", %rules{$mineral};
        say "out $out";
        my $n = ($q / $out).ceiling; # amount of times rule applied
        my $made = $n * $out;
        my $new-spare = $made - $q;
        say "making $made $mineral out of $q needed: leaving $new-spare";
        %spare{$mineral} += $new-spare;
        @needs.append: @next-needs.map({
            my ($x, $name) = $_;
            ($x*$n, $name)
        });
        say "needs: ", @needs;
        say "\n";
    }
    say @needs;
    say %spare;
    say $ore;
}
