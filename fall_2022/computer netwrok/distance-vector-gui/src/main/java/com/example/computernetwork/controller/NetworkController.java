package com.example.computernetwork.controller;

import com.example.computernetwork.model.Network;
import com.sun.org.apache.xpath.internal.operations.Mod;
import org.apache.tomcat.util.http.fileupload.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;


@Controller
public class NetworkController {
	private static Network network = new Network();

	@GetMapping("/autoCompute")
	public String auto_compute(Model model) throws InterruptedException {
		network.compute();
		model.addAttribute("routers", network.getRoutersView());
		boolean stable = network.isStable();
		if(stable){
			model.addAttribute("message", "Network is stable!");
		}else{
			model.addAttribute("message", "Network is not stable!");
		}
		model.addAttribute("cycle", network.getCycle());
		model.addAttribute("auto_compute", true);
		model.addAttribute("is_stable", stable);
		return "network";
	}

	//process the input file
	@PostMapping(value = "/input")
	public String upload(@RequestParam(value = "file") MultipartFile file, Model model) throws IOException, InterruptedException {
		network.init_network(file.getInputStream());
		return "redirect:/";
	}

	//init network
	@GetMapping("/network")
	public String network(Model model) {
		model.addAttribute("routers", network.getRoutersView());
		network.isStable();
		if(network.isStable()){
			model.addAttribute("message", "Network is stable!");
		}else{
			model.addAttribute("message", "Network is not stable!");
		}
		model.addAttribute("cycle", network.getCycle());
		return "network";
	}

	//computer all routers in the network step by step
	@GetMapping("/compute")
	public String compute(Model model) throws InterruptedException {
		network.compute();
		return "redirect:/network";
	}

	//prompt user input if desire to change any link cost
	@GetMapping("/change")
	public String change_link_cost(){
		return "change_link_cost";
	}

	//process the data for changing link cost
	@PostMapping("/update_link")
	public String update_link(@RequestParam(value = "router1") int r1, @RequestParam(value = "router2") int r2,
							  @RequestParam(value = "cost") int cost) throws InterruptedException {
		network.update_link(r1, r2, cost);
		//network.compute();
		return "redirect:/network";
	}
}
