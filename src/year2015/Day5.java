package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day5 extends AoCBase {
    public static void main(String[] args) {
//        new Day5().runStdin();
//        new Day5().runSample();
//        new Day5().runSampleUntilEOF();
        new Day5().runTestcase();
    }

    public void run(Kattio io) {
        int cnt = 0, cnt2 = 0;
        for (String line : io.getLines()) {
            int vowels = 0;
            boolean consec = false, forbid;
            char last = 0;
            for (int i = 0; i < line.length(); i++) {
                char c = line.charAt(i);
                if ("aeiou".contains("" + c)) vowels++;
                if (i > 0) {
                    if (c == last) consec = true;
                }
                last = c;
            }
            forbid = line.contains("ab") || line.contains("cd") || line.contains("pq") || line.contains("xy");
            if (vowels >= 3 && consec && !forbid) cnt++;

            boolean rep = false, split = false;
            for (int i = 0; i < line.length(); i++) {
                if (i > 0 && i + 1 < line.length() && line.substring(i + 1).contains(line.substring(i-1, i+1))) rep = true;
                if (i > 1 && line.charAt(i-2) == line.charAt(i)) split = true;
            }
            if (rep && split) cnt2++;
        }
        io.println(cnt);
        io.println(cnt2);
    }
}
