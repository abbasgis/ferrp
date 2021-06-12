package com.flexmonster;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.flexmonster.compressor.Compressor;

public class FlexmonsterCompressor extends HttpServlet {

	private static final long serialVersionUID = -4997305985202070360L;
	
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
		try {
			Class.forName("com.mysql.jdbc.Driver").newInstance();
			Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/foodmart", "root", "password");
			String query = "SELECT * FROM customer";
			Statement statement = connection.createStatement();
			ResultSet resultSet = statement.executeQuery(query);
			
			InputStream inputStream = Compressor.compressDb(resultSet);
			
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