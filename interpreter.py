import time,random

class Interpreter:
    def __init__(self,rom:bytes,screen) -> None:
        self.screen = screen

        self.registers = {i:0 for i in range(16)} # initializing all 16 registers with 0
        self.pc = 0x200 # initializing the program counter
        self.sp = [] # initializing the stack counter
        self.I = 0 # initializing the instruction register
        self.dt = 0
        self.st = 0

        self.dtTimeBegin = None
        self.stTimeBegin = None


        self.memory = [0] * 4096
        
        FONTSET_START_ADDRESS = 0x50
        fontset = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
    0xF0, 0x80, 0xF0, 0x80, 0x80   # F
]

        for i, byte in enumerate(fontset):
            self.memory[FONTSET_START_ADDRESS + i] = byte
        
        for i, byte in enumerate(rom):
            self.memory[0x200 + i] = byte

    def check_dt(self):
        if self.dt>0:
            if time.time() - self.dtTimeBegin >= (1/60):
                self.dt -=1

    def check_st(self):
        if self.st>0:
            if time.time() - self.stTimeBegin >= (1/60):
                self.st -=1


    def step(self):
        '''Runs the next step of the code'''

        if not self.screen.mainloop():
            return False
       

        current_byte = self.memory[self.pc]
        self.pc += 1  
        next_byte = self.memory[self.pc]
        self.pc +=1

     
        
        print("CURRENT OPCODE IS",hex(current_byte),hex(next_byte))

  
        match (current_byte & 0xF0) >> 4:
            # matching for 6xkk -> set register 'x' the value of 'kk'
            case 0x6:
                self.registers[current_byte & 0x0F] = next_byte
            
            # matchin for akkk -> set register 'I' the value of 'kkk'(12 bytes)
            case 0xa:
                self.I = ((current_byte & 0x0F) << 8) + next_byte
            
            # matching for dxyn -> displaying a sprie
            case 0xd:
                x = current_byte & 0x0F
                y = (next_byte & 0xF0) >> 4
                n = (next_byte & 0x0F)
                # print(hex(self.regis[x]),hex(self.memory[y]))
               
                sprites_ = [self.memory[i] for i in range(self.I, self.I+n)]
                
                if self.screen.draw_sprite(sprites_,self.registers[x],self.registers[y]):
                    self.registers[15] = 0x1
                else:
                    self.registers[15] = 0x0
            
            # matching for 2nnn -> jumps to the address 2nnn
            case 0x2:
                self.sp.append(self.pc)
                self.pc = ((current_byte & 0x0F) << 8) + next_byte
            
            # matching for differenct cases of Fx
            case 0xf:
                # matching for fx33
                if next_byte == 0x33:
                    value = self.registers[current_byte & 0x0F]

                    self.memory[self.I] = value //100
                    self.memory[self.I+1] = (value //10) %10
                    self.memory[self.I+2] = value % 10
                
                # matching for fx29 -> put I = sprite for number stored at register x 
                elif next_byte == 0x29:
                    self.I = 0x50 + self.registers[current_byte & 0x0F] * 5
                
                elif next_byte == 0x1E:
                    self.I = self.I + self.registers[current_byte & 0x0F]
                 
                
                # matching for fx65 -> fills  the values of register V0 through Vx from I 
                elif next_byte == 0x65:
                    for i in range((current_byte & 0x0F)+1):
                        self.registers[i] = self.memory[self.I+i]
                
                # matching for fx55 -> fills  the values of register V0 through Vx from I 
                elif next_byte == 0x55:
                    for i in range((current_byte & 0x0F)+1):
                       self.memory[self.I+i] =  self.registers[i] 
                # matching for fx15 -> sets the dt to the value of vx
                elif next_byte == 0x15:
                    self.dt = self.registers[current_byte & 0x0F]
                    self.dtTimeBegin = time.time()
                
                # matching for fx18 -> sets the st to the value of vx
                elif next_byte == 0x18:
                    self.st = self.registers[current_byte & 0x0F]
                    self.stTimeBegin = time.time()
                
                elif next_byte == 0x0A:
                    self.registers[current_byte & 0x0F] = self.screen.wait_key_press()

                # matching for fx07 -> sets the vx to the value of dt
                elif next_byte == 0x07:
                    self.registers[current_byte & 0x0F] = self.dt
                    


                
                else:
                     raise NotImplementedError("NOT IMPLEMENTED")

            # matching for 7xkk -> ADD Vx, byte 
            case 0x7:
                     x = current_byte & 0x0F
                     self.registers[x] = (self.registers[x] + next_byte) & 0xFF
            
            # matching for 00PP ->
            case 0x0:
                # matching for 00EE -> Return from the subroutine
                if next_byte ==  0xEE:
                    self.pc = self.sp[-1]
                    self.sp.pop() 
                elif next_byte == 0xE0:
                    self.screen.clear_display()
                else:
                     raise NotImplementedError("NOT IMPLEMENTED")

            # matching for 3xkk -> Skip next instruction if Vx = kk
            case 0x3:
                if self.registers[current_byte & 0x0F] == next_byte:
                    self.pc +=2   
            
            # matching for 1nnn -> jump to location nnn
            case 0x1:
                self.pc = ((current_byte & 0x0F) << 8) + next_byte

            # matching for cxkk -> Set Vx = random byte AND kk.
            case 0xc:
                self.registers[current_byte & 0x0F] = random.randint(0,255) & next_byte

            # matching for eppp              
            case 0xe:
                # checks the keyboard and if the key stored in Vx is not pressed skips two instruction
                if next_byte == 0xa1:
                    if  not self.screen.checkKeyPress(self.registers[current_byte & 0x0F]):
                        self.pc += 2 
                
                elif  next_byte == 0x9e:
                    if  self.screen.checkKeyPress(self.registers[current_byte & 0x0F]):
                        self.pc += 2

                else:
                     raise NotImplementedError("NOT IMPLEMENTED")


            case 0x9:
                if self.registers[current_byte & 0x0F] != self.registers[(next_byte & 0xF0) >> 4]:
                    self.pc+=2
            # matchinf for 8ppp

            case 0x8:
                x = current_byte & 0x0F
                y = (next_byte & 0xF0) >> 4
                n = (next_byte & 0x0F)

                # 8xy2 -> Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx
                if n==2:
                    self.registers[x] = self.registers[x] & self.registers[y]
                
                # 8xy3 -> Set Vx = Vx XOR Vy
                elif n==3:
                    self.registers[x] = self.registers[x] ^ self.registers[y]
                
                # 8xye -> Set Vx = Set Vx = Vx SHL 1
                elif n==0xe:
                    x
                    self.registers[0xF] = (self.registers[x] & 0x80) >> 7  # MSB to VF
                    self.registers[x] = (self.registers[x] << 1) & 0xFF
                
                # 8xy0 -> sets  Vx= Vy
                elif n ==0:
                    self.registers[x] = self.registers[y]
                
                elif n ==1:
                    self.registers[x] = self.registers[x] | self.registers[y]
                
                # 8xy4 -> Set Vx = Vx + Vy, set VF = carry
                elif n == 4:
                    sum_val = self.registers[x] + self.registers[y]
                    self.registers[0xF] = 1 if sum_val > 0xFF else 0
                    self.registers[x] = sum_val & 0xFF
                
                # 8xy4 -> Set Vx = Vx - Vy, set VF = NOT Borrow
                elif n == 5:
                    self.registers[0xF] = 1 if self.registers[x] > self.registers[y] else 0
                    self.registers[x] = (self.registers[x] - self.registers[y]) & 0xFF
                elif n == 7:
                    self.registers[0xF] = 1 if self.registers[y] > self.registers[x] else 0
                    self.registers[x] = (self.registers[y] - self.registers[x]) & 0xFF




                else:
                     raise NotImplementedError("NOT IMPLEMENTED")
            
            #matching  for 4xkk -> Skip next instruction if Vx != kk.
            case 0x4:
                if self.registers[current_byte & 0x0F] != next_byte:
                    self.pc += 2
            
            case 0x5:
                    if (next_byte & 0x0F) == 0: 
                        if self.registers[current_byte & 0x0F] == self.registers[(next_byte & 0xF0) >> 4]:
                            self.pc += 2
                        else:
                             raise NotImplementedError("NOT IMPLEMENTED")





                
             

            case default:
                 raise NotImplementedError("NOT IMPLEMENTED")
             
        self.check_dt()
        self.check_st()
        print(self.registers,hex(self.I))
