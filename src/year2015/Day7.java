package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.HashMap;

public class Day7 extends AoCBase {
    public static void main(String[] args) {
//        new Day7().runStdin();
//        new Day7().runSample();
//        new Day7().runSampleUntilEOF();
        new Day7().runTestcase();
    }

    private static class Expr {
        public String op;
        public String p1, p2;
        private int cache = -1;

        public Expr(String[] parts) {
            int x = parts.length - 2;
            if (x == 1) {
                op = "ASSIGN";
                p1 = parts[0];
            } else if (x == 2) {
                assert parts[0].equals("NOT");
                op = parts[0];
                p1 = parts[1];
            } else {
                op = parts[1];
                p1 = parts[0];
                p2 = parts[2];
            }
        }

        private int evalParam(String param, HashMap<String, Expr> map) {
            try {
                int x = Integer.parseInt(param);
                return x;
            } catch (NumberFormatException e) {
                return map.get(param).eval(map);
            }
        }

        public int eval(HashMap<String, Expr> map) {
            if (cache >= 0) return cache;

            int val = 0;
            switch (op) {
                case "ASSIGN":
                    val = evalParam(p1, map);
                    break;
                case "RSHIFT":
                    val = evalParam(p1, map) >> Integer.parseInt(p2);
                    break;
                case "LSHIFT":
                    val = evalParam(p1, map) << Integer.parseInt(p2);
                    break;
                case "AND":
                    val = evalParam(p1, map) & evalParam(p2, map);
                    break;
                case "OR":
                    val = evalParam(p1, map) | evalParam(p2, map);
                    break;
                case "NOT":
                    val = ~evalParam(p1, map);
                    break;
                default :
                    throw new RuntimeException("Unknown op: " + op);
            }
            val &= 65535;
            cache = val;
            return val;
        }
    }

    public void run(Kattio io) {
        HashMap<String, Expr> map = new HashMap<String, Expr>();
        for (String line : io.getLines()) {
            String[] parts = line.split(" ");
            map.put(parts[parts.length-1], new Expr(parts));
        }
        for (String s : map.keySet()) {
            io.println(s + ":" + map.get(s).eval(map));
        }

        io.println("a = " + map.get("a").eval(map));
    }
}
