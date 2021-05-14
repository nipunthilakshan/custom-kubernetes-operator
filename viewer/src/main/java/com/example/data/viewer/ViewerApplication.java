package com.example.data.viewer;

import com.example.data.viewer.config.RequestListener;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.ServletListenerRegistrationBean;
import org.springframework.context.annotation.Bean;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

import javax.servlet.ServletRequestListener;

@SpringBootApplication
@EnableSwagger2
public class ViewerApplication {

	public static void main(String[] args) {
		SpringApplication.run(ViewerApplication.class, args);
	}
	@Bean
	ServletListenerRegistrationBean<ServletRequestListener> ListenerRegistrationBean(){
		ServletListenerRegistrationBean beam = new ServletListenerRegistrationBean();
		beam.setListener(new RequestListener());
		return beam;
	}
}
