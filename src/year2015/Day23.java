package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.ArrayList;

public class Day23 extends AoCBase {
    public static void main(String[] args) {
//        new Day23().runStdin();
//        new Day23().runSample();
//        new Day23().runSampleUntilEOF();
        new Day23().runTestcase();
    }

    public class State {
        public int a, b, ip;

        @Override
        public String toString() {
            return "State{" +
                    "a=" + a +
                    ", b=" + b +
                    ", ip=" + ip +
                    '}';
        }

        public State(int a, int b, int ip) {
            this.a = a;
            this.b = b;
            this.ip = ip;
        }
    }

    public Instruction parse(String line) {
        String[] parts = line.replaceAll(",", "").split(" ");
        if (parts[0].equals("hlf")) {
            return new Half(parts[parts.length-1].charAt(0));
        }
        if (parts[0].equals("tpl")) {
            return new Triple(parts[parts.length-1].charAt(0));
        }
        if (parts[0].equals("inc")) {
            return new Incr(parts[parts.length-1].charAt(0));
        }

        if (parts[0].equals("jmp")) {
            return new Jump(Integer.parseInt(parts[1]));
        }

        if (parts[0].equals("jie")) {
            return new JumpIfEven(parts[1].charAt(0), Integer.parseInt(parts[2]));
        }
        if (parts[0].equals("jio")) {
            return new JumpIfOne(parts[1].charAt(0), Integer.parseInt(parts[2]));
        }
        throw new RuntimeException("Failed to parse " + line);
    }

    public abstract class Instruction {

        public abstract State execute(State state);

    }

    public class Half extends Instruction {
        public char reg;

        public Half(char reg) {
            this.reg = reg;
        }

        public State execute(State state) {
            if (reg == 'a') {
                return new State(state.a / 2, state.b, state.ip+1);
            } else {
                return new State(state.a, state.b / 2, state.ip+1);
            }
        }
    }

    public class Triple extends Instruction {
        public char reg;

        public Triple(char reg) {
            this.reg = reg;
        }

        public State execute(State state) {
            if (reg == 'a') {
                return new State(state.a * 3, state.b, state.ip+1);
            } else {
                return new State(state.a, state.b * 3, state.ip+1);
            }
        }
    }

    public class Incr extends Instruction {
        public char reg;

        public Incr(char reg) {
            this.reg = reg;
        }

        public State execute(State state) {
            if (reg == 'a') {
                return new State(state.a + 1, state.b, state.ip+1);
            } else {
                return new State(state.a, state.b + 1, state.ip+1);
            }
        }
    }

    public class Jump extends Instruction {
        public int ofs;

        public Jump(int ofs) {
            this.ofs = ofs;
        }

        public State execute(State state) {
            return new State(state.a, state.b, state.ip+ofs);
        }
    }

    public class JumpIfEven extends Instruction {
        public char reg;
        public int ofs;

        public JumpIfEven(char reg, int ofs) {
            this.reg = reg;
            this.ofs = ofs;
        }

        public State execute(State state) {
            if ((reg == 'a' ? state.a : state.b) % 2 == 0) {
                return new State(state.a, state.b, state.ip+ofs);
            } else {
                return new State(state.a, state.b, state.ip+1);
            }
        }
    }

    public class JumpIfOne extends Instruction {
        public char reg;
        public int ofs;

        public JumpIfOne(char reg, int ofs) {
            this.reg = reg;
            this.ofs = ofs;
        }

        public State execute(State state) {
            if ((reg == 'a' ? state.a : state.b) == 1) {
                return new State(state.a, state.b, state.ip+ofs);
            } else {
                return new State(state.a, state.b, state.ip+1);
            }
        }
    }

    public void run(Kattio io) {
        ArrayList<Instruction> instructions = new ArrayList<Instruction>();
        for (String line : io.getLines()) {
            instructions.add(parse(line));
        }
        State state = new State(1, 0, 0);
        while (state.ip >= 0 && state.ip < instructions.size()) {
            if (state.ip == 39) debug(state);
            state = instructions.get(state.ip).execute(state);

        }
        io.println(state);
        /*
        int a = 26623, b = 0;
        while (a > 1) {
            if (a % 2 == 0) a/= 2; else a *= 3;
            b++;
        }
        io.println(b);
        */
        /*
        if a == 1:
  A = 31911
else:
  A = 19683*A + 26623

BAR:
if a == 1:
  HALT
b++
if a % 2 == 0:
  a /= 2
else:
  a = a * 3 + 1
jmp BAR

         */
    }
}
