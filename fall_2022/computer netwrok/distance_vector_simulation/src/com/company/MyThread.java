package com.company;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class MyThread implements Runnable{
    Router router;
    public MyThread(Router router){
        this.router = router;
    }

    @Override
    public void run(){
        System.out.println(router.Id);

    }
}
