#!/usr/bin/perl -w

use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use URI::Escape;
use utf8;
use Encode;


require "../db.hash";

$dbname=param("dbname");
$maxcnt=param("maxcnt");
$maxcnt=1000 if (!$maxcnt);


$trans=param("trans");



my $user= $db{$dbname}{'user'};
my $pw= &kdec($db{$dbname}{'passwd'});

#binmode(STDOUT,":utf8");
print header(-charset=>'utf8');
print<<EOP;
<html>
<head>
<style>
table{
width:800px;
border: 1px solid lightgray; 
background-color:#F1E6E3;
}
td{
border: 1px solid lightgray;
text-align:center;
background-color:white;}


.button1 {
    background-color: white;
    color: #A3A3A7;
    border: 2px solid #B3B3B5;
    padding: 10px 23px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 12px;
    margin: 4px 2px;
    -webkit-transition-duration: 0.4s; /* Safari */
    transition-duration: 0.4s;
    cursor: pointer;
	font-weight:bold;
}

.button1:hover {background-color: #B3B3B5;
color:white;}


.css-arrow {
    display: inline-block;
    position: relative;
    margin: 0 0 0 8px;
    padding: 0;
    width: 0;
    height: 0;
    border: 10px solid transparent;
    border-left-color: #000;
}
.css-arrow:before, .css-arrow:after {
    display: block;
    content: "";
    position: absolute;
    top: 0;
    width: 0;
    height: 0;
}
.css-arrow:before {
    left: -30px;
    margin-top: -10px;
    border: 10px solid transparent;
    border-right-color: #000;
}
.css-arrow:after {
    left: -20px;
    margin-top: -14px;
    border: 14px solid transparent;
    border-left-color: white;
}

</style>
</head>
<body>
<center>

EOP

$address=decode_utf8($address);
$station=decode_utf8($station);





# connect to a database (dbh: DB handle)
my $dbh = DBI->connect("DBI:mysql:dbname=$dbname:localhost;", "$user", "$pw", {mysql_enable_utf8=>1}) || die "Can't connect to the database: $DBI::errstr\n";

# Get a list of tables
my @tables = $dbh->tables();

# list table names
#foreach my $table(@tables) {
#   next if ($table =~ /users/i);
#   print ("$table");
#   my $tname=$1 if ($table=~/$dbname`.`(.+?)`$/);
#   &printTables($dbh,$table,$tname,$maxcnt);
#}

$table='`Yangkids`.`TIMETABLE`';
my $tname=$1 if ($table=~/$dbname`.`(.+?)`$/);
&printTables($dbh,$table,$tname,$maxcnt);

print "<a href='select.htm'><input type='button' value='Back to Search' class='button1'></button></a>";

$dbh -> disconnect();


#----------------------------------------------------------------
# modified from Programming the Perl DBI
#  - http://www.unix.org.ua/orelly/linux/dbi/ch06_01.htm
#----------------------------------------------------------------
sub printTables {
    my ($dbh,$table,$tname,$maxn)=@_;

    my $sql= "SELECT REVIEW.* FROM REVIEW ORDER BY REVIEW.reviewDate DESC;";
    my $sth= $dbh->prepare($sql);
    $sth->execute();

    my $ap= $sth->{NAME};


    print "<table><tr><th>\n";
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
