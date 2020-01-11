package com.unbable.unbable_cli;

import com.unbable.unbable_cli.services.CalculatorService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.IOException;

@SpringBootApplication
@Slf4j
public class UnbableCliApplication implements ApplicationRunner {

	@Autowired
	private CalculatorService calculatorService;

	public static void main(String[] args) {
		SpringApplication.run(UnbableCliApplication.class, args);
	}

	@Override
	public void run(ApplicationArguments arguments) {
		try {
			calculatorService.generateAggregatedOutput(arguments);
			log.info("Output generated successfully");
		} catch (IOException exception) {
			log.error("Error running the app", exception);
		}
	}
}
