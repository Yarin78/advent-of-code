package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.regex.Pattern;

public class Day8 extends AoCBase {
    public static void main(String[] args) {
//        new Day8().runStdin();
//        new Day8().runSample();
//        new Day8().runSampleUntilEOF();
        new Day8().runTestcase();
    }

    public void run(Kattio io) {
        String r1 = "\\\\\"";
        String r2 = "\\\\\\\\";

        int codeChars = 0, memoryChars = 0, cnt = 0;
        for (String line : io.getLines()) {
            line = line.trim();

            for (char c : line.toCharArray()) {
                if (c == '"' || c == '\\') cnt++;
            }
            cnt+=2;

            codeChars += line.length();
            line = line.substring(1, line.length() - 1);
            line = line.replaceAll("\\\\x[0-9a-f]{2}", "?");
            line = line.replaceAll(r1, "?");
            line = line.replaceAll(r2, "?");
            memoryChars += line.length();
            debug(line);
        }
        io.println(codeChars - memoryChars);
        io.println(cnt);
    }
}
