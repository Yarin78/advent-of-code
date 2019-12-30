package year2015;

import lib.AoCBase;
import lib.Kattio;

import javax.xml.bind.DatatypeConverter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;

public class Day24 extends AoCBase {
    public static void main(String[] args) {
//        new Day24().runStdin();
//        new Day24().runSample();
//        new Day24().runSampleUntilEOF();
        new Day24().runTestcase();
    }

    public int bitCnt(int i) {
        int cnt = 0;
        while (i > 0) {
            cnt ++;
            i &= (i-1);
        }
        return cnt;
    }

    public List<Integer> getWeights(int mask, int[] w) {
        ArrayList<Integer> al = new ArrayList<>();
        for (int i = 0; (1<<i) <= mask; i++) {
            if (((1<<i) & mask) > 0) al.add(w[i]);
        }
        return al;
    }

    public long qe(int mask, int[] w) {
        long res = 1;
        for (int i = 0; (1<<i) <= mask; i++) {
            if (((1<<i) & mask) > 0) res *= w[i];
        }
        return res;
    }

    public void run(Kattio io) {
        int[] w = new int[100];
        int n = 0, sum = 0;
        for (String line : io.getLines()) {
            w[n++] = Integer.parseInt(line);
            sum += w[n-1];
        }

        ArrayList<Integer> ways = new ArrayList<Integer>();
        generate(n, w, 0,0, sum / 4, ways);
        ways.sort((m1, m2) -> {
            if (bitCnt(m1) != bitCnt(m2)) return bitCnt(m1) - bitCnt(m2);
            return Long.compare(qe(m1, w), qe(m2, w));
        });
        debug(ways.size());
        for (Integer way : ways) {
            for (Integer way2 : ways) {
                if ((way & way2) == 0) {
//                    io.println(String.format("%20s  %d", Integer.toBinaryString(way), qe(way, w)));
                    io.println(getWeights(way, w) + " QE = " + qe(way, w) + "  " + getWeights(way2, w));
                    return;
                }
            }
            io.println("Skipping " + getWeights(way, w));
        }
    }

    private void generate(int n, int[] w, int pos, int mask, int left, ArrayList<Integer> ways) {
        if (pos == n) {
            if (left == 0) {
                ways.add(mask);
            }
        } else {
            generate(n, w, pos+1, mask, left, ways);
            if (left >= w[pos]) generate(n, w, pos+1, mask+(1<<pos), left-w[pos], ways);
        }
    }
}
