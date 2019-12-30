package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day2 extends AoCBase {
    public static void main(String[] args) {
//        new Day2().runStdin();
//        new Day2().runSample();
//        new Day2().runSampleUntilEOF();
        new Day2().runTestcase();
    }

    public void run(Kattio io) {
        int paper = 0, ribbon = 0;
        for (String line : io.getLines()) {
            int[] dims = parseIntsOnLine(line);
            //debug(dims);
            int l = dims[0], w = dims[1], h = dims[2];
            paper += 2 * l * w + 2 * w * h + 2 * h * l + Math.min(Math.min(l * w, w * h), h * l);

            ribbon += Math.min(Math.min(2*(l+w), 2*(l+h)), 2*(w+h)) + l*w*h;
        }
        io.println(paper);
        io.println(ribbon);
    }

}
