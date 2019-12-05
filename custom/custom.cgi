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
$maxcnt=10 if (!$maxcnt);


$address=param("address");
$station=param("station");






my $user= $db{$dbname}{'user'};
my $pw= &kdec($db{$dbname}{'passwd'});

#binmode(STDOUT,":utf8");
print header(-charset=>'utf8');
print<<EOP;
<html>
<head>
<style>
table{
width : 500px;
border: 1px solid lightgray; 
background-color:#A6BFE7;
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
<font size="5px"><b>맞춤노선</b><br>환승노선</font><br><br>
<hr>



EOP

$address=decode_utf8($address);
$station=decode_utf8($station);

#print ("<br>출발 정류장 : $station<br>");


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
my $sql= "SELECT DISTINCT trans_ID1 AS '출발대중교통명', stop_ID1 AS '출발 정류장', trans_ID2 AS '환승대중교통명', stop_ID2 AS '환승 정류장' FROM qBus2KNU22b WHERE ((qBus2KNU22b.stop_ID1='$station') and (stop_ID1<>stop_ID2));";


&printTables($dbh,$sql, $table,$tname,$maxcnt);

print "<a href='custom.htm'><input type='button' value='Back to Search' class='button1'></button></a>";

$dbh -> disconnect();


#----------------------------------------------------------------
# modified from Programming the Perl DBI
#  - http://www.unix.org.ua/orelly/linux/dbi/ch06_01.htm
#----------------------------------------------------------------
sub printTables {
    my ($dbh,$sql,$table,$tname,$maxn)=@_;

    my $sth1= $dbh->prepare($sql);
    $sth1->execute();

 
	
$i=0;
	  while (my @rows1 = $sth1->fetchrow_array()) {

        my $row1= join("<td>",@rows1);
			++$i;
		
		if($row1==''&&$i==0){
	
		my $rcnt1=0;
		last;
		}
	
		$row1=~s/ +/ /g;
      last if (++$rcnt1>$maxn);
    }
	

	
    my $sth= $dbh->prepare($sql);
    $sth->execute();
   my $ap= $sth->{NAME};
	if($i==0)
	{print("<font color='red'> 해당 정류장의 환승 노선이 존재하지 않습니다</font>.<p>")}
	else{
{	
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
}
    ### Explicitly deallocate the statement resources
    ### because we didn't fetch all the data
    $sth->finish();
    }
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
