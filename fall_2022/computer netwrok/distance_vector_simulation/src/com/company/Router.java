package com.company;

import java.util.ArrayList;

public class Router {
    int Id;
    int DV[];
    ArrayList<Integer> neighbors;

    Router(int Id, int distance_vector[], ArrayList<Integer> neighbors){
        this.Id = Id;
        this.DV = distance_vector;
        this.neighbors = neighbors;
    }

}
