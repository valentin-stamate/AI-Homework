import java.util.*;
import java.util.List;

public class MasterMind {
    private final int n;
    private final int m;
    private final int k;

    private final String[] colors;
    private final int[] availablePieces;
    private final HashMap<String, Integer> colorsMap;

    private final List<String> sequence;

    /**
     * n = number of colors
     * m = number of balls with a color
     * k = length of secret code
     */
    public MasterMind(int n, int m, int k) {
        this.n = n;
        this.m = m;
        this.k = k;

        colors = new String[n];
        colorsMap = new HashMap<>();

        for (int i = 0; i < n; i++) {
            colors[i] = Colors.COLORS[i];
            colorsMap.put(colors[i], i);
        }

        availablePieces = createAvailablePieces();
        sequence = initializeSequence();
    }

    private int[] createAvailablePieces() {
        int[] availablePieces = new int[n];

        for (int i = 0; i < n; i++) {
            availablePieces[i] = m;
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
            String color = colors[index];

            if (!sequence.contains(color)) {
                sequence.add(color);
                length--;
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

    public List<String> randomSequence() {
        Random random = new Random();
        List<String> sequence = new ArrayList<>();

        int length = k;

        while (length != 0) {
            int index = random.nextInt(n);
            String color = colors[index];

            if (availablePieces[index] == 0) {
                continue;
            }

            if (!sequence.contains(color)) {
                sequence.add(color);
                length--;
            }
        }

        subtractSequence(sequence);
        return sequence;
    }

    public boolean sequenceIsValid(List<String> sequence) {
        for (String color : sequence) {
            if (availablePieces[colorsMap.get(color)] == 0) {
                return false;
            }
        }

        return true;
    }

    public List<List<String>> generateMoves() {
        List<List<String>> moves = new ArrayList<>();
        String[] buffer = new String[sequence.size()];

        allMoves(0, buffer, moves);

        return moves;
    }

    public void allMoves(int position, String[] move, List<List<String>> list) {
        int n = sequence.size();

        if (position == n) {
            if (sequenceIsValid(asList(move))) {
                list.add(asList(move));
            }
            return;
        }

        for (String c : colors) {
            if (!sequenceContainsColor(move, position, c)) {
                move[position] = c;
                allMoves(position + 1, move, list);
            }
        }
    }

    private List<String> asList(String[] list) {
        return new ArrayList<>(Arrays.asList(list));
    }

    private boolean sequenceContainsColor(String[] list, int len, String color) {
        for (int i = 0; i < len; i++) {
            if (list[i].equals(color)) {
                return true;
            }
        }

        return false;
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
        List<String> secretCode = new ArrayList<>();

        for (int i = 0; i < k; i++) {
            secretCode.add("X");
        }

        List<String> previousSequences = new ArrayList<>();
        List<Integer> previousGuesses = new ArrayList<>();

        System.out.println("Available colors:");
        for (String color : colors) {
            System.out.println(color);
        }
        System.out.printf("\n\n%25s\n", "Game Started");

        String border = "========================================================================";
        StringBuilder secretColors = new StringBuilder();
        for (var piece : secretCode) {
            secretColors.append(String.format("%-7s ", piece));
        }

        boolean playerWon = false;

        while (true) {
            boolean validSequence = true;

            System.out.println(border);
            System.out.printf("||         %-58s ||", secretColors);

            System.out.println();

            int sequences = previousGuesses.size();

            System.out.println(border);
            for (int i = 0; i < sequences; i++) {
                System.out.printf("|| %-2d | %-45s     Guessed: %-2s ||\n", 2 * n - i, previousSequences.get(i), previousGuesses.get(i));
            }
            System.out.println(border);

            if (playerWon) {
                break;
            }

            System.out.printf("\nAvailable Colors: %s\n", remainingColorsAsString(this.colors, availablePieces));

            /* checking for the remaining colors */
            int availableColors = 0;
            for (var n : availablePieces) {
                if (n != 0) {
                    availableColors++;
                }
            }

            if (availableColors < k) {
                System.out.println("No more colors left. You lost.");
                break;
            }

            if (sequences == 2 * n) {
                System.out.println("\nNo remaining moves left. You lost!");
                System.out.println("The secret colors were :");
                for (var color : sequence) {
                    System.out.printf("%-7s ", color);
                }
                break;
            }
            String[] colors;
            var newColors = new ArrayList<String>();

            Scanner scanner = new Scanner(System.in);

            System.out.println("Enter colors:");
            String s = scanner.nextLine();
            s = s.toUpperCase();
            s = s.replace('\n', '\0');

            colors = s.split(" ");
            for (var c : colors) {
                if (c.length() >= 1) {
                    newColors.add(c);
                }
            }

            if (newColors.size() != k) {
                System.out.printf("Sequence must have %d pieces\n", k);
                continue;
            }

            for (String color : newColors) {
                if (!colorsMap.containsKey(color)) {
                    System.out.printf("Color %s is not available\n", color);
                    validSequence = false;
                    continue;
                }

                if (availablePieces[colorsMap.get(color)] == 0) {
                    System.out.printf("Not enough pieces for color %s\n", color);
                    validSequence = false;
                }
            }

            if (areDuplicates(newColors)) {
                System.out.println("All colors in a sequence must be different");
                validSequence = false;
            }

            if (validSequence) {
                subtractSequence(newColors);

                List<String> newSequence = new ArrayList<>((newColors));
                var piecesGuessed = compareSequence(newSequence);

                previousGuesses.add(piecesGuessed);
                previousSequences.add(listToString(newColors, "%-7s "));

                System.out.printf("You guessed %d pieces\n\n", piecesGuessed);

                if (isSolution(newSequence)) {
                    System.out.println("\nYou won");
                    playerWon = true;
                }
            }
        }
    }

    public void startMinimax() {
        List<String> currentMove = randomSequence();
        List<String> bestMove = new ArrayList<>();

        List<List<String>> previousMoves = new ArrayList<>();
        previousMoves.add(new ArrayList<>(currentMove));

        boolean solutionFound = false;

        for (int i = 2 * n; i >= 1; i--) {
            minimax(1, currentMove, previousMoves, true, Integer.MIN_VALUE, Integer.MAX_VALUE, bestMove);

            currentMove = bestMove;
            previousMoves.add(new ArrayList<>(currentMove));

            if (isSolution(currentMove)) {
                solutionFound = true;
                break;
            }
        }

        if (solutionFound) {
            System.out.println("Solution found");
        }

        System.out.println(sequence);
        System.out.println();

        for (var list : previousMoves) {
            System.out.println(list);
        }

    }

    public int minimax(int depth, List<String> sequence, List<List<String>> previousMoves, boolean maximizing, int alpha, int beta, List<String> bestMove) {
        if (depth == 0) {
            return depth + compareSequence(sequence);
        }

        if (compareSequence(sequence) == sequence.size()) {
            return depth + sequence.size();
        }

        List<List<String>> moves = generateMoves();

        if (maximizing) {
            int max = Integer.MIN_VALUE;

            for (var move : moves) {
                boolean found = false;

                for (List<String> list : previousMoves) {
                    if (equalSequences(move, list)) {
                        found = true;
                        break;
                    }
                }

                if (found) {
                    continue;
                }

                subtractSequence(move);
                /* maximizing should be false, but we have only one player */
                int score = minimax(depth - 1, move, previousMoves, true, alpha, beta, bestMove);
                undoSequence(move);

                if (max < score) {
                    max = score;

                    bestMove.clear();
                    bestMove.addAll(move);
                }

                alpha = Math.max(alpha, score);

                if (beta <= alpha) {
                    break;
                }

            }

            return max;
        }

        System.out.println("Something went wrong");
        /* minimizing */
        int min = Integer.MAX_VALUE;

        for (var move : moves) {

            subtractSequence(move);
            int score = minimax(depth - 1, move, previousMoves, true, alpha, beta, bestMove);
            undoSequence(move);

            if (min > score) {
                min = score;

                bestMove.clear();
                bestMove.addAll(move);
            }

            beta = Math.min(beta, score);

            if (beta <= alpha) {
                break;
            }
        }

        return min;

    }

    private boolean equalSequences(List<String> a, List<String> b) {
        for (int i = 0; i < a.size(); i++) {
            if (!a.get(i).equals(b.get(i))) {
                return false;
            }
        }

        return true;
    }

    private void subtractSequence(List<String> colors) {
        for (String color : colors) {
            availablePieces[colorsMap.get(color)]--;
        }
    }

    private void undoSequence(List<String> colors) {
        for (String color : colors) {
            availablePieces[colorsMap.get(color)]++;
        }
    }

    private boolean areDuplicates(List<String> colors) {
        for (int i = 0; i < k - 1; i++) {
            for (int j = i + 1; j < k; j++) {
                if (Objects.equals(colors.get(i), colors.get(j)))
                    return true;
            }
        }
        return false;
    }

    private static <T> String listToString(List<T> list, String delim) {
        StringBuilder sb = new StringBuilder();

        for (var string : list) {
            sb.append(String.format(delim, string));
        }

        return sb.toString();
    }

    private static String remainingColorsAsString(String[] colors, int[] availablePieces) {
        StringBuilder sb = new StringBuilder();

        int n = colors.length;

        for (int i = 0; i < n; i++) {
            sb.append(String.format("%s(%d)  ", colors[i], availablePieces[i]));
        }

        return sb.toString();
    }

}
