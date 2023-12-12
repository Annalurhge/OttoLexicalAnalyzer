from tokens import *

class OttoLexicalAnalyzer():
    def __init__(self, file):
        self.output = []
        
        if self._check_file_extension(file):
            read_file = self._tokenize(file)
    
    class ValidToken():
            def __init__(self, lexeme, token, trail_space):
                self.lexeme = lexeme
                self.token = token
                self.trail_space_count = trail_space
            
            def __str__(self):
                return f"{self.lexeme} \t: \t{self.token}"
            
    def _check_file_extension(self, file):
        if file.lower().endswith(".otto"):
            return True
        return False

    def _identify_chars(self, token_list):
        for item in token_list:
            for token in item:
                if token.isalpha():
                    self.output.append(self.ValidToken(token, "IDENTIFIER", 0))
                    continue
                
                if token in "+-*/=!":
                    self.output.append(self.ValidToken(token, "OPERATOR", 0))
                    continue
                    
                if token.isnumeric():
                    self.output.append(self.ValidToken(token, "NUM_LIT", 0))
                    continue
                
                if token.endswith("'") or token.endswith('"') and len(token) > 1:
                    self.output.append(self.ValidToken(token, "STRING_LIT", 0))
                    continue
                
                if token.isspace():
                    self.output.append(self.ValidToken(token, "WHITESPACE", 0))
                    
                if token == "\n":
                    self.output.append(self.ValidToken(token, "NEWLINE", 0))
                
                self.output.append(self.ValidToken(token, "UNKNOWN", 0))

    def _check_type(self, char):
        if char in ARITH_OPS:
            return "ARITH_OPS"
        
        if char in STRING:
            return "STRING_LIT"
        
        if char in ASS_OPS:
            return "ASS_OPS"
        
        if char.isalpha():
            return "ALPHA"
        
        if char.isnumeric():
            return "NUM_LIT"
        
        if char.isspace():
            return "WHITE_SPACE"

    def _get_chars(self, char_list):
        to_return = []
        prev_char = ""
        empty_string = ""
        closing_quote = ""
        quote_count = 0
        
        for line in char_list:
            for char in line:
                if char in STRING:
                    closing_quote = char
                    if closing_quote == char:
                        quote_count += 1
                    
                if prev_char == "":
                    prev_char += char
                    
                if quote_count % 2 == 1 and prev_char != "=":
                    empty_string += char
                elif quote_count % 2 == 0 and closing_quote != "":
                    empty_string += char
                    to_return.append([empty_string])
                    closing_quote = ""
                    empty_string = ""
                elif self._check_type(prev_char) == self._check_type(char):
                    prev_char = f"{char}"
                    empty_string += char
                else:
                    to_return.append([empty_string])
                    prev_char = f"{char}"
                    empty_string = f"{char}"
                
            if empty_string != "":
                to_return.append([empty_string])
            print(char)
        
        return to_return
        
    def _tokenize(self, file):
        with open(file, "r") as otto_file:
            char_list = [[char for char in word if char] for word in otto_file.readlines()]
        self._identify_chars(self._get_chars(char_list))
        
        for token in self.output:
            print(token)

OttoLexicalAnalyzer(r'chicken.otto')