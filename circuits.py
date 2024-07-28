class circuit(object):
    def __init__(self, in1, in2):
        self.in1_ = in1
        self.in2_ = in2


class andgate(circuit):

    def getCircuitOutput(self):
        if self.in1_ == 1 and self.in2_ == 1:
            return 1
        else:
            return 0


class orgate(circuit):

    def getCircuitOutput(self):
        if self.in1_ == 0 and self.in2_ == 0:
            return 0
        else:
            return 1


class notgate(circuit):
    def __init__(self, in1):
        self.in1_ = in1

    def getCircuitOutput(self):
        if self.in1_ == 1:
            return 0
        elif self.in1_ == 0:
            return 1


class xorgate(circuit):
    def __init__(self, in1, in2):
        self.in1_ = in1
        self.in2_ = in2

    def getCircuitOutput(self):
        notg0 = notgate(self.in1_)
        out_notg0 = notg0.getCircuitOutput()

        notg1 = notgate(self.in2_)
        out_notg1 = notg1.getCircuitOutput()

        andg0 = andgate(self.in1_, out_notg1)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(self.in2_, out_notg0)
        out_andg1 = andg1.getCircuitOutput()

        org0 = orgate(out_andg0, out_andg1)
        out_org0 = org0.getCircuitOutput()

        return out_org0


