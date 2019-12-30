package year2015;

import com.google.gson.Gson;
import com.google.gson.internal.LinkedTreeMap;
import lib.AoCBase;
import lib.Kattio;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Map;

public class Day12 extends AoCBase {
    public static void main(String[] args) {
//        new Day12().runStdin();
//        new Day12().runSample();
//        new Day12().runSampleUntilEOF();
        new Day12().runTestcase();
    }

    public void run(Kattio io) {
        String line = io.getLine();
        int[] ints = parseIntsOnLine(line);
        int sum = 0;
        for (int x : ints) {
            sum += x;
        }
        io.println(sum);

        Gson gson = new Gson();
        Object o = gson.fromJson(line, Object.class);
        io.println(getValue(o));

    }

    private int getValue(Object o) {
        int value;
        if (o.getClass() == LinkedTreeMap.class) {
            value = recSum((LinkedTreeMap<String, Object>) o);
        } else if (o.getClass() == ArrayList.class) {
            value = recSum((ArrayList) o);
        } else {
            try {
                value = (int) Double.parseDouble(o.toString());
            } catch (NumberFormatException e) {
                value = 0;
            }
        }
        return value;
    }

    private int recSum(LinkedTreeMap<String, Object> o) {
        int sum = 0;
        for (String key : o.keySet()) {
            if (o.get(key).equals("red")) return 0;
            sum += getValue(o.get(key));
        }
        return sum;
    }

    private int recSum(ArrayList list) {
        int sum = 0;
        for (Object o : list) {
            sum += getValue(o);
        }
        return sum;
    }
}
