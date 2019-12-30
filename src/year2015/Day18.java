package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day18 extends AoCBase {
    public static void main(String[] args) {
//        new Day18().runStdin();
//        new Day18().runSample();
//        new Day18().runSampleUntilEOF();
        new Day18().runTestcase();
    }

    public void run(Kattio io) {
        String[] grid = new String[100];
        int i = 0;
        for (String line : io.getLines()) {
            if (i == 0 || i == 99) {
                line = "#" + line.substring(1, 99) + "#";
            }
            grid[i++] = line;
        }
        for (int iter = 0; iter < 100; iter++) {
            String[] next = new String[100];
            for (int y = 0; y < 100; y++) {
                StringBuilder sb = new StringBuilder();
                for (int x = 0; x < 100; x++) {
                    int cnt = 0;
                    for (int dy = -1; dy < 2; dy++) {
                        for (int dx = -1; dx < 2; dx++) {
                            if (dx == 0 && dy == 0) continue;
                            int ny = y+dy, nx = x+dx;
                            if (ny >= 0 && nx >= 0 && ny < 100 && nx < 100 && grid[ny].charAt(nx) == '#') cnt++;
                        }
                    }
                    if ((y == 0 || y == 99) && (x == 0 || x == 99)) {
                        sb.append('#');
                    } else if (grid[y].charAt(x) == '#') {
                        if (cnt == 2 || cnt == 3) sb.append('#'); else sb.append('.');
                    } else {
                        if (cnt == 3) sb.append('#'); else sb.append('.');
                    }

                }
                next[y] = sb.toString();
            }
            grid = next;
        }
        int cnt = 0;
        for (int y = 0; y < 100; y++) {
            for (int x = 0; x < 100; x++) {
                if (grid[y].charAt(x) == '#') cnt++;

            }
        }
        io.println(cnt);
    }
}
