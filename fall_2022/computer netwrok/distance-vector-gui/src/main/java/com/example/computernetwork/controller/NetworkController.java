package com.example.computernetwork.controller;

import com.example.computernetwork.input.InputFile;
import com.example.computernetwork.model.Network;
import org.apache.tomcat.util.http.fileupload.FileUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

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


	@PostMapping(value = "/input")
	public String upload(@RequestParam(value = "file") MultipartFile file) throws IOException, InterruptedException {
		network.init_network(file.getInputStream());

		return "redirect:/";
	}

	@GetMapping("/network")
	public String network(Model model) {
		model.addAttribute("routers", network.getRoutersView());
		return "network";
	}
//
//	@PostMapping("/compute")
//	public String compute(Model model) {
//		network.compute();
//		return "redirect:/network";
//	}
}
