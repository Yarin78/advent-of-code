package year2019.lib;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.concurrent.*;

public class IntCode {
    public static final int MEM_OFFSET_START = 0;
    public static final int MEM_OFFSET_END = 5000;

    public int id;
    public long[] factorySettings;
    public long[] mem;
    public int[] instrCount;
    public Input input;
    public Output output;
    public int ip;
    public long basePtr;
    public int count;  // num instructions executed
    public long lastInput, lastOutput;
    public boolean halted, blockedOnInput;

    public IntCode(int programId, String code) {
        long[] parsed = Arrays.stream(code.split(",")).mapToLong(Long::parseLong).toArray();
        factorySettings = new long[MEM_OFFSET_START + MEM_OFFSET_END + parsed.length];
        for (int i = 0; i < parsed.length; i++) {
            factorySettings[i + MEM_OFFSET_START] = parsed[i];
        }
        reset();
        initIo(null, null);
    }

    public void reset() {
        mem = Arrays.copyOf(factorySettings, factorySettings.length);
        ip = 0;
        count = 0;
        basePtr = 0;
        instrCount = new int[mem.length];
        halted = false;
        blockedOnInput = false;
    }

    public void initIo(Input input, Output output) {
        this.input = input == null ? new Pipe() : input;
        this.output = output == null ? new Pipe() : output;
    }

    public List<Long> run(Input input, Output output) {
        return run(input, output, 0);
    }

    public List<Long> run(Input input, Output output, int steps) {
        initIo(input, output);

        if (steps > 0) {
            while (steps > 0 && step());
        } else {
            while (step());
        }

        if (this.output instanceof Pipe) {
            return ((Pipe) this.output).getRemaining();
        }
        return null;
    }

    private static int[] numParamModeParams = new int[] {
            0,
            2, 2, 0, 1, 2, 2, 2, 2, 1
    };

    private long read(long addr) {
        return mem[(int) addr + MEM_OFFSET_START];
    }

    private void write(long addr, long value) {
        mem[(int) addr + MEM_OFFSET_START] = value;
    }

    private boolean step() {
        if (halted) {
            throw new RuntimeException("Machine already halted");
        }

        count++;
        if (count % 100000 == 0) {
            System.out.print(".");
            System.out.flush();
        }
        instrCount[ip + MEM_OFFSET_START]++;

        int opcode = (int) read(ip);
        int paramMode = opcode / 100;
        opcode %= 100;
        long params[] = null;
        if (opcode < numParamModeParams.length) {
            params = new long[numParamModeParams[opcode]];
            for (int i = 0; i < params.length; i++) {
                params[i] = read(ip+i+1);  // assumes the params comes directly after the opcode
                if (paramMode % 10 == 0) {
                    params[i] = read(params[i]);
                } else if (paramMode % 10 == 2) {
                    params[i] = read(basePtr + params[i]);
                }
                paramMode /= 10;
            }
        }
        long ptr = paramMode % 10 == 2 ? basePtr : 0;

        switch (opcode) {
            case 1: // ADD z = x + y
                write((ptr + read(ip+3)), params[0] + params[1]);
                ip += 4;
                break;
            case 2: // MUL z = x * y
                write((ptr + read(ip+3)), params[0] * params[1]);
                ip += 4;
                break;
            case 3: // IN x
                lastInput = input.get();
                write((ptr + read(ip+1)), lastInput);
                ip += 2;
                break;
            case 4 : // OUT x
                lastOutput = params[0];
                output.put(params[0]);
                ip += 2;
                break;
            case 5 : // JT - IF x <> 0 JP y
                if (params[0] != 0) {
                    ip = (int) params[1];
                } else {
                    ip += 3;
                }
                break;
            case 6 : // JF - IF x == 0 JP y
                if (params[0] == 0) {
                    ip = (int) params[1];
                } else {
                    ip += 3;
                }
                break;
            case 7 : // LT - z = x < y ? 1 : 0
                write((ptr + read(ip+3)), params[0] < params[1] ? 1 : 0);
                ip += 4;
                break;
            case 8 : // EQ - z = x == y ? 1 : 0
                write((ptr + read(ip+3)), params[0] == params[1] ? 1 : 0);
                ip += 4;
                break;
            case 9 : // BP += x
                basePtr += params[0];
                ip += 2;
                break;
            case 99: // HALT
                halted = true;
                break;
        }

        return !halted;
    }

    interface Input {
        long get();
    }

    interface Output {
        void put(long value);
    }

    public static Pipe inPipe(long[] initialData) {
        return new Pipe(initialData);
    }

    public static class Pipe implements Input, Output {
        BlockingQueue<Long> queue = new LinkedBlockingQueue<>();

        public Long lastGet = null, lastPut = null;

        public Pipe() {
        }

        public Pipe(long[] initialInput) {
            for (long x : initialInput) {
                queue.offer(x);
            }
        }

        public Pipe(Collection<Long> initialInput) {
            for (long x : initialInput) {
                queue.offer(x);
            }
        }

        @Override
        public long get() {
            try {
                lastGet = queue.take();
                return lastGet;
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }

        @Override
        public void put(long value) {
            lastPut = value;
            queue.add(value);
        }

        public List<Long> getRemaining() {
            ArrayList<Long> result = new ArrayList<>();
            Long el;
            while ((el = queue.poll()) != null) {
                result.add(el);
            }

            return result;
        }
    }

    public static void parallelExecute(IntCode[] programs) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(programs.length);
        for (IntCode program : programs) {
            executor.submit(() -> {
                while (program.step());
            });
        }
        executor.shutdown();
        executor.awaitTermination(60, TimeUnit.SECONDS);
        if (!executor.isTerminated()) throw new RuntimeException("Not all programs finished");
    }
}
