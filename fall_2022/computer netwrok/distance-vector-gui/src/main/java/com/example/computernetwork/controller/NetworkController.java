package com.example.computernetwork.controller;

import com.example.computernetwork.model.Network;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.io.FileNotFoundException;

@Controller
public class NetworkController {

	private static Network network;

	static {
		try {
			network = new Network();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	@GetMapping("/input")
	public String get_input_file(Model model){
		System.out.println("hello");

		return "input";
	}

	@GetMapping("/network")
	public String network(Model model) {
		model.addAttribute("routers", network.getRoutersView());
		return "network";
	}

	@PostMapping("/compute")
	public String compute(Model model) {
		network.compute();
		return "compute";
	}
}
