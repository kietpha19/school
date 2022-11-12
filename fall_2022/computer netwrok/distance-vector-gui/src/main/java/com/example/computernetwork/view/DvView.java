package com.example.computernetwork.view;

import java.util.List;

public class DvView {
    private String destination;
    private String distance;
    private String next_hop;

    public DvView(String destination, String distance, String next_hop) {
        this.destination = destination;
        this.distance = distance;
        this.next_hop = next_hop;
    }

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }

    public String getDistance() {
        return distance;
    }

    public void setDistance(String distance) {
        this.distance = distance;
    }

    public String getNext_hop() {
        return next_hop;
    }

    public void setNext_hop(String next_hop) {
        this.next_hop = next_hop;
    }
}
