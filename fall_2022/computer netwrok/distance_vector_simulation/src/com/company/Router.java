package com.company;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Router {
    private static final int max_cost = 10000;
    int Id;
    int DV[];
    int next_hop[];
    Map<Integer, Router> neighbors = new HashMap<>();
    boolean changed = true;

    //constructor
    Router(int Id, int distance_vector[]){
        this.Id = Id;
        this.DV = distance_vector;
        this.next_hop = new int[this.DV.length];
        for(int i=1; i<this.DV.length; i++){
            if(this.DV[i] >=0 && this.DV[i] < this.max_cost){
                this.next_hop[i] = i;
            }
            else{
                this.next_hop[i] = -1;
            }
        }
    }

    public void compute(){
        changed = false;
        for(int i=1; i< DV.length; i++){
            for(Router nb : neighbors.values()){
                //DV[i] = Math.min(DV[i], DV[nb.Id] + nb.DV[i]);
                if(DV[i] > (DV[nb.Id] + nb.DV[i])){
                    DV[i] = (DV[nb.Id] + nb.DV[i]);
                    next_hop[i] = nb.Id;
                    changed = true;
                }
            }
        }
    }

}
