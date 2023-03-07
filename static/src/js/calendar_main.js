 odoo.define('website_beautician_calendar.calendar_main', function (require) {
"use strict";
	var core = require('web.core');
	var ajax = require('web.ajax')

	var _t = core._t;
	var qweb = core.qweb;
	var header = [];
	$(document).ready(function() {
		var tasks = [];
	    for (var i = 0; i < 20; i++) {
		    var startTime = -1;
		    var duration = 0.5;
		    for (var j = 0; j < 10; j++) {
		      if (Math.random() * 10 > 5) {
		        startTime += 0.5 + duration;
		      } else {
		        startTime += 1 + duration;
		      }

		      if (startTime > 23) {
		        break;
		      }

		      duration = Math.ceil(Math.random() * 2) + (Math.random() * 10 > 5 ? 0 : 0.5);

		      duration -= startTime + duration > 24 ? (startTime + duration) - 24 : 0;

		      var task = {
		        startTime: startTime,
		        duration: duration,
		        column: i,
		        id: Math.ceil(Math.random() * 100000),
		        title: 'Service ' + i + ' ' + j
		      };

		      tasks.push(task);
		    }
		  }
	      
		  ajax.jsonRpc("/get_booking_line", 'call', {}).done(function(data) {
			  var header_l = []
			  $.each(data, function(key, value) {
				  header_l.push(value);
			  });
			  header.push(header_l)
		  });
		  $("#skeduler-container").skeduler({
		    headers: header,
		    tasks: tasks,
		    cardTemplate: '<div>${id}</div><div>${title}</div>',
		    onClick: function (e, t) { console.log(e, t); }
		  });
	});
 });
