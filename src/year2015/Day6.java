package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day6 extends AoCBase {
    public static void main(String[] args) {
//        new Day6().runStdin();
//        new Day6().runSample();
//        new Day6().runSampleUntilEOF();
        new Day6().runTestcase();
    }

    public void run(Kattio io) {
        boolean[][] lights = new boolean[1000][1000];
        int[][] brightness = new int[1000][1000];
        for (String line : io.getLines()) {
            int[] ints = parseIntsOnLine(line);
            int action = -1;
            if (line.startsWith("toggle")) action = 0;
            if (line.startsWith("turn on")) action = 1;
            if (line.startsWith("turn off")) action = 2;
            for (int x = ints[0]; x <= ints[2]; x++) {
                for (int y = ints[1]; y <= ints[3]; y++) {
                    switch (action) {
                        case 0: lights[y][x] = !lights[y][x]; brightness[y][x] += 2; break;
                        case 1: lights[y][x] = true; brightness[y][x]++; break;
                        case 2: lights[y][x] = false; if (brightness[y][x] > 0) brightness[y][x]--; break;
                    }
                }
            }
        }
        int sum = 0, sum2 = 0;
        for (int y = 0; y < 1000; y++) {
            for (int x = 0; x < 1000; x++) {
                if (lights[y][x]) sum++;
                sum2 += brightness[y][x];
            }
        }
        io.println(sum);
        io.println(sum2);
    }
}
