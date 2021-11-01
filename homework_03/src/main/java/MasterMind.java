import java.util.*;

public class MasterMind {
    private final int n;
    private final int m;
    private final int k;
    private final List<String> colors;
    private final List<String> sequence;
    private final List<Integer> availablePieces;
    private final List<String> secretCode;

    public MasterMind(int n, int m, int k) {
        this.n = n;
        this.m = m;
        this.k = k;
        secretCode = new ArrayList<>(Arrays.asList("X", "X", "X", "X"));

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
            System.out.printf("%-7s ", color);
        }
        System.out.println();
    }

    public void startGame() {

        boolean valid;
        List<List<String>> previousSequences = new ArrayList<>();
        List<Integer> previousGuesses = new ArrayList<>();
        while (true) {
            System.out.print("    ");
            for (var piece : secretCode) {
                System.out.printf("%-7s ", piece);
            }
            System.out.println();
            if (previousSequences.size() != 0) {
                int i = 0;
                for (var seq : previousSequences) {
                    i++;
                    System.out.printf("%-4d", i);
                    for (var color : seq) {
                        System.out.printf("%-7s ", color);
                    }
                    System.out.println("     Guessed : " + previousGuesses.get(i - 1));
                }
                System.out.println();
            }
            if (previousSequences.size() == 2 * n) {
                System.out.println("You lost!");
                System.out.println("The secret code was :");
                for (var color : sequence) {
                    System.out.printf("%-7s ", color);
                }
                break;
            }
            String[] colors;
            var newColors = new ArrayList<String>();
            do {
                Scanner scanner = new Scanner(System.in);
                valid = true;
                System.out.println("Enter code:");
                String s = scanner.nextLine();
                s = s.toUpperCase();
                s = s.replace('\n', '\0');
                newColors.clear();
                colors = s.split(" ");
                for (var c : colors) {
                    if (c.length() >= 3) {
                        newColors.add(c);
                    }
                }

                if (newColors.size() != 4) {
                    System.out.println("Sequence must have 4 pieces");
                    valid = false;
                    continue;
                }
                for (String color : newColors) {
                    if (!isValid(color)) {
                        System.out.println("Not enough pieces left or not valid colors");
                        valid = false;
                        break;
                    }
                }
                if (!isValidSequence(newColors)) {
                    System.out.println("All colors in a sequence must be different");
                    valid = false;
                }
            } while (!valid);
            List<String> newSequence = new ArrayList<>((newColors));
            previousSequences.add(newSequence);
            var piecesGuessed = compareSequence(newSequence);
            previousGuesses.add(piecesGuessed);
            System.out.println("you guessed " + piecesGuessed + " pieces");
            if (isSolution(newSequence)) {
                System.out.println("You won");
                break;
            }


        }
    }

    private boolean isValidSequence(List<String> colors) {
        for (int i = 0; i < k - 1; i++) {
            for (int j = i + 1; j < k; j++) {
                if (Objects.equals(colors.get(i), colors.get(j)))
                    return false;
            }
        }
        return true;
    }

    private boolean isValid(String color) {
        try {
            return colors.contains(color) && availablePieces.get(colors.indexOf(color)) > 0;
        } catch (IndexOutOfBoundsException e) {
            return false;
        }
    }

}
