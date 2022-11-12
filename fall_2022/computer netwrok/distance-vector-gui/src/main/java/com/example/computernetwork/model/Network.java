package com.example.computernetwork.model;

import com.example.computernetwork.view.DvView;
import com.example.computernetwork.view.RouterView;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Network {
    private static final int n = 7;
    private static final int max_cost = 10000;
    private static final ExecutorService thread_exe = Executors.newFixedThreadPool(100);
    private Map<Integer, Router> allRouters = new HashMap<>();
    private int[][] graph = new int[n][n];

//    public Network() throws FileNotFoundException, InterruptedException {
//        init();
//    }

    public List<Router> getAllRoutes() {
        return new ArrayList<>(this.allRouters.values());
    }

    public void setAllRoutes(Map<Integer, Router> allRoutes) {
        this.allRouters = allRoutes;
    }

    //parse the input file and create a 2D array represent the network graph
    private void process_input_file(InputStream input_stream) throws FileNotFoundException {
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                graph[i][j] = max_cost;
            }
        }
        Scanner file_reader = new Scanner(input_stream);
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
    }

    //check the graph to see how many routers are in the network
    private int get_num_router(){
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
    private void init_routers(int num_router){
        for(int i=1; i<=num_router; i++){
            int DV[] = new int[num_router+1];
            DV[0] = -2;
            for(int j=1; j<=num_router; j++){
                DV[j] = graph[i][j];
            }
            Router router = new Router(i, DV);
            allRouters.put(router.getId(), router);
        }
        generate_neighbor(num_router );
    }

    //get all neighbors of each router
    private void generate_neighbor(int num_router){
        for(int i =1; i<=num_router; i++){
            for(int j=1; j<=num_router; j++){
                if(graph[i][j] > 0 && graph[i][j] < max_cost){
                    Router nb = allRouters.get(j);
                    allRouters.get(i).getNeighbors().put(nb.getId(), nb);
                }
            }
        }
    }

    //use to print the current state of the network (for debugging)
    private static void print_network(Map<Integer, Router> routers){
        for(Router router : routers.values()){
            System.out.println("router: " + router.getId());
            System.out.println("Distance vector");
            for(int i=1; i<router.getDv().length; i++){
                System.out.println(i + ": " + router.getDv()[i] + ", next hop: " + router.getNext_hop()[i]);
            }
            System.out.println("neighbor");
            for(Router nb : router.getNeighbors().values()){
                System.out.print(nb.getId() + "\t");
            }
            System.out.println("\n-----------------------");
        }

    }

    //check if the network is stable
    private static boolean check_stable(Map<Integer, Router> routers){
        for(Router router : routers.values()){
            if(router.isChanged() == true)
                return false;
        }
        return true;
    }

    /**
     *
     *
     */
//    public void compute() {
//        boolean stable = false;
//
//        while(true){
//            for(Router router : routers.values()){
//                Runnable r = new MyThread(router);
//                thread_exe.execute(r);
//            }
//            System.out.println(thread_exe.awaitTermination(3, TimeUnit.SECONDS));
//
//            print_network(routers);
//            //Thread.sleep(3000);
//            stable = check_stable(routers);
//            if(stable){
//                System.out.println("pausing....");
//                reader.nextLine();
//            }
//        }
//    }

    public void init_network(InputStream input_stream) throws InterruptedException, FileNotFoundException {
        Scanner reader = new Scanner(System.in);

        process_input_file(input_stream);
        int num_router = get_num_router();
        init_routers(num_router);
        //print_network(routers);
    }


    public List<RouterView> getRoutersView() {
        // TODO: convert the Router object to the RouteView object will represent the format on the UI
        List<RouterView> ret = new ArrayList<>();

        for (Router router : allRouters.values()) {
            RouterView routerView = new RouterView();
            routerView.setId(String.valueOf(router.getId()));
            List<DvView> DV_row = new ArrayList<>();
            for(int i=1; i<router.getDv().length; i++){
                DvView row = new DvView(String.valueOf(i), String.valueOf(router.getDv()[i]),
                        String.valueOf(router.getNext_hop()[i]));
                DV_row.add(row);
            }
            routerView.setDv_row(DV_row);
            String neighbor = router.getNeighbors().keySet().toString();
            routerView.setNeighbors(neighbor);
            ret.add(routerView);
        }
        return ret;
    }
}
