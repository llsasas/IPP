<?php

ini_set('display_errors', 'stderr');
echo("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
if($argc > 1)
{
    if($argv[2] == "--help")
        echo("Usage: parser.php "); //TODO
        exit(1);
    
}

$header = false;
if(fgets(STDIN) == ".IPPcode23")
{
$header = true;
}
else
{
    exit(21);
}

$line;

while ($line = fgets(STDIN))
{
    $token = explode('', trim($line, '\n'));
    switch(strtoupper($tokens[0]))
    {
        case 'MOVE':
            break;
        case 'CREATEFRAME':
            break;
        case 'PUSHFRAME':
            break;
        case 'POPFRAME':
            break;
        case 'DEFVAR':
            break;
        case 'CALL':
            break;
        case 'RETURN':
            break;
        case 'PUSHS':
            break;
        case 'POPS':
            break;
        case 'ADD':
            break;
        case 'SUB':
            break;
        case 'MUL':
            break;
        case 'IDIV':
            break;
        case 'LT':
            break;
        case 'GT':
            break;
        case 'EQ':
            break;
        case 'AND':
            break;
        case 'OR':
            break;
        case 'NOT':
            break;
        case 'INT2CHAR':
            break;
        case 'STRI2INT':
            break;
        case 'READ':
            break;
        case 'WRITE':
            break;
        case 'CONCAT':
            break;
        case 'STRLEN':
            break;
        case 'GETCHAR':
            break;
        case 'SETCHAR':
            break;
        case 'TYPE':
            break;
        case 'LABEL':
            break;
        case 'JUMP':
            break;
        case 'JUMPIFEQ':
            break;
        case 'JUMPIFNEQ':
            break;
        case 'EXIT':
            break;
    }
}

?>