package com.company;
import java.io.BufferedReader;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

public class Main {
    private static final int n = 7;
    public static void main(String[] args) throws FileNotFoundException {
        Scanner reader = new Scanner(System.in);
        System.out.print("Enter input file name: ");
        String input_fileName = reader.nextLine();

        int graph[][] = process_input_file(input_fileName);
        int num_router = get_num_router(graph);
        Router routers[] = init_routers(num_router, graph);
    }

    //parse the input file and create a 2D array represent the network graph
    private static int[][] process_input_file(String input_fileName) throws FileNotFoundException {
        int graph[][] = new int[n][n];
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                graph[i][j] = -1;
            }
        }
        Scanner file_reader = new Scanner(new File(input_fileName));
        while(file_reader.hasNextLine()){
            String line = file_reader.nextLine();
            String[] input = line.split(" ");
            int r1 = Integer.parseInt(input[0]);
            int r2 = Integer.parseInt(input[1]);
            int r3 = Integer.parseInt(input[2]);
            graph[r1][r2] = r3;
            graph[r2][r1] = r3;
            graph[r1][r1] = 0;
            graph[r2][r2] = 0;
        }
        return graph;
    }

    //check the graph to see how many routers are in the netwrok
    private static int get_num_router(int[][] graph){
        int num_router = 0;
        for(int i= n-1 ;i > 0; i--){
            if(graph[i][i] == 0) {
                num_router = i;
                break;
            }
        }
        return num_router;
    }

    //parse the graph to initialize each router and store them into an array
    private static Router[] init_routers(int num_router, int[][] graph){
        Router routers[] = new Router[num_router+1];
        for(int i=1; i<=num_router; i++){
            int DV[] = new int[num_router+1];
            DV[0] = -2;
            ArrayList<Integer> neighbors = new ArrayList<Integer>();
            for(int j=1; j<=num_router; j++){
                DV[j] = graph[i][j];
                if(DV[j] > 0){
                    neighbors.add(j);
                }
            }
            routers[i] = new Router(i, DV, neighbors);
        }
        return routers;
    }

}
