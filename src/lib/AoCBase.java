package lib;

import java.io.InputStream;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public abstract class AoCBase {

    private final Pattern intPattern;

    protected AoCBase() {
        intPattern = Pattern.compile("-?[0-9]+");
    }

    protected void runStdin() {
        Kattio io = new Kattio(System.in, System.out);
        try {
            run(io);
        } catch (Exception e) {
            e.printStackTrace();
        }
        io.close();
    }

    protected void runSample() {
        InputStream resourceAsStream = getInputAsResource(".sample.in");

        Kattio io = new Kattio(resourceAsStream, System.out);
        try {
            run(io);
        } catch (Exception e) {
            e.printStackTrace();
        }
        io.close();
    }

    protected void runSampleUntilEOF() {
        InputStream resourceAsStream = getInputAsResource(".sample.in");

        Kattio io = new Kattio(resourceAsStream, System.out);
        try {
            while (io.hasMoreTokens()) {
                run(io);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        io.close();
    }

    public void runTestcase() {
        InputStream resourceAsStream = getInputAsResource(".in");

        Kattio io = new Kattio(resourceAsStream, System.out);
        try {
            run(io);
        } catch (Exception e) {
            e.printStackTrace();
        }
        io.close();
    }

    private InputStream getInputAsResource(String suffix) {
        String simpleClassName = getClass().getSimpleName().toLowerCase();
        String relativeResource = simpleClassName + suffix;
        InputStream resourceAsStream = getClass().getResourceAsStream(relativeResource);
        if (resourceAsStream == null) {
            throw new RuntimeException("Failed to find the resource " + relativeResource + " from package " + this.getClass().getPackage().getName());
        }
        return resourceAsStream;
    }

    protected abstract void run(Kattio io);

    public int[] parseIntsOnLine(String line) {
        Matcher matcher = intPattern.matcher(line);
        ArrayList<Integer> ints = new ArrayList<>();
        while (matcher.find()) {
            ints.add(Integer.parseInt(matcher.group()));
        }
        return ints.stream().mapToInt(i->i).toArray();
    }

    public void debug(Object o) {
        System.err.print("DEBUG: ");
        internalDebug(o);
        System.err.println();
    }

    private void internalDebug(Object o) {
        if (o.getClass().isArray()) {
            System.err.print("[");
            for (int i = 0; i < Array.getLength(o); i++) {
                if (i > 0) System.err.print(", ");
                internalDebug(Array.get(o, i));
            }
            System.err.print("]");
        } else {
            System.err.print(o);
        }
    }

}
