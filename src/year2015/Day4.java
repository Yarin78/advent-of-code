package year2015;

import lib.AoCBase;
import lib.Kattio;
import sun.security.provider.MD5;

import javax.xml.bind.DatatypeConverter;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Day4 extends AoCBase {
    public static void main(String[] args) {
        new Day4().runStdin();
//        new Day4().runSample();
//        new Day4().runSampleUntilEOF();
//        new Day4().runTestcase();
    }

    public void run(Kattio io) {
        try {
            String key = "bgvyzdsv";
            MessageDigest md = MessageDigest.getInstance("MD5");
            int i = 0;
            while (true) {
                md.reset();
                md.update((key + i).getBytes());
                if (DatatypeConverter.printHexBinary(md.digest()).startsWith("000000")) {
                    io.println(i);
                    return;
                }
                i += 1;
                if (i % 10000 == 0) {
                    debug(i);
                }
            }
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }
}
