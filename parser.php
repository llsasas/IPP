<?php

ini_set('display_errors', 'stderr');
echo("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n");
echo("<program language = \"IPPcode23\">");
if($argc > 1)
{
    if($argv[2] == "--help")
        echo("Usage: parser.php "); //TODO
        exit(0);
    
}

$header = false;
if(fgets(STDIN) != ".IPPcode23")
{
    exit(21);
}
else
{

}

function is_variable($string)
{
    if(preg_match("/(LF || TF || GF)@([_\-$#%*!?A-Za-z]([A-Za-z0-9_\-$#%*!?]))* */",$string[1]))
    {
        return true;
    }
    else
    {
        return false;
    }
}

function is_symbol($string)
{
    $type = explode('@', $string);
    switch($type[0])
    {
        case 'int':
            if(is_numeric($type[1]))
            {
                //TODO
            }
            else
            {
                exit(23);
            }
            break;
        case 'string':
            if(ctype_print($type[1]))
            {
                foreach ($type as $char)
                {
                    for($i = 0; $i < strlen($char); $i++)
                    {
                        switch($char[$i])
                        {
                            case '':
                            case '#':
                            case '\\':
                            exit(23);
                        }
                        //TODO escape sequence
                    }
                }
            }
            else
            {
                exit(23);
            }
            break;
        case 'bool':
            if($type[1] == 'true' || $type[1] == 'false')
            {
                //TODO
            }
            else
            {
                exit(23);
            }
            break;
        case 'nil':
            if($type[1] == 'nil')
            {

            }
            else
            {
                exit(23);
            }
            break;
        default:
        exit(23); //TODO check whether the error code is correct
    }
}

function instruction($num,$arguments,$name)
{
    echo("<instruction order=\"$num\" opcode\"$name\">\n");
    //TODO arguments
    echo("<//instruction>");
}
$line;
$instrctnum = 0;
while ($line = fgets(STDIN))
{
    $instrctnum++;
    $token = explode('', trim($line, '\n'));
    switch(strtoupper($tokens[0]))
    {
        case 'MOVE':
            if(is_variable($line[1]))
            {
                //todo
            }
            else
            {
                exit(23);
            }
            break;
      /*  case 'CREATEFRAME':
            break;
        case 'PUSHFRAME':
            break;
        case 'POPFRAME':
            break;*/
        case 'DEFVAR':
            if(is_variable($line[1]))
            {
                //TODO
            }
            else
            {
                exit(23);
            }
            break;
     /*   case 'CALL':
            break;*/
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
        case 'DPRINT':
            break;
    }
}

?>