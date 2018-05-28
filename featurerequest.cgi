#!/usr/bin/perl

local ($buffer, @pairs, $pair, $name, $value, %FORM);
# Read in text
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;

if ($ENV{'REQUEST_METHOD'} eq "POST") {
   read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
} else {
   $buffer = $ENV{'QUERY_STRING'};
}

# Split information into name/value pairs
@pairs = split(/&/, $buffer);
print "Content-type:text/html\r\n\r\n";
print "<html>";
print "<head>";
print "<title>Request confirmation</title>";
print "</head>";
print "<body>";
print "<h1>The following features have been requested</h1>";
print "<table style='width:100%'>";
print "<tr><th>Title</th><th>Description</th><th>Client</th><th>Priority</th><th>Product Area</th><th>Target Date</th></tr>";
print "<tr>";
$loopcount=0;
$numColums = 6;
$BigSQL = "";
$LittleSQL = "<br/><br/>INSERT INTO `FeatureRequest` (`Title`, `Description`, `Client`, `Priority`,  `ProductArea`, `Target Date`,`SubmissionDate`) VALUES (";
foreach $pair (@pairs) {
   if($loopcount % $numColums != 0)
   {
      $LittleSQL .= ',';
   }
   ($name, $value) = split(/=/, $pair);
   $value =~ tr/+/ /;
   $value =~ s/%(..)/pack("C", hex($1))/eg;
   if($loopcount % $numColums == $numColums-1)
   {
      if($value eq "")
      {
         $value = "08/07/2018";
      }
   }
   $FORM{$name} = $value;
   print "<td>$value</td>";
   $loopcount++;
   $LittleSQL = $LittleSQL . "'" . $value . "'";
   if($loopcount % $numColums == 0)
   {
      print "</tr><tr>";
      $LittleSQL .= ")";
      $BigSQL .= $LittleSQL . "<br/><br/>";
      $LittleSQL = "INSERT INTO `FeatureRequest` (`Title`, `Description`, `Client`, `Priority`,  `ProductArea`, `Target Date`,`SubmissionDate`) VALUES (";
   }
}
print "</tr>";
print "</table>";
print $BigSQL;
#$reqtitle = $FORM{reqtitle};
#$description = $FORM{description};
#$client = $FORM{client};
#$priority = $FORM{priority};

print "</body>";
print "</html>";

1;