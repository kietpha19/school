package com.example.computernetwork.view;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class RouterView implements Serializable {
    private String id;
    private List<DvView> dv_row;
    private String neighbors;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public List<DvView> getDv_row() {
        return dv_row;
    }

    public void setDv_row(List<DvView> dv_row) {
        this.dv_row = dv_row;
    }

    public String getNeighbors() {
        return neighbors;
    }

    public void setNeighbors(String neighbors) {
        this.neighbors = neighbors;
    }
}
