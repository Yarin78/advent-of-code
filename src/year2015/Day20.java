package year2015;

import lib.AoCBase;
import lib.Kattio;
import yarin.algorithms.mathlib.MathStuff;
import yarin.algorithms.mathlib.Primes;

import java.util.HashSet;
import java.util.List;

public class Day20 extends AoCBase {
    public static void main(String[] args) {
        new Day20().runStdin();
//        new Day20().runSample();
//        new Day20().runSampleUntilEOF();
//        new Day20().runTestcase();
    }

    public void run(Kattio io) {
        long input = 29000000;
        long most = 0;
        Primes primes = new Primes(1000000);
        for (long house = 1; ; house++) {
            List<Long> factors = primes.getAllPrimeFactors(house);
            HashSet<Long> divisors = new HashSet<Long>();
            for (int i = 0; i < (1 << factors.size()); i++) {
                long prod = 1;
                for (int j = 0; j < factors.size(); j++) {
                    if (((1<<j) & i) > 0) prod *= factors.get(j);
                }
                divisors.add(prod);
            }

            long cnt = 0;
            for (Long d : divisors) {
                if (house / d <= 50) cnt += d*11;
            }
            if (cnt > most) {
                most = cnt;
                debug(house + " "  + most);
                if (cnt >= input) break;
            }
        }
    }
}
