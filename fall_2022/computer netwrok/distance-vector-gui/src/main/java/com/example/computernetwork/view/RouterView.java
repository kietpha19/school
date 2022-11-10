package com.example.computernetwork.view;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

public class RouterView implements Serializable {
    private String id;
    private String dv;
    private String neighbors;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getDv() {
        return dv;
    }

    public void setDv(String dv) {
        this.dv = dv;
    }

    public String getNeighbors() {
        return neighbors;
    }

    public void setNeighbors(String neighbors) {
        this.neighbors = neighbors;
    }
}
