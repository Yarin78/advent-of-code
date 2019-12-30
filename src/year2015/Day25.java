package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day25 extends AoCBase {
    public static void main(String[] args) {
        new Day25().runStdin();
//        new Day25().runSample();
//        new Day25().runSampleUntilEOF();
//        new Day25().runTestcase();
    }

    public void run(Kattio io) {
        int ROW = 2978, COL = 3083;
        //ROW = 10; COL = 10;
        long code = 20151125;
        for (int diag = 0; ; diag++) {
            int row = diag+1, col = 1;
            while (row >= 1) {
                if (row == ROW && col == COL) {
                    io.println(code);
                    return;
                }
                //debug(row + "," + col + " => " + code);
                row--;
                col++;
                code = (code * 252533) % 33554393;
            }


        }
    }
}
