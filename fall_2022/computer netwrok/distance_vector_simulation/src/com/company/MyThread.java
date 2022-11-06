package com.company;


public class MyThread implements Runnable{
    Router router;
    public MyThread(Router router){
        this.router = router;
    }

    @Override
    public void run(){
        long start = System.currentTimeMillis();
        System.out.println("router computing: " + router.Id);

        router.compute();

        long end = System.currentTimeMillis();
        System.out.println("finish computing for: " + router.Id + " time: " + (end-start));
    }
}
