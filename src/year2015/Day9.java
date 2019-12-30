package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.HashMap;
import java.util.Map;

public class Day9 extends AoCBase {
    public static void main(String[] args) {
//        new Day9().runStdin();
//        new Day9().runSample();
//        new Day9().runSampleUntilEOF();
        new Day9().runTestcase();
    }

    private int n;
    private Map<String, Integer> nodeMap = new HashMap<String, Integer>();

    private int getNode(String city) {
        if (!nodeMap.containsKey(city)) {
            nodeMap.put(city, n);
            n++;
        }
        return nodeMap.get(city);
    }

    public void run(Kattio io) {
        n = 0;
        int[][] dist = new int[20][20];
        for (String line : io.getLines()) {
            String[] s = line.split(" ");
            int n1 = getNode(s[0]), n2 = getNode(s[2]);
            dist[n1][n2] = dist[n2][n1] = Integer.parseInt(s[4]);
        }
        int best = Integer.MAX_VALUE, best2=0;
        for (int i = 0; i < n; i++) {
            int d = shortest(i, (1<<n)-1-(1<<i), n, dist);
            int e = longest(i, (1<<n)-1-(1<<i), n, dist);
            if (d<best) best = d;
            if (e>best2) best2=e;
        }
        io.println(best);
        io.println(best2);
    }

    private int shortest(int cur, int left, int n, int[][] dist) {
        if (left == 0) return 0;
        int best = Integer.MAX_VALUE;
        for (int i = 0; i < n; i++) {
            if (((1<<i) & left) > 0) {
                int t = dist[cur][i] + shortest(i, left-(1<<i), n, dist);
                if (t<best) best = t;
            }
        }
        return best;
    }

    private int longest(int cur, int left, int n, int[][] dist) {
        if (left == 0) return 0;
        int best = 0;
        for (int i = 0; i < n; i++) {
            if (((1<<i) & left) > 0) {
                int t = dist[cur][i] + longest(i, left-(1<<i), n, dist);
                if (t>best) best = t;
            }
        }
        return best;
    }
}
