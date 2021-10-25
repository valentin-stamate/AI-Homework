package graph;

import java.util.ArrayList;
import java.util.List;

public class Node implements Comparable<Node> {
    private final int id;
    private String color;
    private final List<String> possibleColors;

    public List<Node> neighbours;

    public Node(int id) {
        this.possibleColors = new ArrayList<>();
        possibleColors.add(Colors.RED);
        possibleColors.add(Colors.GREEN);
        possibleColors.add(Colors.BLUE);
        this.neighbours = new ArrayList<>();
        this.id = id;
    }

    public void addNeighbour(Node node) {
        neighbours.add(node);
        node.neighbours.add(this);
    }

    public void setColor(String color) {
        this.color = color;
    }

    public void addColor(String color) {
        possibleColors.add(color);
    }

    public int getId() {
        return id;
    }

    public String getColor() {
        return color;
    }

    public List<Node> getNeighbours() {
        return neighbours;
    }

    public List<String> getPossibleColors() {
        return possibleColors;
    }

    public boolean removeColor(String color) {
        return possibleColors.remove(color);
    }

    @Override
    public int compareTo(Node node) {
        return Integer.compare(possibleColors.size(), node.possibleColors.size());
    }

}
