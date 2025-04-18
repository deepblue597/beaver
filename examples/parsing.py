def parse_Factor() : 

    if lookahead() == id : 
        val = match('ID') 
        return IDNode(val) 
    
    elif lookahead() == 'INT' : 
        val = match('INT')  
        return INTNode(val)
    elif lookahead() == '(' : 
        match('(') 
        expr = parse_expression() 
        match(')') 
        return expr
    else :
        raise ParseError("Expected ID, INT, or '('")

def parse_Term() : 

    left = parse_Factor()
    while lookahead() == '*' or lookahead() == '/' : 
        
        if lookahead() == '*' : 
            match('*') 
            right = parse_Factor() 
            combined = MulNode(left, right)
        else : 
            match('/') 
            right = parse_Factor() 
            combined = DivNode(left, right)
        
        return combined 

    return left 

def parse_expression() : 

    left = parse_Term()
    while lookahead() == '+' or lookahead() == '-' : 
        
        if lookahead() == '+' : 
            match('+') 
            right = parse_Term() 
            combined = AddNode(left, right)
        else : 
            match('-') 
            right = parse_Term() 
            combined = SubNode(left, right)
        
        return combined 

    return left
    
    