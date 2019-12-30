package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day10 extends AoCBase {
    public static void main(String[] args) {
        new Day10().runStdin();
//        new Day10().runSample();
//        new Day10().runSampleUntilEOF();
//        new Day10().runTestcase();
    }

    public void run(Kattio io) {
        String cur = io.getLine();
        for (int i = 0; i < 50; i++) {
            StringBuilder sb = new StringBuilder();
            int pos = 0;
            while (pos < cur.length()) {
                int j = pos;
                while (j < cur.length() && cur.charAt(j) == cur.charAt(pos)) j++;
                sb.append(j-pos);
                sb.append(cur.charAt(pos));
                pos = j;
            }
            cur = sb.toString();
            //debug(cur);
        }
        io.println(cur.length());
    }
}
