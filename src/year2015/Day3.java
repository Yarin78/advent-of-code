package year2015;

import lib.AoCBase;
import lib.Coord;
import lib.Kattio;

import java.util.HashMap;
import java.util.HashSet;

public class Day3 extends AoCBase {
    public static void main(String[] args) {
//        new Day3().runStdin();
//        new Day3().runSample();
//        new Day3().runSampleUntilEOF();
        new Day3().runTestcase();
    }

    public void run(Kattio io) {
        HashSet<Coord> coords = new HashSet<>();
        Coord cur1 = new Coord(0, 0);
        Coord cur2 = new Coord(0, 0);

        coords.add(cur1);
        coords.add(cur2);
        String line = io.getLine();
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (i % 2 == 0) {
                cur1 = cur1.add(Coord.directions.get(c));
                coords.add(cur1);
            } else {
                cur2 = cur2.add(Coord.directions.get(c));
                coords.add(cur2);
            }
        }
        io.println(coords.size());
    }
}
