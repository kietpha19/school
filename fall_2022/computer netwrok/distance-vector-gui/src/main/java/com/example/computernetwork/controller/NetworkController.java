package com.example.computernetwork.controller;

import com.example.computernetwork.input.InputFile;
import com.example.computernetwork.model.Network;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.io.IOException;

@Controller
public class NetworkController {
	private static Network network;
	private final InputFile inputFile;

	@Autowired
	public NetworkController(InputFile inputFile) {
		this.inputFile = inputFile;
	}

	@GetMapping("/")
	public String listUploadedFiles(Model model) throws IOException {

//		model.addAttribute("files", storageService.loadAll().map(
//						path -> MvcUriComponentsBuilder.fromMethodName(FileUploadController.class,
//								"serveFile", path.getFileName().toString()).build().toUri().toString())
//				.collect(Collectors.toList()));

		return "uploadForm";
	}


//	@GetMapping("/network")
//	public String network(Model model) {
//		model.addAttribute("routers", network.getRoutersView());
//		return "network";
//	}
//
//	@PostMapping("/compute")
//	public String compute(Model model) {
//		network.compute();
//		return "compute";
//	}
}
