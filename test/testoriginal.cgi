#!/usr/bin/perl -w

use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use URI::Escape;
use utf8;

require "db.hash";

$dbname=param("dbname");
$maxcnt=param("maxcnt");
$maxcnt=5 if (!$maxcnt);

my $user= $db{$dbname}{'user'};
my $pw= &kdec($db{$dbname}{'passwd'});

binmode(STDOUT,":utf8");
print header(-charset=>'utf8');
print start_html();
print h1("$dbname Database");


# connect to a database (dbh: DB handle)
my $dbh = DBI->connect("DBI:mysql:dbname=$dbname:localhost;", "$user", "$pw", {mysql_enable_utf8=>1}) || die "Can't connect to the database: $DBI::errstr\n";

# Get a list of tables
my @tables = $dbh->tables();

# list table names
foreach my $table(@tables) {
    next if ($table =~ /users/i);
    my $tname=$1 if ($table=~/$dbname`.`(.+?)`$/);
    &printTables($dbh,$table,$tname,$maxcnt);
}

$dbh -> disconnect();


#----------------------------------------------------------------
# modified from Programming the Perl DBI
#  - http://www.unix.org.ua/orelly/linux/dbi/ch06_01.htm
#----------------------------------------------------------------
sub printTables {
    my ($dbh,$table,$tname,$maxn)=@_;

    my $sql= "SELECT * FROM $table";
    my $sth= $dbh->prepare($sql);
    $sth->execute();

    my $ap= $sth->{NAME};

    print "<b>Table: $tname</b>\n";
    print "<table border=1><tr><th>\n";
    print join("<th>",@{$ap}),"\n";
    
    # Iterate through all the table rows
    my $rcnt=0;
    while ( my @rows = $sth->fetchrow_array() ) {
        my $row= join("<td>",@rows);
        $row=~s/ +/ /g;
        print "<tr><td>$row</tr>\n";
        last if (++$rcnt>$maxn);
    }
    print "</table><p>\n";

    ### Explicitly deallocate the statement resources
    ### because we didn't fetch all the data
    $sth->finish();
    
}

sub mkench {
    my($in,$out,$inp,$outp)=@_;

    my @a1= split(//,$in);
    my @a2= split(//,$out);
    for($i=0;$i<@a1;$i++) {
       my($c1,$c2)=($a1[$i],$a2[$i]);
       $inp->{$c1}=$c2;
       $outp->{$c2}=$c1;
       #print "$c1=$c2\n";
    }

}

sub kdec {
    my ($str,$hp)=@_;

    $kbll= '123456qwertasdfgzxcvb';
    $kblu= '!@#$%^QWERTASDFGZXCVB';
    $kbrl= '7890-=yuiop[]hjkl;\'nm,./';
    $kbru= '&*()_+YUIOP{}|HJKL:"NM<>?';
    $kbll2= 'bgt65rfvcde43wsxzaq21';
    $kblu2= 'BGT^%RFVCDE$#WSXZAQ@!';
    $kbrl2= 'nhy78ujm,ki90ol./;p-=[\']\\';
    $kbru2= 'NHY&*UJM<KI()OL>?:P_+{"}|';

    $kbc= $kbll.$kblu.$kbrl.$kbru;
    $kbc2= $kbru2.$kbrl2.$kblu2.$kbll2;

    my(%enc,%dec,@chs2);
    &mkench($kbc,$kbc2,\%enc,\%dec);

    my @chs=split(//,uri_unescape($str));
    for(my $i=0;$i<@chs;$i++) {
        $chs2[$i]=$dec{$chs[$i]};
    }

    my $str2=join("",@chs2);

    return $str2;

}