# Hint: you may implement some multi-input logic gates to help you build the circuit,
# for example, below is a 3-input andgate3 boolean algebra: Y=ABC
class andgate3(circuit):

    def __init__(self, in1, in2, in3):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3

    def getCircuitOutput(self):
        andg0 = andgate(self.in1_, self.in2_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(out_andg0, self.in3_)
        out_andg1 = andg1.getCircuitOutput()

        return out_andg1


class andgate6(circuit):

    def __init__(self, in1, in2, in3, in4, in5, in6):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.in5_ = in5
        self.in6_ = in6

    def getCircuitOutput(self):
        andg0 = andgate(self.in1_, self.in2_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(self.in3_, self.in4_)
        out_andg1 = andg1.getCircuitOutput()

        andg2 = andgate(self.in5_, self.in6_)
        out_andg2 = andg2.getCircuitOutput()

        andg3 = andgate3(out_andg0, out_andg1, out_andg2)
        out_andg3 = andg3.getCircuitOutput()

        return out_andg3


class orgate3(circuit):
    def __init__(self, in1, in2, in3):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3

    def getCircuitOutput(self):
        org0 = orgate(self.in1_, self.in2_)
        out_org0 = org0.getCircuitOutput()

        org1 = orgate(out_org0, self.in3_)
        out_org1 = org1.getCircuitOutput()

        return out_org1


# 2to1 mux implemented by notgate, andgates and orgates
class mux_2to1(circuit):

    def __init__(self, in1, in2, select):
        self.in1_ = in1
        self.in2_ = in2
        self.select_ = select

    def getCircuitOutput(self):
        not_select = notgate(self.select_)
        out_notselect = not_select.getCircuitOutput()

        and1 = andgate(self.in1_, out_notselect)
        out_and1 = and1.getCircuitOutput()

        and2 = andgate(self.in2_, self.select_)
        out_and2 = and2.getCircuitOutput()

        or1 = orgate(out_and1, out_and2)
        out_or1 = or1.getCircuitOutput()

        return out_or1


# 4to1 mux implemented by 2to1 muxes
class mux_4to1(circuit):

    def __init__(self, in1, in2, in3, in4, select1, select2):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.select1_ = select1
        self.select2_ = select2

    def getCircuitOutput(self):
        mux1 = mux_2to1(self.in1_, self.in2_, self.select2_)
        out_mux1 = mux1.getCircuitOutput()

        mux2 = mux_2to1(self.in3_, self.in4_, self.select2_)
        out_mux2 = mux2.getCircuitOutput()

        mux3 = mux_2to1(out_mux1, out_mux2, self.select1_)
        out_mux3 = mux3.getCircuitOutput()

        return out_mux3


# fulladder implemented with logic gates

class fulladder(circuit):

    def __init__(self, in1, in2, cIn):
        self.in1_ = in1
        self.in2_ = in2
        self.cIn = cIn

    def getSumOutput(self):
        xorg0 = xorgate(self.in1_, self.in2_)
        xout_org0 = xorg0.getCircuitOutput()

        xorg1 = xorgate(xout_org0, self.cIn)
        sum = xorg1.getCircuitOutput()

        return sum

    def getCarryOutput(self):
        xorg0 = xorgate(self.in1_, self.in2_)
        xout_org0 = xorg0.getCircuitOutput()

        andg0 = andgate(xout_org0, self.cIn)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(self.in1_, self.in2_)
        out_andg1 = andg1.getCircuitOutput()

        org1 = orgate(out_andg0, out_andg1)
        carryOut = org1.getCircuitOutput()

        return carryOut

class decoder_5x32(circuit):
    def __init__(self, in1, in2, in3, in4, in5):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.in5_ = in5

    def getCircuitOutput(self):
        output = [0] * 27

        output.append(self.in1_)
        output.append(self.in2_)
        output.append(self.in3_)
        output.append(self.in4_)
        output.append(self.in5_)

        return output


class decoderReg(circuit):

    def __init__(self, Instr_RegFiled):
        self.Instr_RegFiled_ = Instr_RegFiled

    def getCircuitOutput(self):
        input_bit = self.Instr_RegFiled_

        decoder = decoder_5x32(input_bit[0], input_bit[1], input_bit[2], input_bit[3], input_bit[4])
        out_decoder = decoder.getCircuitOutput()
        decoders = out_decoder

        return decoders


class mainCtrol(circuit):
    def __init__(self, op_5, op_4, op_3, op_2, op_1, op_0):
        self.op_5 = op_5
        self.op_4 = op_4
        self.op_3 = op_3
        self.op_2 = op_2
        self.op_1 = op_1
        self.op_0 = op_0

    def getCircuitOutput(self):
        andg0 = andgate6(notgate(self.op_5).getCircuitOutput(), notgate(self.op_4).getCircuitOutput(),
                         notgate(self.op_3).getCircuitOutput(), notgate(self.op_2).getCircuitOutput(),
                         notgate(self.op_1).getCircuitOutput(),
                         notgate(self.op_0).getCircuitOutput()).getCircuitOutput()
        andg1 = andgate6(self.op_5, notgate(self.op_4), notgate(self.op_3), notgate(self.op_2), self.op_1,
                         self.op_0).getCircuitOutput()
        andg2 = andgate6(self.op_5, notgate(self.op_4), self.op_3, notgate(self.op_2), self.op_1,
                         self.op_0).getCircuitOutput()
        andg3 = andgate6(notgate(self.op_5), notgate(self.op_4), notgate(self.op_3), self.op_2, notgate(self.op_1),
                         notgate(self.op_0)).getCircuitOutput()

        org0 = orgate(andg1, andg2).getCircuitOutput()
        org1 = orgate(andg0, andg1).getCircuitOutput()

        op = [andg0, andg3]

        return op


class registerFile(circuit):
    def __init__(self, reg_initial_value):
        self.reg_initial_value = reg_initial_value

        self.registers = []
        for i in range(32):
            self.registers.append(self.reg_initial_value)

    def setRegValue(self, o_regDecoder, valueToSet):

        for i in range(len(self.registers)):
            if i == o_regDecoder:
                self.registers[i] = valueToSet
            else:
                self.registers[i] = self.registers[i]

        return self.registers

    def getRegValue(self, o_regDecoder):
        joined_decoder = (''.join(map(str, o_regDecoder)))
        decoders_dec = int(joined_decoder, 2)
        value = self.registers[decoders_dec]
        return value

    def getRegPlace(self, o_regDecoder):
        joined_decoder = (''.join(map(str, o_regDecoder)))
        decoders_dec = int(joined_decoder, 2)
        return decoders_dec

    def getAllRegValues(self):
        return self.registers


# 1 bit ALU implemented with logic gates
class ALU_1bit(object):

    def __init__(self, in1, in2, op, cIn, less):
        self.in1_ = in1
        self.in2_ = in2
        self.op_ = op
        self.cIn_ = cIn
        self.less_ = less

    def getCircuitOutput(self):
        ainvert = self.op_[0]
        binvert = self.op_[1]
        op1 = self.op_[2]
        op2 = self.op_[3]

        not0 = notgate(self.in1_)  # A NOT
        out_not0 = not0.getCircuitOutput()

        not1 = notgate(self.in2_)  # B NOT
        out_not1 = not1.getCircuitOutput()

        mux0 = mux_2to1(self.in1_, out_not0, ainvert)  # A MUX
        out_mux0 = mux0.getCircuitOutput()

        mux1 = mux_2to1(self.in2_, out_not1, binvert)  # B MUX
        out_mux1 = mux1.getCircuitOutput()

        andg0 = andgate(out_mux0, out_mux1)  # A B AND
        out_andg0 = andg0.getCircuitOutput()

        org0 = orgate(out_mux0, out_mux1)  # A B OR
        out_org0 = org0.getCircuitOutput()

        adder0 = fulladder(out_mux0, out_mux1, self.cIn_)  # SUM OUT FOR ADDER
        out_adder0 = adder0.getSumOutput()

        mux2 = mux_4to1(out_andg0, out_org0, out_adder0, self.less_, op1, op2)  # ALU RESULT
        out_mux2 = mux2.getCircuitOutput()

        return out_mux2

    def getCarryOutput(self):
        ainvert = self.op_[0]
        binvert = self.op_[1]

        less = self.less_

        not0 = notgate(self.in1_)  # A NOT
        out_not0 = not0.getCircuitOutput()

        not1 = notgate(self.in2_)  # B NOT
        out_not1 = not1.getCircuitOutput()

        mux0 = mux_2to1(self.in1_, out_not0, ainvert)  # A MUX
        out_mux0 = mux0.getCircuitOutput()

        mux1 = mux_2to1(self.in2_, out_not1, binvert)  # B MUX
        out_mux1 = mux1.getCircuitOutput()

        adder0 = fulladder(out_mux0, out_mux1, self.cIn_)  # CARRY OUT FOR ADDER
        out_adder0 = adder0.getCarryOutput()

        return out_adder0

    def getSet(self):
        ainvert = self.op_[0]
        binvert = self.op_[1]
        op1 = self.op_[2]
        op2 = self.op_[3]

        not0 = notgate(self.in1_)  # A NOT
        out_not0 = not0.getCircuitOutput()

        not1 = notgate(self.in2_)  # B NOT
        out_not1 = not1.getCircuitOutput()

        mux0 = mux_2to1(self.in1_, out_not0, ainvert)  # A MUX
        out_mux0 = mux0.getCircuitOutput()

        mux1 = mux_2to1(self.in2_, out_not1, binvert)  # B MUX
        out_mux1 = mux1.getCircuitOutput()

        andg0 = andgate(out_mux0, out_mux1)  # A B AND
        out_andg0 = andg0.getCircuitOutput()

        org0 = orgate(out_mux0, out_mux1)  # A B OR
        out_org0 = org0.getCircuitOutput()

        adder0 = fulladder(out_mux0, out_mux1, self.cIn_)  # SUM OUT FOR ADDER
        out_adder0 = adder0.getSumOutput()

        return out_adder0


class aluControl(circuit):
    '''
    Implement the ALU control circuit shown in Figure D.2.2 on page 7 of the slides 10_ALU_Control.pdf.
    There are eight inputs: aluOp1, aluOp2, f5, f4, f3, f2, f1, f0.
    There are four outputs of the circuit, you may put them in a python list and return as a whole.
    '''

    def __init__(self, aluOp, f5, f4, f3, f2, f1, f0):
        self.aluOp_ = aluOp
        self.f0_ = f0
        self.f1_ = f1
        self.f2_ = f2
        self.f3_ = f3
        self.f4_ = f4
        self.f5_ = f5

    def getControlBits(self):
        aluOp0 = self.aluOp_[1]
        aluOp1 = self.aluOp_[0]

        notg0 = notgate(aluOp0)
        out_notg0 = notg0.getCircuitOutput()

        notg1 = notgate(aluOp1)
        out_notg1 = notg1.getCircuitOutput()

        notg2 = notgate(self.f2_)
        out_notg2 = notg2.getCircuitOutput()

        org0 = orgate(self.f0_, self.f3_)
        out_org0 = org0.getCircuitOutput()

        andg0 = andgate(aluOp1, self.f1_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(aluOp1, out_org0)
        out_ControlBit0 = andg1.getCircuitOutput()

        org1 = orgate(out_notg1, out_notg2)
        out_ControlBit1 = org1.getCircuitOutput()

        org2 = orgate(aluOp0, out_andg0)
        out_ControlBit2 = org2.getCircuitOutput()

        andg2 = andgate(aluOp0, out_notg0)
        out_ControlBit3 = andg2.getCircuitOutput()

        ControlBits = [out_ControlBit3, out_ControlBit2, out_ControlBit1, out_ControlBit0]

        return ControlBits

class ALU_32bit(object):
    '''
    Implement a 32 bit ALU by using the 1 bit ALU.
    Your 32-bit ALU should be able to compute 32-bit AND, OR, addition, subtraction, slt(set on if less than).
    The inputs are:

    two python lists with lenth 32, e.g.:
    A = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    please note that bit 0 is at the end of the list, which means that bit 0 of A is A[31], bit 31 of A is A[0], bit 0 of B is B[31] and bit 31 of B is B[0].

    carryIn for the 0th 1-bit ALU, which take care of the bit 0.

    aluctrs, which could be a list of alu control signals:
    aluctrs[0] controls the all the 2to1 mux in each 1-bit ALU for bits of input A,
    aluctrs[1] controls the all the 2to1 mux in each 1-bit ALU for bits of input B.
    aluctrs[2] and aluctrs[3] controls all the 4to1 mux in each 1-bit ALU for choose what as output, 00 choose out from AND, 01 choose out from OR, 10 choose out from adder, 11 choose the less.

    Please note that the carryOut output of each 1-bit ALU except the 31th one should be the carryIn the next 1 bit ALU, you may use for loop here for the computation of the sequential 1-bit ALU.

    And please also note that in order to make slt work, we need to use the sum output from the adder of the 31th 1-bit ALU and make it as the less input of the 0th 1bit ALU.
    '''

    def __init__(self, a, b, aluctrs, cIn, less):
        self.a_ = a
        self.b_ = b
        self.aluctrs_ = aluctrs
        self.cIn_ = cIn
        self.less_ = less

    def getCarryOutput(self):
        result = [0] * 32
        out_result = []

        for i in range(len(self.a_) -1, -1, -1):
            if i == 31:
                result = ALU_1bit(self.a_[i], self.b_[i], self.aluctrs_, self.cIn_, self.less_)
                out_result.append(result.getCarryOutput())
            elif i != 31:
                result = ALU_1bit(self.a_[i], self.b_[i], self.aluctrs_, out_result, 0)
                out_result.insert(0,result.getCarryOutput())

        return out_result

    def getSet(self):
        result = [0] * 32
        out_result = []

        carry = [0] * 32

        carry = ALU_32bit(self.a_, self.b_, self.aluctrs_, self.cIn_, self.less_).getCarryOutput()

        for i in range(len(self.a_) - 1, -1, -1):
            if i == 31:
                result = ALU_1bit(self.a_[i], self.b_[i], self.aluctrs_, self.cIn_, self.less_)
                out_result.append(result.getSet())
            elif i != 31:
                result = ALU_1bit(self.a_[i], self.b_[i], self.aluctrs_, carry[i+1], 0)
                out_result.insert(0,result.getSet())

        return out_result

    def getResult(self):
        result = [0] * 32
        out_result = []

        carry = [0] * 32

        set = [0] * 32

        carry = ALU_32bit(self.a_, self.b_, self.aluctrs_, self.cIn_, self.less_).getCarryOutput()

        set = ALU_32bit(self.a_, self.b_, self.aluctrs_, self.cIn_, self.less_).getSet()

        for i in range(len(self.a_) - 1, -1, -1):
            if i == 31:
                result = ALU_1bit(self.a_[i], self.b_[i], self.aluctrs_, self.cIn_, set[0])
                out_result.append(result.getCircuitOutput())
            elif i != 31:
                result = ALU_1bit(self.a_[i], self.b_[i], self.aluctrs_, carry[i+1], 0)
                out_result.insert(0,result.getCircuitOutput())

        return out_result






class simpleMIPS(circuit):
    def __init__(self, registers):
        self.registers = registers

    def getCircuitOutput(self, instru):

        rs = decoderReg(instru[6:11]).getCircuitOutput()
        rt = decoderReg(instru[11:16]).getCircuitOutput()
        rd = decoderReg(instru[16:21]).getCircuitOutput()

        A = self.registers.getRegValue(rs)
        B = self.registers.getRegValue(rt)

        C = self.registers.getRegPlace(rd)

        ctrolOutput = mainCtrol(instru[0], instru[1], instru[2], instru[3], instru[4],instru[5]).getCircuitOutput()

        aluCtrolOutput = aluControl(ctrolOutput, instru[26], instru[27], instru[28], instru[29], instru[30],instru[31]).getControlBits()

        aluOutput = ALU_32bit(A, B, aluCtrolOutput, 0, 0).getResult()

        final = self.registers.setRegValue(C, aluOutput)

        return final

