package com.company;

import java.util.ArrayList;

public class Router {
    int Id;
    int DV[];
    ArrayList<Router> neighbors = new ArrayList<>();


    Router(int Id, int distance_vector[]){
        this.Id = Id;
        this.DV = distance_vector;
    }

    public void compute(){
        for(int i=1; i< DV.length; i++){
            for(Router nb : neighbors){
                DV[i] = Math.min(DV[i], DV[nb.Id] + nb.DV[i]);
            }
        }
    }

}
