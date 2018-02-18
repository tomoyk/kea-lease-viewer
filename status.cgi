#! /usr/bin/perl

# no-data on table

use warnings;
use DBI;
use strict;

##
# Escape XSS
##

sub h {

  # Receive html
  my $html = $_[0];

  if( length($html) <= 0 ) {
    return;
  }

  ##
  # Replace symbols
  ##
  
  my %symbols = (
    "&" => "&amp;",
    "<" => "&lt;",
    ">" => "&gt;",
    "\"" => "&quot;",
    "\'" => "&#39;"
  );

  while( my ($key, $val) = each(%symbols) ) {
    $html =~ s/$key/$val/g;
  }

  return $html;

}

##
# Build Web Page
##

print << "EOF";
Content-type: text/html\n
<html>
<head>
  <meta charset="utf-8">
  <title>DHCP Release Viewer</title>
  <link rel="stylesheet" href="normalize.css">
  <link rel="stylesheet" href="HTML-KickStart-master/css/kickstart.css">
  <link rel="stylesheet" href="style.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
  <script src="HTML-KickStart-master/js/kickstart.js"></script>
</head>
<body>
  <div id="container">
    <aside id="sidebar">
      <ul class="navi">
        <li class="current"><a href="#">IPv4 Lease</a></li>
        <li><a href="#">IPv6 Lease</a></li>
        <li><a href="#">About</a></li>
      </ul>
    </aside><!-- #sidebar -->
    <main id="content">
      <div class="container">
        <h3>IPv4 Lease</h3>
        <form action="status.cgi" method="get">
          <label for="select1">Select Field</label>
          <select id="select1" name="type">
            <option>MAC Address</option>
            <option>IP Address</option>
            <option>FQDN Reverse</option>
            <option>Subnet ID</option>
            <option>FQDN Forward</option>
            <option>Valid Lifetime</option>
            <option>Hostname</option>
            <option>State</option>
            <option>Client ID</option>
            <option>Lease Limit</option>
          </select>
          <input type="text" id="text2" name="text" placeholder="sss Text" />
          <button class="blue">Search</button>
        </form>
        <br>
EOF

##
# Connect to DB
##

my $db = "dhcpdb";
my $dst = "127.0.0.1";
my $user = "kea";
my $password = "PassWord";

my $dbh = DBI->connect("DBI:mysql:$db:$dst", $user, $password, {
  RaiseError => 1,
  AutoCommit => 1
}) or die "cannot connect to Database: $DBI::errstr";

##
# Send query for DB
##

my $sth = $dbh->prepare("SELECT inet_ntoa(address), hex(hwaddr), hex(client_id), valid_lifetime, expire, subnet_id, fqdn_fwd, fqdn_rev, hostname, state FROM lease4");

$sth->execute;

##
# Print Info List
##

if( $sth->rows > 0) {

  # Define columnName and tableLabel
  my %table_info = (
    "inet_ntoa(address)" => "IP Address",
    "hex(hwaddr)" => "MAC Address",
    "hex(client_id)" => "Client ID",
    "valid_lifetime" => "Valid Lifetime",
    "expire" => "Lease Limit",
    "subnet_id" => "Subnet ID",
    "fqdn_fwd" => "FQDN Forward",
    "fqdn_rev" => "FQDN Reverse",
    "hostname" => "Hostname",
    "state" => "State",
  );

  ##
  # Print Label on table
  ##

  print "<table id=\"release\" class=\"sortable\"><thead>\n";
  print "<tr>\n";

  foreach my $key(keys %table_info) {
    print "<th>".h($table_info{$key})."</th>\n";
  }

  print "</tr>\n";
  print "</thead><tbody>\n";

  ##
  # Print Info on machines
  ##

  while (my $ref = $sth->fetchrow_hashref) {

    print "<tr>\n";

    foreach my $key(keys %table_info) {
      print "<td>".h($ref->{$key})."</td>\n";
    }

    print "</tr>\n";

  }

  # Build Web Page
  print "</tbody></table>\n"

} else {

  print 'No such data on table.'; 

}

##
# Close connection
##

$sth->finish;
$dbh->disconnect;

##
# Build Web Page
##

print << "EOF";
      </div><!-- .container -->
    </main><!-- #content -->
  </div><!-- #container -->
</body>
</html>
EOF
