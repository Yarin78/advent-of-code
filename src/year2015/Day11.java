package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.HashSet;

public class Day11 extends AoCBase {
    public static void main(String[] args) {
        new Day11().runStdin();
//        new Day11().runSample();
//        new Day11().runSampleUntilEOF();
//        new Day11().runTestcase();
    }

    private boolean isValid(String pw) {
        boolean threeInc = false;
        for (int i = 0; i < pw.length() - 2; i++) {
            if (pw.charAt(i)+1==pw.charAt(i+1) && pw.charAt(i+1)+1 == pw.charAt(i+2)) threeInc = true;
        }
        HashSet<String> doubles = new HashSet<>();
        for (int i = 0; i < pw.length() - 1; i++) {
            if (pw.charAt(i) == pw.charAt(i+1)) doubles.add(pw.substring(i, i+2));
        }
        if (!threeInc) return false;
        if (pw.contains("i") || pw.contains("o") || pw.contains("l")) return false;
        if (doubles.size() < 2) return false;
        return true;
    }

    private String next(String cur) {
        int pos = cur.length() - 1;
        while (cur.charAt(pos) == 'z') pos--;
        String pw = cur.substring(0, pos) + (char)(cur.charAt(pos) + 1);
        while (pw.length() < 8) pw += "a";
        return pw;
    }

    public void run(Kattio io) {
        String pw = io.getLine();
        while (true) {
            pw = next(pw);
            if (isValid(pw)) {
                io.println(pw);
                break;
            }
        }
    }
}
