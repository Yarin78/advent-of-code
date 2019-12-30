package year2015;

import lib.AoCBase;
import lib.Kattio;

import java.util.*;

public class Day22 extends AoCBase {
    public static void main(String[] args) {
        new Day22().runStdin();
//        new Day22().runSample();
//        new Day22().runSampleUntilEOF();
//        new Day22().runTestcase();
    }

    final int BOSS_DAMAGE = 8;
    final int BOSS_HP = 55;
    final int INF = 1000000;

    final int MAGIC_MISSILE_COST = 53;
    final int DRAIN_COST = 73;
    final int SHIELD_COST = 113;
    final int POISION_COST = 173;
    final int RECHARGE_COST = 229;

    public static class State implements Comparable<State> {
        public int hp, bossHp, manaLeft, poison, shield, recharge, manaSpent;
        public boolean bossTurn;

        public State(int hp, int bossHp, int manaLeft, int poison, int shield, int recharge, int manaSpent, boolean bossTurn) {
            this.hp = hp;
            this.bossHp = bossHp;
            this.manaLeft = manaLeft;
            this.poison = poison;
            this.shield = shield;
            this.recharge = recharge;
            this.manaSpent = manaSpent;
            this.bossTurn = bossTurn;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            State state = (State) o;
            return hp == state.hp &&
                    bossHp == state.bossHp &&
                    manaLeft == state.manaLeft &&
                    poison == state.poison &&
                    shield == state.shield &&
                    recharge == state.recharge &&
                    bossTurn == state.bossTurn;
        }

        @Override
        public int hashCode() {
            return Objects.hash(hp, bossHp, manaLeft, poison, shield, recharge, bossTurn);
        }

        @Override
        public int compareTo(State o) {
            return this.manaSpent - o.manaSpent;
        }
    }

    public int goBoss(int hp, int bossHp, int manaLeft, int poison, int shield, int recharge) {
        int armor = 0;
        if (poison > 0) {
            bossHp -= 3;
            poison--;
        }
        if (shield > 0) {
            shield--;
            armor = 7;
        }
        if (recharge > 0) {
            manaLeft += 101;
            recharge--;
        }
        if (bossHp <= 0) return 0;
        hp -= Math.max(1, BOSS_DAMAGE-armor);
        if (hp <= 0) return INF;
        return goYou(hp, bossHp, manaLeft, poison, shield, recharge);
    }

    Map<Integer,Integer> memo = new HashMap<Integer, Integer>();

    public int goYou(int hp, int bossHp, int manaLeft, int poison, int shield, int recharge) {
        if (bossHp <= 0) return 0;

        int state = ((((hp * (BOSS_HP + 1) + bossHp) * 501 + manaLeft) * 8 + poison) * 8 + shield) * 8 + recharge;
        if (memo.containsKey(state)) memo.get(state);

        if (poison > 0) {
            bossHp -= 3;
            poison--;
        }
        if (shield > 0) {
            shield--;
        }
        if (recharge > 0) {
            manaLeft += 101;
            recharge--;
        }

        if (bossHp <= 0) return 0;

        int best = INF;

        best = Math.min(best, goBoss(hp, bossHp, manaLeft, poison, shield, recharge));
        if (manaLeft >= 53) {
            best = Math.min(best, 53 + goBoss(hp, bossHp - 4, manaLeft - 53, poison, shield, recharge));
        }
        if (manaLeft >= 73) {
            best = Math.min(best, 73 + goBoss(hp + 2, bossHp - 2, manaLeft - 73, poison, shield, recharge));
        }
        if (manaLeft >= 113 && shield == 0) {
            best = Math.min(best, 113 + goBoss(hp, bossHp, manaLeft - 113, poison, 6, recharge));
        }
        if (manaLeft >= 173 && poison == 0) {
            best = Math.min(best, 173 + goBoss(hp, bossHp, manaLeft - 173, 6, shield, recharge));
        }
        if (manaLeft >= 229 && recharge == 0 && manaLeft <= 500) {
            best = Math.min(best, 229 + goBoss(hp, bossHp, manaLeft - 229, poison, shield, 5));
        }

        memo.put(state, best);

        return best;
    }

    public void run(Kattio io) {
        int mostMana = 0;
        HashSet<State> visited = new HashSet<State>();
        PriorityQueue<State> q = new PriorityQueue<>();
        State start = new State(50, BOSS_HP, 500, 0, 0, 0, 0, false);
        q.add(start);

        while (q.size() > 0) {
            State c = q.poll();
            if (c.manaSpent >= mostMana) {
                debug("At mana cost " + c.manaSpent);
                mostMana = c.manaSpent + 100;
            }
            if (visited.contains(c)) continue;
            visited.add(c);
            if (visited.size() % 10000 == 0) {
                debug("Visited " + visited.size());
            }

            if (c.bossHp <= 0) {
                io.println("You win at " + c.manaSpent + " cost");
                break;
            }

            if (!c.bossTurn) {
                c.hp--;
                if (c.hp <= 0) continue;
            }
            if (c.manaLeft >= 1000) continue;

            int armor = 0;
            if (c.poison > 0) {
                c.bossHp -= 3;
                c.poison--;
            }
            if (c.shield > 0) {
                c.shield--;
                armor = 7;
            }
            if (c.recharge > 0) {
                c.manaLeft += 101;
                c.recharge--;
            }
            if (c.bossHp <= 0) {
                io.println("You win at " + c.manaSpent + " cost");
                break;
            }
            if (c.bossTurn) {
                c.hp -= Math.max(1, BOSS_DAMAGE-armor);
                if (c.hp > 0) {
                    q.add(new State(c.hp, c.bossHp, c.manaLeft, c.poison, c.shield, c.recharge, c.manaSpent, false));
                }
            } else {
                // Magic missile
                if (c.manaLeft >= MAGIC_MISSILE_COST) {
                    q.add(new State(c.hp, c.bossHp - 4, c.manaLeft - MAGIC_MISSILE_COST, c.poison, c.shield, c.recharge, c.manaSpent + MAGIC_MISSILE_COST, true));
                }
                // Drain
                if (c.manaLeft >= DRAIN_COST) {
                    q.add(new State(c.hp + 2, c.bossHp - 2, c.manaLeft - DRAIN_COST, c.poison, c.shield, c.recharge, c.manaSpent + DRAIN_COST, true));
                }
                // Shield
                if (c.manaLeft >= SHIELD_COST && c.shield == 0) {
                    q.add(new State(c.hp, c.bossHp, c.manaLeft - SHIELD_COST, c.poison, 6, c.recharge, c.manaSpent + SHIELD_COST, true));
                }
                // Poison
                if (c.manaLeft >= POISION_COST && c.poison == 0) {
                    q.add(new State(c.hp, c.bossHp, c.manaLeft - POISION_COST, 6, c.shield, c.recharge, c.manaSpent + POISION_COST, true));
                }
                // Recharge
                if (c.manaLeft >= RECHARGE_COST && c.recharge == 0) {
                    q.add(new State(c.hp, c.bossHp, c.manaLeft - RECHARGE_COST, c.poison, c.shield, 5, c.manaSpent + RECHARGE_COST, true));
                }
            }
        }
    }
}
