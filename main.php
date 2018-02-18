<?php

require_once 'vendor/autoload.php';

$loader = new Twig_Loader_Filesystem('templates');
$twig = new Twig_Environment($loader, [
  'debug' => true, 
  'auto_reload' => true, 
  'strict_variables' => true
]);

echo $twig->render('_base.html', ['title' => 'IPv4 Lease']);

