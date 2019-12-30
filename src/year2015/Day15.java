package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day15 extends AoCBase {
    public static void main(String[] args) {
//        new Day15().runStdin();
//        new Day15().runSample();
//        new Day15().runSampleUntilEOF();
        new Day15().runTestcase();
    }

    int[][] ingredients;

    public void run(Kattio io) {
        ingredients = new int[4][5];
        int i = 0;
        for (String line : io.getLines()) {
            int[] ints = parseIntsOnLine(line);
            int cap = ints[0], dur = ints[1], flav = ints[2], text = ints[3], cal = ints[4];
            ingredients[i] = ints;
            i++;
        }
        int ans = go(0, 100, new int[4]);
        io.println(ans);
    }

    private int go(int cur, int left, int[] amount) {
        if (cur == amount.length) {
            int prod = 1;
            for (int i = 0; i < 5; i++) {
                int psum = 0;
                for (int j = 0; j < cur; j++) {
                    psum += amount[j] * ingredients[j][i];
                }
                if (i < 4) {
                    if (psum < 0) psum = 0;
                    prod *= psum;
                } else if (psum != 500) {
                    prod = 0;
                }
            }
            return prod;
        }
        int best = 0;
        for (int i = 0; i <= left; i++) {
            amount[cur] = i;
            best = Math.max(best, go(cur+1,left-i,amount));
        }
        return best;
    }
}
