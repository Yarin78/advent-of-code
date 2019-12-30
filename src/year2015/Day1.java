package year2015;

import lib.AoCBase;
import lib.Kattio;

public class Day1 extends AoCBase {
    public static void main(String[] args) {
        new Day1().runStdin();
//        new Day1().runSample();
//        new Day1().runSampleUntilEOF();
//        new Day1().runTestcase();
    }

    public void run(Kattio io) {
        String line = io.getLine();
        long answer = line.chars().reduce(0, (cur, c) -> (char) c == '(' ? cur + 1 : cur - 1);
        io.println(answer);

        long index = 0, sum = 0;
        for (char c : line.toCharArray()) {
            index += 1;
            sum += c == '(' ? 1 : -1;
            if (sum < 0) break;
        }
        io.println(index);
    }
}
