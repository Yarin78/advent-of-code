from goto import with_goto
from lib.intcode import *
from lib.intcode_decompile import *

class DecompiledProgram(DecompiledProgramBase):

    dir_counter = 0

    @with_goto
    def func0(self):
        #    0: IN (8)
        self.mem[8] = self.input()
        #    2: JMPT (8), #330
        if self.mem[8]:
            self.func330()
        #    5: JMPF #0, #11
        self.func11()
        return

    #    8: DB 0, 0, 0

    @with_goto
    def func11(self):
        #   11: OUT #1
        label .lbl_11
        self.output(1)
        #   13: OUT #0
        self.output(0)
        #   15: IN (8)
        label .lbl_15
        self.mem[8] = self.input()
        #   17: MUL #-1, (8), (10)
        label .lbl_17
        tmp = -1 * self.mem[8]
        #   21: ADD #1, (10), (10)
        tmp += 1
        #   25: OUT (10)
        self.output(tmp)
        #   27: EQ (8), #0, (10)
        tmp = 1 if self.mem[8] == self.mem[29] else 0
        #   31: OUT (10)
        self.output(tmp)
        #   33: MUL #1, (8), (29)
        self.mem[29] = self.mem[8]
        #   37: IN (8)
        self.mem[8] = self.input()
        #   39: MUL (8), #-1, (10)
        tmp = self.mem[8] * -1
        #   43: ADD (10), #1, (10)
        tmp += 1
        #   47: OUT (10)
        label .lbl_47
        self.output(tmp)
        #   49: EQ (8), #0, (10)
        label .lbl_49
        tmp = 1 if self.mem[8] == self.mem[51] else 0
        #   53: OUT (10)
        self.output(tmp)
        #   55: ADD #0, (8), (51)
        self.mem[51] = self.mem[8]
        #   59: ADD (1103), (2), (10)
        tmp = self.mem[1103] + self.mem[2]
        #   63: JMPF (0), #94
        if not self.mem[0]:
            pass # 1
        #   66: JMPF (0), #11
        if not self.mem[0]:
            goto .lbl_11
        #   69: ADD (1106), (13), (10)
        tmp = self.mem[1106] + self.mem[13]
        #   73: IN (8)
        self.mem[8] = self.input()
        #   75: MUL (8), #-1, (10)
        tmp = self.mem[8] * -1
        #   79: ADD #1, (10), (10)
        tmp += 1
        #   83: OUT (10)
        self.output(tmp)
        #   85: EQ (8), #1, (10)
        tmp = 1 if self.mem[8] == self.mem[87] else 0
        #   89: OUT (10)
        self.output(tmp)
        #   91: ADD (8), #0, (87)
        self.mem[87] = self.mem[8]
        #   95: IN (8)
        self.mem[8] = self.input()
        #   97: MUL #-1, (8), (10)
        tmp = -1 * self.mem[8]
        #  101: ADD #1, (10), (10)
        tmp += 1
        #  105: OUT (10)
        self.output(tmp)
        #  107: EQ (8), #0, (10)
        tmp = 1 if self.mem[8] == self.mem[109] else 0
        #  111: OUT (10)
        self.output(tmp)
        #  113: ADD (8), #0, (109)
        self.mem[109] = self.mem[8]
        #  117: MUL (1105), (5), (10)
        tmp = self.mem[1105] * self.mem[5]
        #  121: MUL (103), (16), (10)
        tmp = self.mem[103] * self.mem[16]
        #  125: ADD (1103), (12), (10)
        tmp = self.mem[1103] + self.mem[12]
        #  129: MUL (105), (2), (10)
        tmp = self.mem[105] * self.mem[2]
        #  133: IN (8)
        self.mem[8] = self.input()
        #  135: MUL #-1, (8), (10)
        tmp = -1 * self.mem[8]
        #  139: ADD (10), #1, (10)
        tmp += 1
        #  143: OUT (10)
        self.output(tmp)
        #  145: EQ #1, (8), (10)
        tmp = 1 if self.mem[146] == self.mem[8] else 0
        #  149: OUT (10)
        self.output(tmp)
        #  151: ADD (8), #0, (146)
        self.mem[146] = self.mem[8]
        #  155: JMPF (0), #49
        if not self.mem[0]:
            goto .lbl_49
        #  158: MUL (1), (12), (10)
        tmp = self.mem[1] * self.mem[12]
        #  162: MUL (1006), (6), (10)
        tmp = self.mem[1006] * self.mem[6]
        #  166: ADD (1101), (4), (10)
        tmp = self.mem[1101] + self.mem[4]
        #  170: IN (8)
        self.mem[8] = self.input()
        #  172: MUL (8), #-1, (10)
        tmp = self.mem[8] * -1
        #  176: ADD (10), #1, (10)
        tmp += 1
        #  180: OUT (10)
        self.output(tmp)
        #  182: EQ #0, (8), (10)
        tmp = 1 if self.mem[183] == self.mem[8] else 0
        #  186: OUT (10)
        self.output(tmp)
        #  188: ADD (8), #0, (183)
        self.mem[183] = self.mem[8]
        #  192: ADD (6), (9), (10)
        tmp = self.mem[6] + self.mem[9]
        #  196: JMPF (0), #32
        if not self.mem[0]:
            pass # 1
        #  199: IN (8)
        self.mem[8] = self.input()
        #  201: MUL #-1, (8), (10)
        tmp = -1 * self.mem[8]
        #  205: ADD (10), #1, (10)
        tmp += 1
        #  209: OUT (10)
        self.output(tmp)
        #  211: EQ (8), #1, (10)
        tmp = 1 if self.mem[8] == self.mem[213] else 0
        #  215: OUT (10)
        self.output(tmp)
        #  217: ADD #0, (8), (213)
        self.mem[213] = self.mem[8]
        #  221: MUL (1101), (9), (10)
        tmp = self.mem[1101] * self.mem[9]
        #  225: IN (8)
        self.mem[8] = self.input()
        #  227: MUL (8), #-1, (10)
        tmp = self.mem[8] * -1
        #  231: ADD (10), #1, (10)
        tmp += 1
        #  235: OUT (10)
        self.output(tmp)
        #  237: EQ (8), #1, (10)
        tmp = 1 if self.mem[8] == self.mem[239] else 0
        #  241: OUT (10)
        self.output(tmp)
        #  243: ADD #0, (8), (239)
        self.mem[239] = self.mem[8]
        #  247: JMPF (0), #47
        if not self.mem[0]:
            goto .lbl_47
        #  250: JMPF (0), #4
        if not self.mem[0]:
            pass # 1
        #  253: MUL (6), (0), (10)
        tmp = self.mem[6] * self.mem[0]
        #  257: JMPF (0), #58
        if not self.mem[0]:
            pass # 1
        #  260: IN (8)
        self.mem[8] = self.input()
        #  262: MUL (8), #-1, (10)
        tmp = self.mem[8] * -1
        #  266: ADD (10), #1, (10)
        tmp += 1
        #  270: OUT (10)
        self.output(tmp)
        #  272: EQ (8), #0, (10)
        tmp = 1 if self.mem[8] == self.mem[274] else 0
        #  276: OUT (10)
        self.output(tmp)
        #  278: MUL #1, (8), (274)
        self.mem[274] = self.mem[8]
        #  282: MUL (1005), (14), (10)
        tmp = self.mem[1005] * self.mem[14]
        #  286: JMPF (0), #17
        if not self.mem[0]:
            goto .lbl_17
        #  289: ADD (104), (20), (10)
        tmp = self.mem[104] + self.mem[20]
        #  293: JMPF (0), #28
        if not self.mem[0]:
            pass # 1
        #  296: IN (8)
        self.mem[8] = self.input()
        #  298: MUL #-1, (8), (10)
        tmp = -1 * self.mem[8]
        #  302: ADD (10), #1, (10)
        tmp += 1
        #  306: OUT (10)
        self.output(tmp)
        #  308: EQ #1, (8), (10)
        tmp = 1 if self.mem[309] == self.mem[8] else 0
        #  312: OUT (10)
        self.output(tmp)
        #  314: MUL (8), #1, (309)
        self.mem[309] = self.mem[8]
        #  318: ADD #1, (9), (9)
        self.mem[9] += 1
        #  322: LT (9), #928, (10)
        tmp = 1 if self.mem[9] < 928 else 0
        #  326: JMPT (10), #15
        if tmp:
            goto .lbl_15
        #  329: HALT
        raise MachineHaltedException()

    @with_goto
    def func330(self):
        #  330: ADD_BP #652
        #  332: OUT #0
        self.output(0)
        #  334: OUT #1
        self.output(1)
        #  336: ADD #0, #937263411860, (BP+1)
        q0 = 937263411860
        #  340: MUL #347, #1, (BP+0)
        #  344: JMPT #1, #451
        (q0) = self.func451(q0)
        #  347: ADD #932440724376, #0, (BP+1)
        q0 = 932440724376
        #  351: MUL #1, #358, (BP+0)
        #  355: JMPT #1, #451
        (q0) = self.func451(q0)
        #  358: IN (10)
        tmp = self.input()
        #  360: OUT #0
        self.output(0)
        #  362: OUT #1
        self.output(1)
        #  364: IN (10)
        tmp = self.input()
        #  366: OUT #0
        self.output(0)
        #  368: OUT #0
        self.output(0)
        #  370: IN (10)
        tmp = self.input()
        #  372: OUT #0
        self.output(0)
        #  374: OUT #1
        self.output(1)
        #  376: IN (10)
        tmp = self.input()
        #  378: OUT #0
        self.output(0)
        #  380: OUT #1
        self.output(1)
        #  382: IN (10)
        tmp = self.input()
        #  384: OUT #0
        self.output(0)
        #  386: OUT #0
        self.output(0)
        #  388: IN (10)
        tmp = self.input()
        #  390: OUT #0
        self.output(0)
        #  392: OUT #1
        self.output(1)
        #  394: ADD #0, #29015167015, (BP+1)
        q0 = 29015167015
        #  398: ADD #0, #405, (BP+0)
        #  402: JMPF #0, #451
        (q0) = self.func451(q0)
        #  405: MUL #1, #3422723163, (BP+1)
        q0 = 3422723163
        #  409: ADD #0, #416, (BP+0)
        #  413: JMPF #0, #451
        (q0) = self.func451(q0)
        #  416: IN (10)
        tmp = self.input()
        #  418: OUT #0
        self.output(0)
        #  420: OUT #0
        self.output(0)
        #  422: IN (10)
        tmp = self.input()
        #  424: OUT #0
        self.output(0)
        #  426: OUT #0
        self.output(0)
        #  428: ADD #0, #868389376360, (BP+1)
        q0 = 868389376360
        #  432: ADD #0, #439, (BP+0)
        #  436: JMPT #1, #451
        (q0) = self.func451(q0)
        #  439: MUL #825544712960, #1, (BP+1)
        q0 = 825544712960
        #  443: MUL #1, #450, (BP+0)
        #  447: JMPF #0, #451
        (q0) = self.func451(q0)
        #  450: HALT
        raise MachineHaltedException()

    @with_goto
    def func451(self, p0=0):
        #  451: ADD_BP #2
        #  453: ADD (BP+-1), #0, (BP+1)
        q0 = p0
        #  457: ADD #0, #40, (BP+2)
        q1 = 40
        #  461: MUL #482, #1, (BP+3)
        q2 = 482
        #  465: MUL #1, #472, (BP+0)
        #  469: JMPF #0, #515
        (q0, q1, q2) = self.func515(q0, q1, q2)
        #  472: ADD_BP #-2
        #  474: JMPF #0, (BP+0)
        pass # 0
        return (p0)

    #  477: DB 0, 1, 0, 0, 1

    @with_goto
    def func482(self, p0=0):
        #  482: ADD_BP #2
        #  484: IN (10)
        tmp = self.input()
        #  486: OUT (BP+-1)
        self.output(p0)
        #  488: ADD (477), #478, (493)
        self.mem[493] = self.dir_counter + 478
        #  492: OUT (0)
        self.output(self.mem[self.mem[493]])
        #  494: ADD (477), #1, (477)
        self.dir_counter += 1
        #  498: EQ #4, (477), (10)
        tmp = 1 if 4 == self.dir_counter else 0
        #  502: JMPF (10), #509
        if not tmp:
            goto .lbl_509
        #  505: ADD #0, #0, (477)
        self.dir_counter = 0
        #  509: ADD_BP #-2
        label .lbl_509
        #  511: JMPF #0, (BP+0)
        pass # 0
        return (p0)

    #  514: DB 0

    @with_goto
    def func515(self, p0=0, p1=0, p2=0):
        #  515: ADD_BP #4
        #  517: ADD #0, (BP+-1), (514)
        self.mem[514] = p2
        #  521: LT (BP+-3), #0, (10)
        tmp = 1 if p0 < 0 else 0
        #  525: JMPF (10), #532
        if not tmp:
            goto .lbl_532
        #  528: MUL #1, #0, (BP+-3)
        p0 = 0
        #  532: ADD #0, (BP+-3), (BP+1)
        label .lbl_532
        q0 = p0
        #  536: MUL #1, (BP+-2), (BP+2)
        q1 = p1
        #  540: MUL #1, #1, (BP+3)
        q2 = 1
        #  544: ADD #551, #0, (BP+0)
        #  548: JMPF #0, #556
        (q0, q1, q2, q3) = self.func556(q0, q1, q2)
        #  551: ADD_BP #-4
        #  553: JMPT #1, (BP+0)
        pass # 0
        return (p0, p1, p2)

    @with_goto
    def func556(self, p0=0, p1=0, p2=0, p3=0):
        #  556: ADD_BP #5
        #  558: LT (BP+-3), #1, (10)
        tmp = 1 if p1 < 1 else 0
        #  562: JMPF (10), #579
        if not tmp:
            goto .lbl_579
        #  565: LT (BP+-4), (BP+-2), (10)
        tmp = 1 if p0 < p2 else 0
        #  569: JMPF (10), #579
        if not tmp:
            goto .lbl_579
        #  572: MUL #1, (BP+-4), (BP+-4)
        #  576: JMPF #0, #647
        pass # 1
        goto .lbl_647
        #  579: ADD (BP+-4), #0, (BP+1)
        label .lbl_579
        q0 = p0
        #  583: ADD (BP+-3), #-1, (BP+2)
        q1 = p1 - 1
        #  587: MUL (BP+-2), #2, (BP+3)
        q2 = p2 * 2
        #  591: MUL #1, #598, (BP+0)
        #  595: JMPF #0, #556
        (q0, q1, q2, q3) = self.func556(q0, q1, q2)
        #  598: ADD #0, (BP+1), (BP+-4)
        p0 = q0
        #  602: ADD #1, #0, (BP+-1)
        p3 = 1
        #  606: LT (BP+-4), (BP+-2), (10)
        tmp = 1 if p0 < p2 else 0
        #  610: JMPF (10), #617
        if not tmp:
            goto .lbl_617
        #  613: MUL #0, #1, (BP+-1)
        p3 = 0
        #  617: MUL (BP+-2), (BP+-1), (BP+-2)
        label .lbl_617
        p2 *= p3
        #  621: LT #0, (BP+-3), (10)
        tmp = 1 if 0 < p1 else 0
        #  625: JMPF (10), #639
        if not tmp:
            goto .lbl_639
        #  628: ADD (BP+-1), #0, (BP+1)
        q0 = p3
        #  632: MUL #639, #1, (BP+0)
        #  636: JMPT #1, (514)
        (q0) = self.funcs[self.mem[514]](self, q0)
        #  639: MUL (BP+-2), #-1, (BP+-2)
        label .lbl_639
        p2 = -p2
        #  643: ADD (BP+-4), (BP+-2), (BP+-4)
        p0 += p2
        #  647: ADD_BP #-5
        label .lbl_647
        #  649: JMPT #1, (BP+0)
        pass # 0
        return (p0, p1, p2, p3)

    funcs = {
      0: func0, 11: func11, 330: func330, 451: func451, 482: func482, 515: func515, 556: func556
    }

    code = "3,8,1005,8,330,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,29,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,51,1,1103,2,10,1006,0,94,1006,0,11,1,1106,13,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,87,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,109,2,1105,5,10,2,103,16,10,1,1103,12,10,2,105,2,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,146,1006,0,49,2,1,12,10,2,1006,6,10,1,1101,4,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,183,1,6,9,10,1006,0,32,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,213,2,1101,9,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,239,1006,0,47,1006,0,4,2,6,0,10,1006,0,58,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,274,2,1005,14,10,1006,0,17,1,104,20,10,1006,0,28,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,309,101,1,9,9,1007,9,928,10,1005,10,15,99,109,652,104,0,104,1,21101,0,937263411860,1,21102,347,1,0,1105,1,451,21101,932440724376,0,1,21102,1,358,0,1105,1,451,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,29015167015,1,21101,0,405,0,1106,0,451,21102,1,3422723163,1,21101,0,416,0,1106,0,451,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,868389376360,1,21101,0,439,0,1105,1,451,21102,825544712960,1,1,21102,1,450,0,1106,0,451,99,109,2,21201,-1,0,1,21101,0,40,2,21102,482,1,3,21102,1,472,0,1106,0,515,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,477,478,493,4,0,1001,477,1,477,108,4,477,10,1006,10,509,1101,0,0,477,109,-2,2106,0,0,0,109,4,2101,0,-1,514,1207,-3,0,10,1006,10,532,21102,1,0,-3,22101,0,-3,1,22102,1,-2,2,21102,1,1,3,21101,551,0,0,1106,0,556,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,579,2207,-4,-2,10,1006,10,579,22102,1,-4,-4,1106,0,647,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,1,598,0,1106,0,556,22101,0,1,-4,21101,1,0,-1,2207,-4,-2,10,1006,10,617,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,639,21201,-1,0,1,21102,639,1,0,105,1,514,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0"
