package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day17 extends AoCBase {
    public static void main(String[] args) {
//        new Day17().runStdin();
//        new Day17().runSample();
//        new Day17().runSampleUntilEOF();
        new Day17().runTestcase();
    }

    public void run(Kattio io) {
        int[] cap = new int[20];
        int n = 0;
        for (String line : io.getLines()) {
            cap[n++] = Integer.parseInt(line);
        }
        int cnt = 0, best = 100;
        for (int i = 0; i < (1 << n); i++) {
            int sum = 0, t = 0;
            for (int j = 0; j < n; j++) {
                if (((1<<j) & i) > 0) {
                    sum += cap[j];
                    t++;
                }
            }
            if (sum == 150) {
                if (t < best) {
                    best = t;
                    cnt = 1;
                } else if (t == best) {
                    cnt++;
                }
            }
        }
        io.println(cnt);
    }
}
