import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class MasterMind {
    private final int n;
    private final int m;
    private final int k;
    private final List<String> colors;
    private final List<String> sequence;
    private final List<Integer> availablePieces;

    public MasterMind(int n, int m, int k) {
        this.n = n;
        this.m = m;
        this.k = k;

        colors = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            colors.add(Colors.COLORS[i]);
        }

        availablePieces = createAvailablePieces();
        sequence = initializeSequence();
    }

    private List<Integer> createAvailablePieces() {
        List<Integer> availablePieces = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            availablePieces.add(m);
        }

        return availablePieces;
    }

    public List<String> getSequence() {
        return sequence;
    }

    private List<String> initializeSequence() {
        Random random = new Random();
        List<String> sequence = new ArrayList<>();

        int length = k;

        while (length != 0) {
            int index = random.nextInt(n);
            String color = colors.get(index);

            if (!sequence.contains(color)) {
                sequence.add(color);
                length--;
                availablePieces.set(index, availablePieces.get(index) - 1);
            }
        }

        return sequence;
    }

    public boolean isSolution(List<String> playerSequence) {
        for (int i = 0; i < playerSequence.size(); i++) {
            if (!playerSequence.get(i).equals(sequence.get(i))) {
                return false;
            }
        }

        return true;
    }

    public List<String> choosePieces() {
        Random random = new Random();
        List<String> sequence = new ArrayList<>();

        int length = k;

        while (length != 0) {
            int index = random.nextInt(n);
            String color = colors.get(index);

            if (availablePieces.get(index) == 0) {
                continue;
            }

            if (!sequence.contains(color)) {
                sequence.add(color);
                length--;
                availablePieces.set(index, availablePieces.get(index) - 1);
            }
        }

        return sequence;
    }

    public int compareSequence(List<String> playerSequence) {
        int matched = 0;

        for (int i = 0; i < k; i++) {
            if (playerSequence.get(i).equals(sequence.get(i))) {
                matched++;
            }
        }

        return matched;
    }

    static public void showSequence(List<String> sequence) {
        for (String color : sequence) {
            System.out.printf("%s ", color);
        }
        System.out.println();
    }

}
