package lib;

import java.io.*;
import java.util.Iterator;
import java.util.StringTokenizer;

public class Kattio extends PrintWriter {
    public Kattio(InputStream i) {
        super(new BufferedOutputStream(System.out));
        r = new BufferedReader(new InputStreamReader(i));
    }

    public Kattio(InputStream i, OutputStream o) {
        super(new BufferedOutputStream(o));
        r = new BufferedReader(new InputStreamReader(i));
    }

    public boolean hasMoreTokens() {
        return peekToken() != null;
    }

    public int getInt() {
        return Integer.parseInt(nextToken());
    }

    public double getDouble() {
        return Double.parseDouble(nextToken());
    }

    public long getLong() {
        return Long.parseLong(nextToken());
    }

    public String getWord() {
        return nextToken();
    }

    public String getLine() {
        return nextLine();
    }


    private BufferedReader r;
    private String line;
    private StringTokenizer st;
    private String token;

    private String peekToken() {
        if (token == null)
            try {
                while (st == null || !st.hasMoreTokens()) {
                    line = r.readLine();
                    if (line == null) return null;
                    st = new StringTokenizer(line);
                }
                token = st.nextToken();
            } catch (IOException e) {
            }
        return token;
    }

    private String nextLine() {
        // If any tokens have been read from the current line, they will be returned again
        if (line == null) {
            try {
                line = r.readLine();
            } catch (IOException e) {
            }
        }
        String result = line;
        line = null;
        st = null;
        token = null;
        return result;
    }

    private String nextToken() {
        String ans = peekToken();
        token = null;
        return ans;
    }

    public Iterable<String> getLines() {
        Iterator<String> iterator = new Iterator<String>() {
            String line;

            @Override
            public boolean hasNext() {
                if (line == null) {
                    line = getLine();
                }
                return line != null;
            }

            @Override
            public String next() {
                String nextLine;
                if (hasNext()) {
                    nextLine = line;
                    line = null;
                    return nextLine;
                }
                return null;
            }
        };
        return () -> iterator;
    }
}
