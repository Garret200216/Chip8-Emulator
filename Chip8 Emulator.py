import pygame, random, tkinter
from tkinter.filedialog import askopenfilename
    
class myChip8():
        def __init__(self, rom):
                self.opcode = [0x00000000, 0x00000000]
                self.memory = []
                self.V = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
                self.I = 0
                self.pc = 0x200
                self.gfx = dict()
                self.delay_timer = 255
                self.sound_timer = 0
                self.stack = []
                self.sp = 0
                self.keys = 100
                self.font = [
                        "0xF0", "0x90", "0x90", "0x90", "0xF0",  # 0
                        "0x20", "0x60", "0x20", "0x20", "0x70",  # 1
                        "0xF0", "0x10", "0xF0", "0x80", "0xF0",  # 2
                        "0xF0", "0x10", "0xF0", "0x10", "0xF0",  # 3
                        "0x90", "0x90", "0xF0", "0x10", "0x10",  # 4
                        "0xF0", "0x80", "0xF0", "0x10", "0xF0",  # 5
                        "0xF0", "0x80", "0xF0", "0x90", "0xF0",  # 6
                        "0xF0", "0x10", "0x20", "0x40", "0x40",  # 7
                        "0xF0", "0x90", "0xF0", "0x90", "0xF0",  # 8
                        "0xF0", "0x90", "0xF0", "0x10", "0xF0",  # 9
                        "0xF0", "0x90", "0xF0", "0x90", "0x90",  # A
                        "0xE0", "0x90", "0xE0", "0x90", "0xE0",  # B
                        "0xF0", "0x80", "0x80", "0x80", "0xF0",  # C
                        "0xE0", "0x90", "0x90", "0x90", "0xE0",  # D
                        "0xF0", "0x80", "0xF0", "0x80", "0xF0",  # E
                        "0xF0", "0x80", "0xF0", "0x80", "0x80"   # F
                ]
                
                
                for i in range(4096):
                        self.memory += [hex(0)]
                        
                j = 0
                for i in self.font:
                        self.memory[0x50+j] = i
                        j+=1 
                        
                with open(rom, 'rb') as file:
                        content = file.read() 
                        j = 0
                        for bit in content:
                                self.memory[0x200+j] = hex(bit)
                                j += 1
                        for i in range(len(self.memory)):
                                if len(self.memory[i]) < 4:
                                        self.memory[i] = f'{self.memory[i][0:2]}0{self.memory[i][2:]}'
                                self.memory[i] = self.memory[i][2:].upper()              
                                                       
                for i in range(64*32): 
                        self.gfx[(i-(i//64)*64,i//64)] = 0
                              
                
                #self.memory[0x1FF] = '0x01'      
                self.gfx[(0, 0)] = 2
                self.loop()
        
        def run_opcode(self, opcode):
                #print(opcode, self.keys)
                if opcode == '00E0':
                        for key in self.gfx.keys():
                                self.gfx[key] = 0
                                
                if opcode == '00EE':
                        self.pc = self.stack.pop()  

                if opcode[0] == '1':
                        self.pc = int(opcode[1:], 16)
                        
                if opcode[0] == '2':
                        self.stack.append(self.pc)
                        self.pc = int(opcode[1:], 16)
                        
                if opcode[0] == '3':
                        if self.V[opcode[1]] == int(opcode[2:], 16):
                                self.pc += 2
                                
                if opcode[0] == '4':
                        if self.V[opcode[1]] != int(opcode[2:], 16):
                                self.pc += 2
                                
                if opcode[0] == '5':
                        if self.V[opcode[1]] == self.V[opcode[2]]:
                                self.pc += 2
                                
                if opcode[0] == '9':
                        if self.V[opcode[1]] != self.V[opcode[2]]:
                                self.pc += 2                 
                                
                if opcode[0] == '6':
                        self.V[opcode[1]] = int(opcode[2:], 16)

                if opcode[0] == '7':
                        self.V[opcode[1]] += int(opcode[2:], 16)
                        if self.V[opcode[1]] > 255:
                                self.V[opcode[1]] -= 256

                        
                if opcode[0] == '8':
                        
                        if opcode[3] == '0':
                                self.V[opcode[1]] = self.V[opcode[2]]
                        elif opcode[3] == '1':
                                self.V[opcode[1]] = self.V[opcode[1]] | self.V[opcode[2]]
                        elif opcode[3] == '2':
                                self.V[opcode[1]] = self.V[opcode[1]] & self.V[opcode[2]]                        
                        elif opcode[3] == '3':
                                self.V[opcode[1]] = self.V[opcode[1]] ^ self.V[opcode[2]]
                        elif opcode[3] == '4':
                                self.V[opcode[1]] = self.V[opcode[1]] + self.V[opcode[2]]
                                if self.V[opcode[1]] > 255:
                                        self.V[opcode[1]] -= 256
                                        self.V['F'] = 1
                                else:
                                        self.V['F'] = 0
                        elif opcode[3] == '5':
                                self.V[opcode[1]] = self.V[opcode[1]] - self.V[opcode[2]]
                                if self.V[opcode[1]] < 0:
                                        self.V[opcode[1]] += 256
                                        self.V['F'] = 0
                                else:
                                        self.V['F'] = 1       
                        elif opcode[3] == '7':   
                                self.V[opcode[1]] = self.V[opcode[2]] - self.V[opcode[1]]
                                if self.V[opcode[1]] < 0:
                                        self.V[opcode[1]] += 256
                                        self.V['F'] = 0
                                else:
                                        self.V['F'] = 1 
                        elif opcode[3] == '6':
                                if bin(self.V[opcode[1]])[-1] == '1':
                                        self.V['F'] = 1
                                else:
                                        self.V['F'] = 0
                                self.V[opcode[1]] = self.V[opcode[1]] // 2
                                
                        elif opcode[3] == 'E':
                                if self.V[opcode[1]] >= 128:
                                        self.V['F'] = 1
                                else:
                                        self.V['F'] = 0
                                self.V[opcode[1]] = self.V[opcode[1]] * 2
                                while self.V[opcode[1]] > 255:
                                        self.V[opcode[1]] -= 256


                                
                if opcode[0] == 'A':
                        self.I = int(opcode[1:], 16)
                        
                if opcode[0] == 'B':
                        self.pc = int(opcode[1:], 16) + self.V['0']
                        
                if opcode[0] == 'C':
                        self.V[opcode[1]] = random.randint(0, 255) & int(opcode[2:], 16)     
                        
                if opcode[0] == 'D':
                        VX = self.V[opcode[1]]
                        VY = self.V[opcode[2]]
                        self.V['F'] = 0
                        
                        for y in range(int(opcode[3], 16)):
                                sprite = format(int(self.memory[self.I+y], 16), '08b')
                                for x in range(len(sprite)):
                                        if VX+x<64 and VY+y<32:
                                                if self.gfx[(VX+x, VY+y)] == 1 and sprite[x] == '1':
                                                        self.V['F'] = 1
                                                        self.gfx[(VX+x, VY+y)] = 0
                                                elif self.gfx[(VX+x, VY+y)] == 0 and sprite[x] == '1':
                                                        self.gfx[(VX+x, VY+y)] = 1
                
                if opcode[0] == 'E':
                        #print(opcode, self.V[opcode[1]], self.keys, self.delay_timer)
                        if opcode[2:] == '9E':
                                if self.keys == self.V[opcode[1]]:
                                        self.pc += 2
                        elif opcode[2:] == 'A1':
                                if self.keys != self.V[opcode[1]]:
                                        self.pc += 2
                                       
                if opcode[0]+opcode[2:] == 'F0A':
                        if self.keys == 100:
                                self.pc -= 2
                        else:
                                self.V[opcode[1]] = self.keys
                        


                                
                if opcode[0]+opcode[2:] == 'F07':
                        self.V[opcode[1]] = self.delay_timer
                
                if opcode[0]+opcode[2:] == 'F15':
                        self.delay_timer = self.V[opcode[1]]
                        
                if opcode[0]+opcode[2:] == 'F18':
                        self.sound_timer = self.V[opcode[1]]                  
                
                if opcode[0]+opcode[2:] == 'F1E':
                        self.I += self.V[opcode[1]]

                        
                if opcode[0]+opcode[2:] == 'F29':
                        self.I = 0x50+self.V[opcode[1]]*5                    
                
                if opcode[0]+opcode[2:] == 'F33':
                        j = 0
                        if len(str(self.V[opcode[1]])) < 3:
                                while len(str(self.V[opcode[1]])) + j < 3:
                                        self.memory[self.I+j] = hex(0)
                                        j += 1
                        for i in range(len(str(self.V[opcode[1]]))):
                                self.memory[self.I+i+j] = hex(int(str(self.V[opcode[1]])[i]))
                
                if opcode[0]+opcode[2:] == 'F55':
                        for i in range(int(opcode[1], 16)+1):                              
                                self.memory[self.I+i] = hex(self.V[hex(i)[2].upper()])
                                                 
                if opcode[0]+opcode[2:] == 'F65':
                        for i in range(int(opcode[1], 16)+1):
                                self.V[hex(i)[2].upper()] = int(self.memory[self.I+i], 16)
                
                        
        def loop(self):
                fps = 720
                display_fps = 12
                clock = pygame.time.Clock()
                pygame.init()
                screen = pygame.display.set_mode(size=(64*30, 32*33), flags=0, depth=0, display=0, vsync=0)
                beep_sound = pygame.mixer.Sound('Beep.mp3')
                
                run = True
                while run:
                        opcode = self.memory[self.pc].replace('0x', '').upper() + self.memory[self.pc+1].replace('0x', '').upper()
                        self.pc += 2
                        events = pygame.event.get()
                        
                        keys = pygame.key.get_pressed()
                        self.get_key(keys)

                                                
                        self.run_opcode(opcode)
                        if self.sound_timer > 0:
                                beep_sound.play()
                                self.sound_timer -= 1                        
                        display_fps -= 1
                        if display_fps <= 0:
                                if self.delay_timer > 0:
                                        self.delay_timer -= 1

                                display_fps = 12
                                for key, value in self.gfx.items():
                                        if value == 1:
                                                pixel = pygame.Rect((key[0]*30, key[1]*33), (30, 33))
                                                pygame.draw.rect(screen, 'white', pixel)
                                        else:
                                                pixel = pygame.Rect((key[0]*30, key[1]*33), (30, 33))
                                                pygame.draw.rect(screen, 'black', pixel)                                                
                                pygame.display.flip()
                        for event in events:                
                                if event.type == pygame.QUIT:
                                        run = False                                        
                        clock.tick(fps)
                pygame.display.quit()
        
        
        def get_key(self, keys):
                if keys[pygame.K_1]:
                        self.keys = 1
                elif keys[pygame.K_2]:
                        self.keys = 2
                elif keys[pygame.K_3]:
                        self.keys = 3
                elif keys[pygame.K_q]:
                        self.keys = 4
                elif keys[pygame.K_w]:
                        self.keys = 5
                elif keys[pygame.K_e]:
                        self.keys = 6
                elif keys[pygame.K_a]:
                        self.keys = 7
                elif keys[pygame.K_s]:
                        self.keys = 8
                elif keys[pygame.K_d]:
                        self.keys = 9
                elif keys[pygame.K_x]:
                        self.keys = 0
                elif keys[pygame.K_z]:
                        self.keys = 10
                elif keys[pygame.K_c]:
                        self.keys = 11
                elif keys[pygame.K_4]:
                        self.keys = 12
                elif keys[pygame.K_r]:
                        self.keys = 13
                elif keys[pygame.K_f]:
                        self.keys = 14
                elif keys[pygame.K_v]:
                        self.keys = 15                        
                else:
                        self.keys = 100                
                
                
chip8 = myChip8(askopenfilename())
