import graph.Finished;
import graph.Graph;
import java.util.Stack;

public class Main {

    public static void main(String[] args) {
        Graph graph = new Graph();
        graph.initializeGraph();

        graph.minimumRemainingValue(new Stack<>(), new Stack<>(), new Finished());
        graph.forwardChecking(new Stack<>(), new Stack<>(), new Finished());
    }
}
