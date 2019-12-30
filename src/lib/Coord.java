package lib;

import java.util.HashMap;
import java.util.Objects;

public class Coord {
    public static final Coord LEFT = new Coord(-1 ,0);
    public static final Coord RIGHT = new Coord(1 ,0);
    public static final Coord UP = new Coord(0 ,-1);
    public static final Coord DOWN = new Coord(0 ,1);

    public static HashMap<Character, Coord> directions = new HashMap<Character, Coord>() {{
            put('<', LEFT);
            put('>', RIGHT);
            put('^', UP);
            put('v', DOWN);
    }};

    public int X,Y;

    public Coord(int x, int y) {
        X = x;
        Y = y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Coord coord = (Coord) o;
        return X == coord.X &&
                Y == coord.Y;
    }

    public Coord add(Coord other) {
        return new Coord(X + other.X, Y + other.Y);
    }

    @Override
    public int hashCode() {
        return Objects.hash(X, Y);
    }

    @Override
    public String toString() {
        return String.format("{X=%d, Y=%d}", X, Y);
    }
}
