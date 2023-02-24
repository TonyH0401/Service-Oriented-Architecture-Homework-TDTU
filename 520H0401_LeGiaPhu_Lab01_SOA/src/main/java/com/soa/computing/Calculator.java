package com.soa.computing;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.*;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import java.text.SimpleDateFormat;  
import java.util.*;

// extra imports
import org.joda.time.*;
import org.joda.time.format.*;

@Path("/calculator")
public class Calculator {
	
	@GET
	@Path("/compute-interest/{month}/{deposit}/")
	@Produces(MediaType.TEXT_PLAIN)
	public double computeInterests(@PathParam("deposit") double deposit, @PathParam("month") int month)
	{
		double interestRate = 0.073;
		double output = deposit * (double) month * (interestRate/12.0);
		return output;
	}
	
	@GET
	@Path("/getdatetime/")
	@Produces(MediaType.TEXT_PLAIN)
	public String getDateTime()
	{
		SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
		Date date = new Date();
		String output = formatter.format(date).toString();
		return output;
	}
	
	@POST
	@Path("/create-student-instance/")
	@Consumes(MediaType.APPLICATION_JSON)
	public Response createStudentInstance(Student s)
	{
		if(s == null) {
			return Response.serverError().entity("Student object cannot be NULL.").build();
		}
		
		System.out.println(s.toString());

		return Response.status(200).entity("Student object has been successfully created.").build();
	}
	
//	-----------------------------------------EXERCISE 1:
	@GET
	@Path("/getdatetime/{region}/{city}/")
	@Produces(MediaType.TEXT_PLAIN)
	public String getDateTime(@PathParam("region") String region, @PathParam("city") String city) {
		String zoneString = region.trim() + "/" + city.trim();
		Set<String> timeZoneSet = DateTimeZone.getAvailableIDs();
		boolean containTimeZone = (timeZoneSet.contains(zoneString) == true) ? true : false;
		
		if(containTimeZone == true) {
		    DateTime dt = new DateTime();
		    DateTime dtTime = dt.withZone(DateTimeZone.forID(zoneString));
			DateTimeFormatter dtfOut = DateTimeFormat.forPattern("dd/MM/yyyy HH:mm:ss");
			return dtfOut.print(dtTime).toString();
		} else {
			return String.valueOf(containTimeZone) + ", there are no ID with: " + zoneString;
		}
	}

	@GET
	@Path("/getdatetime/{region}/{city}/{city2}")
	@Produces(MediaType.TEXT_PLAIN)
	public String getDateTime(@PathParam("region") String region, @PathParam("city") String city, @PathParam("city2") String city2) {
		String zoneString = region.trim() + "/" + city.trim() + "/" + city2.trim();
		Set<String> timeZoneSet = DateTimeZone.getAvailableIDs();
		boolean containTimeZone = (timeZoneSet.contains(zoneString) == true) ? true : false;
		
		if(containTimeZone == true) {
		    DateTime dt = new DateTime();
		    DateTime dtTime = dt.withZone(DateTimeZone.forID(zoneString));
			DateTimeFormatter dtfOut = DateTimeFormat.forPattern("dd/MM/yyyy HH:mm:ss");
			return dtfOut.print(dtTime).toString();
		} else {
			return String.valueOf(containTimeZone) + ", there are no ID with: " + zoneString;
		}
	}
//	-----------------------------------------EXERCISE 2:
	private static ArrayList<Student> studentList = new ArrayList<Student>();
	@GET
	@Path("/students/get-student-amount/")
	@Produces(MediaType.TEXT_PLAIN)
	public int getTotalStudent() {
		return studentList.size();
	}
	
	@GET
	@Path("/students/get-student-by-id/{studentId}")
	@Produces(MediaType.APPLICATION_JSON)
	public Student getStudentById(@PathParam("studentId") String studentId) {
		if(studentList.size() != 0) {
			for (Student n : studentList) {
				if(n.getId().equals(studentId) == true) {
					return n;
				}
			}
		}
		return new Student();
	}
	
	@POST
	@Path("/students/create-student-instance/")
	@Consumes(MediaType.APPLICATION_JSON)
	public Response createStudentInstance_2(Student s)
	{
		if(s == null) {
			return Response.serverError().entity("Student object cannot be NULL.").build();
		}
		if(studentList.size() != 0) {
			for(Student n : studentList) {
				if(n.compare(s) == true) {
					return Response.status(510).entity("Student object has already been created.").build();
				}
			}
		}
		studentList.add(s);
		System.out.println(s.toString() + ", size: " + studentList.size());
		return Response.status(200).entity("Student object has been successfully created. All is clear.").build();
	}
	
//	-----------------------------------------EXERCISE 3:
	@PUT
	@Path("/students/changeGender/{id}/{gender}")
	@Produces(MediaType.APPLICATION_JSON)
	public Response changeGender(@PathParam("id") int id, @PathParam("gender") int gender)
	{
		if(studentList.size() != 0) {
			for(Student n : studentList) {
				if(n.getId().equals(Integer.toString(id)) == true) {
					n.setGender(gender);
					return Response.status(200).entity("Student object has been changed").build();
				}
			}
			return Response.status(500).entity("No student with that id").build();
		} else {
			return Response.status(500).entity("No student with that id").build();
		}
	}

}
