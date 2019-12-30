package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.*;

public class Day19 extends AoCBase {
    public static void main(String[] args) {
//        new Day19().runStdin();
//        new Day19().runSample();
//        new Day19().runSampleUntilEOF();
        new Day19().runTestcase();
    }

    class Transformation {
        public String from, to;

        public Transformation(String from, String to) {
            this.from = from;
            this.to = to;
        }
    }

    private Set<String> replacements(String cur, List<Transformation> transformations) {
        Set<String> result = new HashSet<>();
        for (Transformation entry : transformations) {

            String key = entry.from, value = entry.to;
            int pos = 0, x;
            while ((x = cur.indexOf(key, pos)) >= 0) {
                String t = cur.substring(0, x) + value + cur.substring(x + key.length());
                result.add(t);
                pos = x + 1;
            }
        }

        return result;
    }

    public void run(Kattio io) {
        String line;
        ArrayList<Transformation> input = new ArrayList<>();
        while ((line = io.getLine()).length() > 0) {
            String[] parts = line.split(" => ");
            input.add(new Transformation(parts[0], parts[1]));
        }
        String start = io.getLine();

        io.println(replacements(start, input).size());

        /*
        Queue<String> q = new LinkedList<>();
        HashMap<String, Integer> dist = new HashMap<>();
        q.add("e");
        dist.put("e", 0);
        while (!dist.containsKey(start)) {
            String cur = q.remove();
            int curDist = dist.get(cur);
            //debug("At " + cur + " dist " + curDist);
            for (String t : replacements(cur, input)) {
                if (t.length() > start.length()) continue;
                if (!dist.containsKey(t)) {
                    q.add(t);
                    dist.put(t, curDist + 1);
                }
            }
        }
        io.println(dist.get(start));
        */

        int cnt = 0;
        while (!start.equals("e")) {
            for (Transformation transformation : input) {
                int pos;
                while ((pos = start.indexOf(transformation.to)) >= 0) {
                    start = start.substring(0, pos) + transformation.from + start.substring(pos + transformation.to.length());
                    cnt++;
                    debug(start);
                }
            }
        }
        io.println(cnt);
    }
}
