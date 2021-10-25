package graph;

import java.util.*;

public class Graph {
    private final List<Node> nodes;

    public Graph() {
        this.nodes = new ArrayList<>();
    }

    public void initializeGraph() {
        Node a = new Node(1);
        Node b = new Node(2);
        Node c = new Node(3);
        Node d = new Node(4);
        Node e = new Node(5);

        a.addNeighbour(b);
        a.addNeighbour(c);
        b.addNeighbour(c);
        c.addNeighbour(d);
        e.addNeighbour(d);

        nodes.addAll(Arrays.asList(a, b, c, d, e)); // immutable
    }

    public void forwardChecking(Stack<Node> visited, Stack<String> solution, Finished finished) {
        if (finished.finished) {
            return;
        }

        if (visited.size() == nodes.size()) {
            System.out.println("FC: Solution found");

            for (String sol : solution) {
                System.out.println(sol);
            }

            System.out.println();
            finished.finished = true;
            return;
        }

        List<Node> unvisitedNodes = getUnvisitedNodes(visited);

        for (Node node : unvisitedNodes) {
            visited.add(node);

            for (String color : node.getPossibleColors()) {
                node.setColor(color);

                List<Node> changedNeighbours = new ArrayList<>();

                for (Node neighbour : node.getNeighbours()) {
                    if (visited.contains(neighbour)) {
                        continue;
                    }

                    if (neighbour.removeColor(color)) {
                        changedNeighbours.add(neighbour);
                    }
                }

                solution.add(currentConfiguration(visited));
                forwardChecking(visited, solution, finished);
                solution.pop();

                for (Node neighbour : changedNeighbours) {
                    neighbour.addColor(color);
                }
            }

            visited.pop();
        }

    }

    public void minimumRemainingValue(Stack<Node> visited, Stack<String> solution, Finished finished) {
        if (finished.finished) {
            return;
        }

        if (visited.size() == nodes.size()) {
            System.out.println("MRV: Solution Found");

            for (String sol : solution) {
                System.out.println(sol);
            }

            System.out.println();
            finished.finished = true;
            return;
        }

        PriorityQueue<Node> sortedNodes = new PriorityQueue<>(getUnvisitedNodes(visited));

        while (!sortedNodes.isEmpty()) {
            Node node = sortedNodes.poll();
            visited.add(node);

            for (String color : node.getPossibleColors()) {
                node.setColor(color);

                List<Node> changedNeighbours = new ArrayList<>();

                for (Node neighbour : node.getNeighbours()) {
                    if (visited.contains(neighbour)) {
                        continue;
                    }

                    if (neighbour.removeColor(color)) {
                        changedNeighbours.add(neighbour);
                    }
                }

                solution.add(currentConfiguration(visited));
                minimumRemainingValue(visited, solution, finished);
                solution.pop();

                for (Node neighbour : changedNeighbours) {
                    neighbour.addColor(color);
                }

            }

            visited.pop();
        }
    }

    private String currentConfiguration(Stack<Node> visited) {
        StringBuilder stringBuilder = new StringBuilder();
        for (Node node : nodes) {
            stringBuilder.append(String.format("%3d(%s) -> ", node.getId(), visited.contains(node) ? node.getColor() : " "));
            StringBuilder stringBuilderColor = new StringBuilder();
            for (String color : node.getPossibleColors()) {
                stringBuilderColor.append(color);
            }

            stringBuilder.append(String.format("%-6s", stringBuilderColor));
        }

        return stringBuilder.toString();
    }


    private List<Node> getUnvisitedNodes(Stack<Node> visited) {
        List<Node> unvisitedNodes = new ArrayList<>();

        for (Node node : nodes) {
            if (!visited.contains(node)) {
                unvisitedNodes.add(node);
            }
        }

        return unvisitedNodes;
    }

}
