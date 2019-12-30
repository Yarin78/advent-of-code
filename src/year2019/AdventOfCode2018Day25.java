import yarin.yal.UnionFind;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;

public class AdventOfCode2018Day25 {
    public static class Coord {
        private int index;
        public int a;
        public int b;
        public int c;
        public int d;

        public Coord(int index, int a, int b, int c, int d) {
            this.index = index;
            this.a = a;
            this.b = b;
            this.c = c;
            this.d = d;
        }

        public int distance(Coord other) {
            return Math.abs(a-other.a)+Math.abs(b-other.b)+Math.abs(c-other.c)+Math.abs(d-other.d);
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        Kattio io = new Kattio(new FileInputStream("src/aoc2018_25.in"), System.out);

        String line;
        ArrayList<Coord> coords = new ArrayList<>();
        while ((line = io.getWord()) != null) {
            String[] parts = line.split(",");
            Coord coord = new Coord(
                    coords.size(),
                    Integer.parseInt(parts[0]),
                    Integer.parseInt(parts[1]),
                    Integer.parseInt(parts[2]),
                    Integer.parseInt(parts[3]));
            coords.add(coord);
        }
        UnionFind uf = new UnionFind(coords.size());
        for (Coord coord : coords) {
            for (Coord coord1 : coords) {
                if (coord.distance(coord1) <= 3) {
                    uf.unionSet(coord.index, coord1.index);
                }
            }
        }
        HashSet<Integer> sets = new HashSet<>();
        for (Coord coord : coords) {
            sets.add(uf.findSet(coord.index));
        }
        io.println(sets.size());
        io.close();

    }
}
