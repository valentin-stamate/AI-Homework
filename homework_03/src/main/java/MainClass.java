import java.util.List;

public class MainClass {
    public static void main(String[] args) {
        MasterMind masterMind = new MasterMind(6, 10, 4);

        MasterMind.showSequence(masterMind.getSequence());
        List<String> chosenPieces = masterMind.choosePieces();
        MasterMind.showSequence(chosenPieces);
        System.out.println(masterMind.compareSequence(chosenPieces));
        System.out.println(masterMind.isSolution(chosenPieces));

    }
}
