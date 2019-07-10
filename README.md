## BNFParser
**Formal Methods in Software Engineering** course project, as taught at the **Faculty of Electrical Engineering Banja Luka**.

### Description
The task was to create a text parser that would parse the contents of the input file, as specified by the grammar in the modified [Backus-Naur form](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_Form). The grammar is given in a configuration file.

BNF is modified by adding the following nodes:

* `<a> ::= regex(regular_expression)` which represents any expression matched by *regular_expression*
* `<a> ::= standard_expression` where *standard_expression* can be any of the following:

expression | meaning 
---|---
phone_number|phone number with or without international and country call codes, with different delimiters
mail_address|properly formatted e-mail address
web_link|properly formatted absolute URL
number_constant|integer or floating-point constant
big_city|any of the big European cities (first 200)

If parsing is successful, the output of the parser should be an **XML file** representing the parse tree.
Otherwise, any error that occurs should be appropriately logged.

### Project structure
General project structure can be seen here:

![Project structure](https://github.com/ngrahovac/BNFParser/blob/master/docs/project_structure.png)



### Literature
The book that helped me the most is:
* [Dick Grune, Ceriel J. H. Jacobs - Parsing techniques - A Practical Guide - Monographs in Computer Science](https://www.amazon.com/Parsing-Techniques-Practical-Monographs-Computer/dp/1441919015)

You may also find these helpful:
* [Peter Linz - An Introduction to Formal Languages and Automata](https://www.amazon.com/Introduction-Formal-Languages-Automata/dp/1284077241)
* [Stanford CS143 Course Materials](https://web.stanford.edu/class/archive/cs/cs143/cs143.1128/)

