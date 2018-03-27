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
$pages = ['IPv4 Lease', 'IPv6 Lease', 'About'];
$pages = [
  // Slug => Label
  'v4'     => 'IPv4 Lease',
  'v6'     => 'IPv6 Lease',
  'about'  => 'About'      
];

if(isset($_GET['v4']) || isset($_GET['v6'])) {

  $active = isset($_GET['v4']) ? 'v4' : 'v6';
  
  echo $twig->render('_ipTable.html', [
    'navLabels' => $pages,
    'enableItem' => $active
  ]);

} elseif(isset($_GET['about'])){

  echo $twig->render('_base.html', [
    'navLabels' => $pages,
    'enableItem' => 'about'
  ]);

}
