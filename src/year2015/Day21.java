package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.ArrayList;

public class Day21 extends AoCBase {
    public static void main(String[] args) {
        new Day21().runStdin();
//        new Day21().runSample();
//        new Day21().runSampleUntilEOF();
//        new Day21().runTestcase();
    }

    public class Equipment {
        public String type;
        public int cost, damage, armor;

        public Equipment(String type, int cost, int damage, int armor) {
            this.type = type;
            this.cost = cost;
            this.damage = damage;
            this.armor = armor;
        }
    }

    public void run(Kattio io) {
        ArrayList<Equipment> equipments = new ArrayList<Equipment>();
        equipments.add(new Equipment("weapon", 8, 4, 0));
        equipments.add(new Equipment("weapon", 10, 5, 0));
        equipments.add(new Equipment("weapon", 25, 6, 0));
        equipments.add(new Equipment("weapon", 40,7, 0));
        equipments.add(new Equipment("weapon", 74, 8, 0));

        equipments.add(new Equipment("armor", 13, 0, 1));
        equipments.add(new Equipment("armor", 31, 0, 2));
        equipments.add(new Equipment("armor", 53, 0, 3));
        equipments.add(new Equipment("armor", 75, 0, 4));
        equipments.add(new Equipment("armor", 102, 0, 5));

        equipments.add(new Equipment("ring", 25, 1, 0));
        equipments.add(new Equipment("ring", 50, 2, 0));
        equipments.add(new Equipment("ring", 100, 3, 0));
        equipments.add(new Equipment("ring", 20, 0, 1));
        equipments.add(new Equipment("ring", 40, 0, 2));
        equipments.add(new Equipment("ring", 80, 0, 3));

        int bestCost = Integer.MAX_VALUE;
        int worstCost = 0;
        for (int i = 0; i < (1 << equipments.size()); i++) {
            int w = 0, a = 0, r = 0;
            int cost = 0, damage = 0, armor = 0;
            for (int j = 0; j < equipments.size(); j++) {
                Equipment e = equipments.get(j);
                if (((1<<j) & i) > 0) {
                    cost += e.cost;
                    damage += e.damage;
                    armor += e.armor;
                    if (e.type.equals("weapon")) w++;
                    if (e.type.equals("armor")) a++;
                    if (e.type.equals("ring")) r++;
                }
            }
            if (w != 1) continue;
            if (a > 1) continue;
            if (r > 2) continue;
            boolean winning = fight(100, damage, armor, 103, 9, 2);
            if (cost < bestCost && winning) {
                bestCost = cost;
            }
            if (cost > worstCost && !winning) {
                worstCost = cost;
            }

        }
        io.println(bestCost);
        io.println(worstCost);

    }

    private boolean fight(int hp, int damage, int armor, int bossHp, int bossDamage, int bossArmor) {
        while (true) {
            bossHp -= Math.max(damage - bossArmor, 1);
            if (bossHp <= 0) return true;
            hp -= Math.max(bossDamage - armor, 1);
            if (hp <= 0) return false;
        }
    }
}
