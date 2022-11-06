package com.company;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;


public class Main {
    private static final int n = 7;
    private static final int max_cost = 10000;
    private static final ExecutorService thread_exe = Executors.newFixedThreadPool(100);

    public static void main(String[] args) throws IOException, InterruptedException {
        Scanner reader = new Scanner(System.in);
        System.out.print("Enter input file name: ");
        String input_fileName = reader.nextLine();

        int graph[][] = process_input_file(input_fileName);
        int num_router = get_num_router(graph);
        Map<Integer, Router> routers = init_routers(num_router, graph);
        print_network(routers);

        boolean stable = false;

        while(true){

            for(Router router : routers.values()){
                Runnable r = new MyThread(router);
                thread_exe.execute(r);
            }
           System.out.println(thread_exe.awaitTermination(3, TimeUnit.SECONDS));

            print_network(routers);
            //Thread.sleep(3000);
            stable = check_stable(routers);
            if(stable){
                System.out.println("pausing....");
                reader.nextLine();
            }

        }
    }

    //parse the input file and create a 2D array represent the network graph
    private static int[][] process_input_file(String input_fileName) throws FileNotFoundException {
        int graph[][] = new int[n][n];
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                graph[i][j] = max_cost;
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
        file_reader.close();
        return graph;
    }

    //check the graph to see how many routers are in the network
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

    //initialize all router in the network
    private static Map<Integer, Router> init_routers(int num_router, int[][] graph){
        Map<Integer, Router> routers = new HashMap<>();
        for(int i=1; i<=num_router; i++){
            int DV[] = new int[num_router+1];
            DV[0] = -2;
            for(int j=1; j<=num_router; j++){
                DV[j] = graph[i][j];
            }
            Router router = new Router(i, DV);
            routers.put(router.Id, router);
        }
        generate_neighbor(num_router, graph, routers );
        return routers;
    }

    //get all neighbors of each router
    private static void generate_neighbor(int num_router, int[][] graph, Map<Integer, Router> routers){
        for(int i =1; i<=num_router; i++){
            for(int j=1; j<=num_router; j++){
                if(graph[i][j] > 0 && graph[i][j] < max_cost){
                    Router nb = routers.get(j);
                    routers.get(i).neighbors.put(nb.Id, nb);
                }
            }
        }
    }

    //use to print the current state of the network (for debugging)
    private static void print_network(Map<Integer, Router> routers){
        for(Router router : routers.values()){
            System.out.println("router: " + router.Id);
            System.out.println("Distance vector");
            for(int i=1; i<router.DV.length; i++){
                System.out.println(i + ": " + router.DV[i] + ", next hop: " + router.next_hop[i]);
            }
            System.out.println("neighbor");
            for(Router nb : router.neighbors.values()){
                System.out.print(nb.Id + "\t");
            }
            System.out.println("\n-----------------------");
        }

    }

    //check if the network is stable
    private static boolean check_stable(Map<Integer, Router> routers){
        for(Router router : routers.values()){
            if(router.changed == true)
                return false;
        }
        return true;
    }
}
