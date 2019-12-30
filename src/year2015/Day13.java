package year2015;

import lib.AoCBase;
import lib.Kattio;
import yarin.algorithms.Sequences;

public class Day13 extends AoCBase {
    public static void main(String[] args) {
//        new Day13().runStdin();
//        new Day13().runSample();
//        new Day13().runSampleUntilEOF();
        new Day13().runTestcase();
    }

    public void run(Kattio io) {
        int n = 9;
        int[][] m = new int[n][n];
        for (String line : io.getLines()) {
            int delta = parseIntsOnLine(line)[0];
            if (line.contains("lose")) delta=-delta;
            String[] parts = line.split(" ");
            int n1 = parts[0].charAt(0)-'A', n2 = parts[parts.length-1].charAt(0)-'A';
            if (n1 > 6) n1 = 7;
            if (n2 > 6) n2 = 7;
            m[n1][n2] = delta;
        }
        debug(m);

        Integer[] current = new Integer[n];
        for (int i = 0; i < n; i++) {
            current[i] = i;
        }
        int best = 0;
        do {
            int sum = 0;
            for (int i = 0; i < n; i++) {
                sum += m[current[i]][current[(i+1)%n]];
                sum += m[current[(i+1)%n]][current[i]];
            }
            if (sum>best) best = sum;

        } while (Sequences.nextPermutation(current));

        io.println(best);
    }
}
