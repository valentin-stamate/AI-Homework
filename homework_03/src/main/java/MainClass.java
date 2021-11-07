import java.util.List;

public class MainClass {
    public static void main(String[] args) {
        MasterMind masterMind = new MasterMind(4, 10, 4);
//        masterMind.startGame();
        masterMind.startMinimax();
    }

}
