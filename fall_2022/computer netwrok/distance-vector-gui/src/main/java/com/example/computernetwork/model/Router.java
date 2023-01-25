package com.example.computernetwork.model;

import java.util.HashMap;
import java.util.Map;

//this class store info of each router
public class Router {
    private static final int max_cost = 10000;
    private int id;
    private int dv[];
    private int next_hop[];
    private Map<Integer, Router> neighbors = new HashMap<>();
    private boolean changed = true;

    //create new router and init its DV to max cost
    public Router(int id, int dv[]) {
        this.id = id;
        this.dv = dv;
        this.next_hop = new int[this.dv.length];
        for(int i=1; i<this.dv.length; i++){
            if(this.dv[i] >=0 && this.dv[i] < this.max_cost){
                this.next_hop[i] = i;
            }
            else{
                this.next_hop[i] = -1;
            }
        }
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int[] getDv() {
        return dv;
    }

    public void setDv(int[] dv) {
        this.dv = dv;
    }

    public Map<Integer, Router> getNeighbors() {
        return neighbors;
    }

    public void setNeighbors(Map<Integer, Router> neighbors) {
        this.neighbors = neighbors;
    }

    public int[] getNext_hop() {
        return next_hop;
    }

    public void setNext_hop(int[] next_hop) {
        this.next_hop = next_hop;
    }

    public boolean isChanged() {
        return changed;
    }

    public void setChanged(boolean changed) {
        this.changed = changed;
    }

    //compute its DV whenever receive updated DV from its neighbor
    public void compute(){
        changed = false;
        for(int i=1; i< dv.length; i++){
            for(Router nb : neighbors.values()){
                //DV[i] = Math.min(DV[i], DV[nb.Id] + nb.DV[i]);
                if(dv[i] > (dv[nb.id] + nb.dv[i])){
                    dv[i] = (dv[nb.id] + nb.dv[i]);
                    next_hop[i] = nb.id;
                    changed = true;
                }
            }
        }
    }
}
