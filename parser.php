<?php

ini_set('display_errors', 'stderr');

$xml_output = "";

// Attaches given string to an output xml file that will be printed at the end of the program
function attach_to_output($current, $to_attach)
{
    $current = $current . $to_attach . "\n";
    return $current;
}

// Prints the instruction how to use the program correctly if the --help is used
if ($argc > 1) {
    if ($argv[2] == "--help")
        echo ("Usage: parser.php "); //TODO
    exit(0);
}

$xml_output = attach_to_output($xml_output, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
$xml_output = attach_to_output($xml_output, "<program language = \"IPPcode23\">");

// Erases the comments from the given line
function erase_comments($line)
{
    preg_replace("/#.*/",'',$line);
}
function is_variable($name)
{
    if (preg_match("/(LF | TF | GF)@([_\-$#%*!?A-Za-z]([A-Za-z0-9_\-$#%*!?]))* /", $name)) {
        return 0;
    } else {
        return 23;
    }
}

function is_label($name)
{
    if (preg_match("/([_\-$#%*!?A-Za-z]([A-Za-z0-9_\-$#%*!?]))* /", $name)) {
        return 0;
    } else {
        return 23;
    }
}

function is_symbol($name)
{
    if (preg_match("/(LF | TF | GF)@([_\-$#%*!?A-Za-z]([A-Za-z0-9_\-$#%*!?])*) /", $name)) 
    {
        return 0;
    } 
    if(preg_match("/(bool)@(true | false) */", $name))
    {
        return 0;
    }
    if(preg_match("/(int)@ [+-]?[0-9]* /", $name))
    {
        return 0;
    }
    if(preg_match("/nil@nil/", $name))
    {
        return 0;
    }
    //TODO finish string 
    if(preg_match("/string@[s] /", $name))
    {
        return 0;
    }

    return 23;
}

function is_type($name)
{
    switch ($name) {
        case 'int':
        case 'bool':
        case 'string':
            return 0;
        default:
            return 23;
    }
}

/*function instruction($num, $arguments, $name)
{
    echo ("<instruction order=\"$num\" opcode\"$name\">\n");
    //TODO arguments
    echo ("<//instruction>");
}*/
$header = false;
$line;
$instrctnum = 0;
while ($line = fgets(STDIN)) {
    if(!$header)
    {
        $line = strtoupper($line);
        if($line == ".IPPCODE23")
        {
            $header = true;
        }
        else
        {
            exit(21);
        }
    }
    $instrctnum++;
    $token = explode('', trim($line, '\n'));
    switch (strtoupper($tokens[0])) {
        // <var> <symb>
        case 'MOVE':
        case 'INT2CHAR':
        case 'STRLEN':
        case 'TYPE':
            if (!is_variable($line[1])) {
                //todo
            } else {
                exit(23);
            }
            break;

        // <var>
        case 'DEFVAR':
        case 'POPS':
            if (is_variable($line[1])) {
                //TODO
            } else {
                exit(23);
            }
            break;
        // <label>
        case 'CALL':
        case 'LABEL':

        case 'JUMP':
            break;

        // <var> <symb1> <symb2>
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
        case 'STRI2INT':
            break;

        // <var> <type>
        case 'READ':
            break;

        // <var> <symb2> <symb2> 
        case 'CONCAT':
            break;
        case 'GETCHAR':
            break;
        case 'SETCHAR':
            break;

        // <label> <symb1> <symb2>
        case 'JUMPIFEQ':
            break;
        case 'JUMPIFNEQ':
            break;

        // <symb>
        case 'EXIT':
        case 'WRITE':
        case 'DPRINT':
        case 'PUSHS':
            break;

    }
}

?>