package com.flexmonster;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.flexmonster.compressor.Compressor;

public class FlexmonsterCompressor extends HttpServlet {

	private static final long serialVersionUID = -4997305985202070360L;
	
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
		try {
			String filePath = getServletContext().getRealPath("/WEB-INF/data.csv");
			InputStream inputStream = Compressor.compressFile(filePath);
			
			response.setContentType("text/plain");
			OutputStream outputStream = response.getOutputStream();
			int length = 0;
			byte[] buffer = new byte[10240];
			while ((length = inputStream.read(buffer)) > 0) {
				outputStream.write(buffer, 0, length);
				outputStream.flush();
		    }
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}