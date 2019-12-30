package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.ArrayList;

public class Day14 extends AoCBase {
    public static void main(String[] args) {
//        new Day14().runStdin();
//        new Day14().runSample();
//        new Day14().runSampleUntilEOF();
        new Day14().runTestcase();
    }

    public class Reindeer {
        public String name;
        public int speed, flyTime, restTime;
        public int pos;

        public Reindeer(String name, int speed, int flyTime, int restTime) {
            this.name = name;
            this.speed = speed;
            this.flyTime = flyTime;
            this.restTime = restTime;
        }

        public int distance(int time) {
            int d = 0;
            while (time > 0) {
                int f = Math.min(time, flyTime);
                d += f*speed;
                time -= f;
                int r = Math.min(time, restTime);
                time -= r;
            }
            return d;
        }
    }

    public void run(Kattio io) {
        int time = 2503, best = 0;
        ArrayList<Reindeer> rs = new ArrayList<>();
        for (String line : io.getLines()) {
            int[] ints = parseIntsOnLine(line);
            Reindeer r = new Reindeer(line.split(" ")[0], ints[0], ints[1], ints[2]);
            rs.add(r);
            int d = r.distance(time);
            if (d>best) best = d;
        }
        io.println(best);

        int[] scores = new int[rs.size()];
        for (int i = 1; i <= time; i++) {
            int lead = 0;
            for (Reindeer r : rs) {
                int d = r.distance(i);
                lead = Math.max(d, lead);
            }
            for (int j = 0; j < rs.size(); j++) {
                if (rs.get(j).distance(i) == lead) scores[j]++;
            }
        }
        debug(scores);
    }
}
