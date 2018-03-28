<?php

require_once 'vendor/autoload.php';

// Initialize Twig
$loader = new Twig_Loader_Filesystem('templates');
$twig = new Twig_Environment($loader, [
  'debug' => true, 
  'auto_reload' => true, 
  // 'strict_variables' => true
]);

// Menu settings
$pages = [
  // Slug  => Label
  'v4'     => 'IPv4 Lease',
  'v6'     => 'IPv6 Lease',
  'about'  => 'About',
  'search' => 'Search'
];

if(isset($_GET['v4']) || isset($_GET['v6'])) {

  try{

    $db_user = 'kea';
    $db_pass = 'password';
    $dbh = new PDO('mysql:host=localhost;dbname=dhcpdb', $db_user, $db_pass);

  } catch( PDOException $e ) {

    echo "PDOException has occured.<br>\n";
    echo "Error:: ".$e->getMessage()."<br>\n";
    die();

  }
  
  $active = isset($_GET['v4']) ? 'v4' : 'v6';
  echo $twig->render('_ipTable.html', [
    'navLabels' => $pages,
    'enableItem' => $active
  ]);

} elseif(isset($_GET['about'])){

  echo $twig->render('about.html', [
    'navLabels' => $pages,
    'enableItem' => 'about'
  ]);

} else {

  // Redirect to v4 
  $currentURL = (empty($_SERVER["HTTPS"]) ? "http://" : "https://") . $_SERVER["HTTP_HOST"] . $_SERVER["SCRIPT_NAME"];
  header("Location: ${currentURL}?v4", true, 307);

}
