from program import ProgramRunner
import random

class BrainfuckRunner(ProgramRunner):
    CHAR_LOOKUP = [']', '+', '-', '>', '<', '[', '.', ',']
    
    def __init__(self, tape_length, cell_bits=8, output_max_length=256, debug=False):
        self.tape_length = tape_length
        self.cell_bits = cell_bits
        self.output_max_length = output_max_length
        self.debug = debug
         
    def convert_program(self, prog_encoding):
        """Takes either a brainfuck program in string form and simply returns it as a list of 
        characters, or takes a whole number (int or long) and converts it into a brainfuck program. 
        """
        if isinstance(prog_encoding, basestring):
            return [instruct for instruct in prog_encoding if instruct in BrainfuckRunner.CHAR_LOOKUP]
        elif isinstance(prog_encoding, (int, long)):
            octal_str = format(prog_encoding, 'o')
            result = []
            
            balance = 0
            for digit in octal_str:
                char_to_add = BrainfuckRunner.CHAR_LOOKUP[int(digit)]
                if char_to_add == ']' and balance <= 0:
                    return None
                
                if char_to_add == '[':
                    balance += 1
                elif char_to_add == ']':
                    balance -= 1
                    
                result.append(char_to_add)
            
            if balance != 0:
                return None
                
            return result
        else:
            raise ValueError("Program encoding has invalid type: "+str(prog_encoding))
            
    
    def run_program(self, prog, steps, problem_input):
        instance = _BrainfuckInstance(self.tape_length, self.cell_bits, prog, problem_input, self.output_max_length)
        for i in xrange(0, steps+1):
            if self.debug:
                print str(instance)
            still_running = instance.step()
            if not still_running:
                break
            
        return instance.get_output()
        
        
class _BrainfuckInstance:
    def __init__(self, tape_length, cell_bits, prog, input, output_max_length):
        self._cell_max_value = 2**(cell_bits - 1)
        self._cell_min_value = -self._cell_max_value + 1
        self._tape = [0]*tape_length
        self._ptr = 0
        
        self._instructions = prog
        self._instruction_ptr = 0
        
        self._input = input
        self._output = []
        self._output_max_length = output_max_length
        
        self._error = False
    
    
    def step(self):
        if self._error or self._instruction_ptr >= len(self._instructions):
            return False
        else:
            instruct = self._instructions[self._instruction_ptr]
            if instruct == '+':
                self._tape[self._ptr] += 1
                if self._tape[self._ptr] > self._cell_max_value:
                    self._tape[self._ptr] = self._cell_min_value
                self._instruction_ptr += 1
            elif instruct == '-':
                self._tape[self._ptr] -= 1
                if self._tape[self._ptr] < self._cell_min_value:
                    self._tape[self._ptr] = self._cell_max_value
                self._instruction_ptr += 1
            elif instruct == '>':
                self._ptr += 1
                if self._ptr >= len(self._tape):
                    self._ptr = 0
                self._instruction_ptr += 1
            elif instruct == '<':
                self._ptr -= 1
                if self._ptr < 0:
                    self._ptr = len(self._tape) - 1
                self._instruction_ptr += 1
            elif instruct == '[':
                if self._tape[self._ptr] == 0:
                    self._jump_to_matching_paren()
                self._instruction_ptr += 1
            elif instruct == ']':
                self._jump_to_matching_paren()
            elif instruct == '.':
                self._output.insert(0, self._tape[self._ptr])
                if len(self._output) == self._output_max_length:
                    return False
                self._instruction_ptr += 1
            elif instruct == ',':
                if len(self._input) > 0:
                    # assume that the input has value within cell bounds
                    self._tape[self._ptr] = self._input.pop()   
                else:
                    self._tape[self._ptr] = 0
                self._instruction_ptr += 1
            
            return True
            
    def __repr__(self):
        res = '['
        for i in range(0, len(self._tape)):
            val_str = str(self._tape[i])
            if i == self._ptr:
                res += '*' + val_str + '*'
            else:
                res += val_str
            if i < len(self._tape)-1:
                res += ',\t'
            
        return res + ']'
                    
        
    def _jump_to_matching_paren(self):
        start_inst = self._instructions[self._instruction_ptr]
        if start_inst == '[':
            direction = 1
            balance = 1
        elif start_inst == ']':
            direction = -1
            balance = -1
        
        while balance != 0:
            self._instruction_ptr += direction
            if self._instruction_ptr < 0 or self._instruction_ptr >= len(self._instructions):
                self._error = True
                return
            instruct = self._instructions[self._instruction_ptr]
            if instruct == '[':
                balance += 1
            elif instruct == ']':
                balance -= 1
            
            
    def get_output(self):
        if self._error:
            return None
        else:
            return self._output

            
def test(runner, prog_str, input, expected_output, steps=5000):
    print "Running %s" % prog_str
    print "input = %s" % input
    output = runner.run_program(prog_str, steps, input)
    if output == expected_output:
        print "success! output = %s" % output
    else:
        print "failure!"
        print "expected = %s" % expected_output
        print "actual = %s" % output
    print ""
            
if __name__ == '__main__':
    bf = BrainfuckRunner(15, cell_bits=8, output_max_length=255, debug=False)

    longnum = random.getrandbits(100)

    # prog = bf.convert_program(longnum)
    # if prog is not None:
        # print("".join(prog))
        # print(bf.run_program(prog, 100, [20, 5]))
    
    # prog = bf.convert_program(',[.,]')
    # print (bf.run_program(prog, 100, [20, 5, 3, 50]))
    
    multi_add = ',[>,]<<[>[-<+>]<<]>.'
    inputs = [
            [6],
            [6, 40, 23],
            [6, 24],
            [6, 24, -13, 1, -25],
            [2, 5, -2, 4, 90, -110, 45, 2, 101, 25, -70]
        ]
    for array in inputs:
        test(bf, multi_add, array, [sum(array)], steps=6000)
    
    negate = ',[->-<]>.'
    test(bf, negate, [45], [-45], steps=1000)
    test(bf, negate, [-13], [13], steps=10000)
    
    
    # i = 203733
    # while True:
        # prog = bf.convert_program(i)
        # if prog is not None:
            # print "%s ==> %s" % (str(i).ljust(10), "".join(prog))
            # if "".join(prog) == ',>,.<.':
                # break
        # i += 1
        
    
        
    
    



        