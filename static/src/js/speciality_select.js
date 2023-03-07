odoo.define('clinic_appointment.booking', function (require) {
"use strict";
	
require('web.dom_ready');
var core = require('web.core');
var _t = core._t;


    var ajax = require('web.ajax');
    var time = require('web.time');
    // var Model = require('web.Model');
    var Dialog = require('web.Dialog');
    var formats = require('web.formats');
    var QWeb = core.qweb;
    
    
 
   $(document).ready(function() {
	   
	   var dt = new Date();
		var yyyy = dt.getFullYear().toString();
		var mm = (dt.getMonth() + 1).toString(); // getMonth() is
													// zero-based
		var dd = dt.getDate().toString();
		var min = yyyy + '-' + (mm[1] ? mm : "0" + mm[0]) + '-'
				+ (dd[1] ? dd : "0" + dd[0]); // padding
		$('#datepicker1').prop('min', min);
		
		
		
		
		
		
		
	   
	   if ($('#show_result').length ){
		   $('#show_result').text($('#dt_sel').val() + " | " + $('#spec_sel').val())
	   }
	   
	   if ($('#date_final').length ){
		   var text = $('#date_final').text()
		   text = $.trim(text);
		   var arr = text.split('/');
		   var dict = {
				   '01': "JAN",
				   '02': "FEB",
				   '03': "MAR",
				   '04': "APR",
				   '05': "MAY",
				   '06': "JUN",
				   '07': "JUL",
				   '08': "AUG",
				   '09': "SEP",
				   '10': "OCT",
				   '11': "NOV",
				   '12': "DEC",
				 };
		   text =  arr[1] + " " + dict[arr[0]] + " " + arr[2]
		   $('#date_final').text(text)
		   
		   
	   }
	   
//	   $("#select_box").click(function() {
//	   		alert()
//	   	});
	   
	   $('.box-time').click(function(e) { 
		   //original color #D7E3E4
		   //selected color #29F305
		   
		   $('.box-time').css('background','#D7E3E4')
		   $('.box-time').css('border-color','#D7E3E4')
		   
		   $(this).css('background','#29F305')
		   $(this).css('border-color','#29F305')
		   
		   var txt = $(e.target).text();
	   		txt = $.trim(txt);
	   		$('#box-time-selected').val(txt)
	   		
	   		//$('#book-btn').show()
	   		
	   		
	   		var data = $(this).parent().attr("data-id");
	   		$('[data-value=' + data + ']').show();
	   		
	   		var slot = $(this).attr("data-slot");
	   		$('#slot-selected').val(slot)
	   		
		    return false; 
		});
	   
	   $(".book-btn").click(function(e) {
	   		
	   		var data = $(this).attr("data-value");
	   		$('#phy-selected').val(data)
	   		$('form#doctor_form').submit();
	   		
	   	});
	   
	   
	   $("#confirm-btn").click(function(e) {
		   //Original color = #14addb
		   var err = false
		   if ($('#element_3').val() == ""){
			   $('#element_3').css({'border-color': '#FF0000'})
			   err = true
		   }
		   else{
			   $('#element_3').css({'border-color': '#14addb'})
		   }
		   
		   if ($('#element_1').val() == ""){
			   $('#element_1').css({'border-color': '#FF0000'})
			   err = true
		   }
		   else{
			   $('#element_1').css({'border-color': '#14addb'})
		   }
		   
		   if ($('#element_2').val() == ""){
			   $('#element_2').css({'border-color': '#FF0000'})
			   err = true
		   }
		   else{
			   $('#element_2').css({'border-color': '#14addb'})
		   }
		   
		   if ($('#element_4').val() == ""){
			   $('#element_4').css({'border-color': '#FF0000'})
			   err = true
		   }
		   else{
			   $('#element_4').css({'border-color': '#14addb'})
		   }
		   
			   
		   
		   if (err == false){
			   $('form#confirm_form').submit();
		   }
	   		
	   	});
	   
	   
	   
	   
	   $('.speciality_name').hover(
			    function(e){
			        $(this).css('color', 'red');
			        $(this).css('font-weight', 'bold');
			        e.preventDefault();
			        e.stopPropagation();
			        return false;
			    },function(e){
			    	$(this).css('color', 'black');
			        $(this).css('font-weight', 'normal');
			        e.preventDefault();
			        e.stopPropagation();
			        return false;
			    }
			);
	   
	   
	   
	   
	   
    	
    	var modal = $("#select_speciality");
    	var input = $("#speciality_input");
    	
    	$("#speciality_input").click(function() {
    		$("#dr_name_div").append(modal);
    		modal.show()
    	});
    	
//    	$(".modal-content").click(function(e) {
//    		var txt = $(e.target).parent().text();
//    		alert(txt);
//    		modal.hide()
//    	});
    	
    	$(".speciality_name").click(function(e) {
    		var txt = $(e.target).text();
    		txt = $.trim(txt);
    		$('#speciality_input').val(txt);
    		modal.hide()
    	});
    	
    	
    	$(".find").click(function(e) {
    		$(".find").css('background', '#dddddd');
    		$('#date_selected').val($('#datepicker1').val())
    		$('#spec_selected').val($('#id_select_spec').val())
    		$('#doc_selected').val($('#id_select_dr').val())
    		
    		$('form#search_form').submit();
    	});
    	
    	
    	$(".view-button").click(function(e) {
    		var data = $(this).attr("data-id");
    		console.log(data, 'DDDDDDDDDDDDDDDDDDDDDDDDdDDDDDDDDDDDDDDDD')
    		$('[data-id=' + data + ']').show();
    		
    		$('[data-name=' + data + ']').hide();
    		//$('[data-value=' + data + ']').show();
    		
    	});
    	$(".hide-button").click(function(e) {
//    		var data = $(this).attr("data-id");
//    		$('[data-id=' + data + ']').hide();
    		
//    		$('[data-value=' + data + ']').hide();
//    		

    	});
    	
    	
    	
    });
    	
    
    
    
    
    
    
    
    
    
    	
    	
    	
    });



