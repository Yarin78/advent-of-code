package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.HashMap;

public class Day16 extends AoCBase {
    public static void main(String[] args) {
//        new Day16().runStdin();
//        new Day16().runSample();
//        new Day16().runSampleUntilEOF();
        new Day16().runTestcase();
    }

    public void run(Kattio io) {
        HashMap<String, Integer> map = new HashMap<>();
        map.put("children", 3);
        map.put("cats", 7);
        map.put("samoyeds", 2);
        map.put("pomeranians", 3);
        map.put("akitas", 0);
        map.put("vizslas", 0);
        map.put("goldfish", 5);
        map.put("trees", 3);
        map.put("cars", 2);
        map.put("perfumes", 1);

        for (String line : io.getLines()) {
            line = line.replaceAll(":", "").replaceAll(",", "");
            String[] parts = line.split(" ");
            boolean impossible = false;
            for (int i = 2; i < parts.length; i+=2) {
                if (parts[i].equals("cats") || parts[i].equals("trees")) {
                    if (!(Integer.parseInt(parts[i+1]) > map.get(parts[i]))) impossible = true;
                } else if (parts[i].equals("pomeranians") || parts[i].equals("goldfish")) {
                    if (!(Integer.parseInt(parts[i + 1]) < map.get(parts[i]))) impossible = true;
                } else {
                    if (map.get(parts[i]) != Integer.parseInt(parts[i + 1])) impossible = true;
                }
            }
            if (!impossible) {
                io.println(line);
            }
        }
    }
}
