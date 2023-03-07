# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, http
from odoo.http import request, Response
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import pytz
import werkzeug.utils
weekday_attendance_selection = ["Monday", "Tuesday", "Wednesday", "Thursday",
								"Friday", "Saturday", "Sunday"]

all_times = [('12:00 AM','12:00 AM'),('12:15 AM','12:15 AM'),('12:30 AM','12:30 AM'),('12:45 AM','12:45 AM'),('01:00 AM','01:00 AM'),('01:15 AM','01:15 AM'),('01:30 AM','01:30 AM'),('01:45 AM','01:45 AM'),('02:00 AM','02:00 AM'),('02:15 AM','02:15 AM'),('02:30 AM','02:30 AM'),('02:45 AM','02:45 AM'),('03:00 AM','03:00 AM'),('03:15 AM','03:15 AM'),('03:30 AM','03:30 AM'),('03:45 AM','03:45 AM'),('04:00 AM','04:00 AM'),('04:15 AM','04:15 AM'),('04:30 AM','04:30 AM'),('04:45 AM','04:45 AM'),('05:00 AM','05:00 AM'),('05:15 AM','05:15 AM'),('05:30 AM','05:30 AM'),('05:45 AM','05:45 AM'),('06:00 AM','06:00 AM'),('06:15 AM','06:15 AM'),('06:30 AM','06:30 AM'),('06:45 AM','06:45 AM'),('07:00 AM','07:00 AM'),('07:15 AM','07:15 AM'),('07:30 AM','07:30 AM'),('07:45 AM','07:45 AM'),('08:00 AM','08:00 AM'),('08:15 AM','08:15 AM'),('08:30 AM','08:30 AM'),('08:45 AM','08:45 AM'),('09:00 AM','09:00 AM'),('09:15 AM','09:15 AM'),('09:30 AM','09:30 AM'),('09:45 AM','09:45 AM'),('10:00 AM','10:00 AM'),('10:15 AM','10:15 AM'),('10:30 AM','10:30 AM'),('10:45 AM','10:45 AM'),('11:00 AM','11:00 AM'),('11:15 AM','11:15 AM'),('11:30 AM','11:30 AM'),('11:45 AM','11:45 AM'),('12:00 PM','12:00 PM'),('12:15 PM','12:15 PM'),('12:30 PM','12:30 PM'),('12:45 PM','12:45 PM'),('01:00 PM','01:00 PM'),('01:15 PM','01:15 PM'),('01:30 PM','01:30 PM'),('01:45 PM','01:45 PM'),('02:00 PM','02:00 PM'),('02:15 PM','02:15 PM'),('02:30 PM','02:30 PM'),('02:45 PM','02:45 PM'),('03:00 PM','03:00 PM'),('03:15 PM','03:15 PM'),('03:30 PM','03:30 PM'),('03:45 PM','03:45 PM'),('04:00 PM','04:00 PM'),('04:15 PM','04:15 PM'),('04:30 PM','04:30 PM'),('04:45 PM','04:45 PM'),('05:00 PM','05:00 PM'),('05:15 PM','05:15 PM'),('05:30 PM','05:30 PM'),('05:45 PM','05:45 PM'),('06:00 PM','06:00 PM'),('06:15 PM','06:15 PM'),('06:30 PM','06:30 PM'),('06:45 PM','06:45 PM'),('07:00 PM','07:00 PM'),('07:15 PM','07:15 PM'),('07:30 PM','07:30 PM'),('07:45 PM','07:45 PM'),('08:00 PM','08:00 PM'),('08:15 PM','08:15 PM'),('08:30 PM','08:30 PM'),('08:45 PM','08:45 PM'),('09:00 PM','09:00 PM'),('09:15 PM','09:15 PM'),('09:30 PM','09:30 PM'),('09:45 PM','09:45 PM'),('10:00 PM','10:00 PM'),('10:15 PM','10:15 PM'),('10:30 PM','10:30 PM'),('10:45 PM','10:45 PM'),('11:00 PM','11:00 PM'),('11:15 PM','11:15 PM'),('11:30 PM','11:30 PM'),('11:45 PM','11:45 PM')]


def _get_datetime_based_timezone(src_dt, context={}):
	dt = False
	if src_dt:
		timezone = pytz.timezone(request.env['res.users'].
								 sudo().browse([int(request.env.user)]).tz or 'UTC')
		dt = pytz.UTC.localize(fields.Datetime.from_string(src_dt))
		dt = dt.astimezone(timezone)
		dt = str(dt).split('+')[0]
	return dt

class WebsiteAppointment(http.Controller):

	
	def get_data_doctors(self, **kwargs):
		print (kwargs)
		print ('\n\nRRRRRRRRRRRRRRRRRRR===========================================\n\n\n\n')
		
		if 'edate' not in kwargs or ('edate' in kwargs and not kwargs['edate']):
			kwargs.update(
				{'physician_ids': [], 
				'specs': ",".join([]), 
				'times': [], 
				'selected_date': kwargs['edate'] if 'edate' in kwargs else '',
				'selected_spec': 0,
				'selected_doc': 0})
			
			return kwargs
		
		
		
		doc_ids = []
		specs = []
		times = []
		domain = [('is_doctor', '=', True)]
		if 'doc' in kwargs and kwargs['doc'] and kwargs['doc'] != '0':
			domain.append(('id', '=', int(kwargs['doc'])))
		if 'spec' in kwargs and  kwargs['spec'] and kwargs['spec'] != '0':
			domain.append(('specialty_ids', '=', int(kwargs['spec'])))
			
		print (domain, "DOMAINNNNNNNNNNNNNNNNNNN")
		
		physician_ids = request.env['res.partner'].sudo().search(domain) #or request.env['res.partner'].sudo().search([])
		print (physician_ids, 'PPPPPPPPPPPPPPPPPPPPPPPPPPP')
		specs = []
		for doc in physician_ids:
			specs.append(doc.specialty_ids.name)
			temp = []
			slot_found = False
			date_domain = [('doctor', '=', doc.id), ('alloted', '=', False)]
			if 'edate' in kwargs and  kwargs['edate']:
				date_domain.append(('date', '=', kwargs['edate']))
				
			print (date_domain, "DATE DOMAINNNNNNNNNNNNNNNNNNNNNNNNN")
			for item in request.env['doc.appointment.temp'].sudo().search(date_domain):
				slot_found = True
				print (item,'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
				temp = [doc.id, item.start, item.alloted, item.slot]
				times.append(temp)
				
			if slot_found == True:
				doc_ids.append(doc)
						
		print (specs, 'specsspecsspecs')
		kwargs.update(
			{'physician_ids': doc_ids, 
			#'specs': ",".join(specs), 
			'times': times, 
			'selected_date': kwargs['edate'] if 'edate' in kwargs else '',
			'selected_doc': kwargs['doc'] if 'doc' in kwargs else 0,
			'selected_spec': kwargs['spec'] if 'spec' in kwargs else 0})
		
			
			
		print (kwargs,'++++++++++++++++++=')
		
		return kwargs
		
		
	def get_data(self, **kwargs):
		
		print ('1111111111111111111111111111111a', kwargs)
		beauticians_book = {}

		beauticians = {}
		dropdown_services = {}
		dropdown_physiciance = {}
		dp_val = kwargs.get('cal_beutician')
		
		dt_val = False
		if not kwargs.get('cal_date'):
			dt_val = datetime.strftime(datetime.now(), '%m/%d/%Y')
		else:
			dt_val = kwargs.get('cal_date')
		
		
		speciality_ids = request.env['spec.spec'].sudo().search([])
			
			
		doctor_ids = request.env['res.partner'].sudo().search([('is_doctor', '=', True)])
#		 for physician in physicians_ids:
#			 dropdown_physiciance.update({physician.id: physician.name.name})
		
		return {
				'speciality_ids': speciality_ids,
				'doctor_ids': doctor_ids
				}
		
		
		
		
		
	@http.route(['/page/appointment'], auth='public',
				type='http', website=True, methods=['POST', 'GET'], csrf=False)
	def appointment(self, **kwargs):
		#		if not request.session.uid:
		#			return werkzeug.utils.redirect('/web/login', 303)
		print ("Success -------------------------------")
		value = self.get_data(**kwargs)
		return request.render(
			'clinic_appointment.selector_page', value
		)
		
		
	@http.route(['/page/show_doctors'], auth='public',
				type='http', website=True, methods=['POST', 'GET'], csrf=False)
	def show_doctors(self, **kwargs):
		
		print (kwargs, '\n\n\n\nKWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW\n\n\n\n\n')
		#		if not request.session.uid:
		#			return werkzeug.utils.redirect('/web/login', 303)
		value = self.get_data_doctors(**kwargs)
		
		print (value, 'V111111111111')
		value.update(self.get_data())
		print (value, 'V22222222222222222')
		
		print ("show doctors values", value)
		return request.render(
			'clinic_appointment.show_doctors_list', value
		)
		
		
	@http.route(['/page/book_appointment'], auth='public',
				type='http', website=True, methods=['POST', 'GET'], csrf=False)
	def book_appointment(self, **kwargs):
		#		if not request.session.uid:
		#			return werkzeug.utils.redirect('/web/login', 303)
		print (kwargs, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n\n\n\n')
		value = kwargs
		phy_id = request.env['res.partner'].sudo().search([('id', '=', value['phy-selected'])])
		value['physician'] = phy_id
		value['box_time_text'] = str(value['selected-box-name'])
		#value['date_selected'] = 2 
		print ("selected time and doctor details ------ \n", value)
		return request.render(
			'clinic_appointment.appointment_user_confirm', value
		)
		
		
		
	@http.route(['/page/confirm_appointment'], auth='public',
				type='http', website=True, methods=['POST', 'GET'], csrf=False)
	def confirm_appointment(self, **kwargs):
		#		if not request.session.uid:
		#			return werkzeug.utils.redirect('/web/login', 303)
		value = kwargs
		print ("user confirmed details ------ \n", value)
		
		import ast
		times = ast.literal_eval(value['times_selected2'])
		timespan = ''
		for item in times:
			if int(value['physician_id']) == item[0] and value['time'] == item[1] :
				timespan = item[3]
				break
				
			
			
		month = {
				 '01': 'Jan',
				 '02': 'Feb',
				 '03': 'Mar',
				 '04': 'Apr',
				 '05': 'May',
				 '06': 'Jun',
				 '07': 'Jul',
				 '08': 'Aug',
				 '09': 'Sep',
				 '10': 'Oct',
				 '11': 'Nov',
				 '12': 'Dec',
				 }
		
		d = value['date'].split('-')
		t = value['time'].replace(" ", "")
		d = "%s %s %s %s"%(month[str(d[1])], d[2], d[0], t)
		date1 = datetime.strptime(d, '%b %d %Y %I:%M%p')
		
		
		local = pytz.timezone (request.env['res.users'].
								 sudo().browse([1]).tz or 'UTC')
		naive = str(value['date'])+ ' ' +str(value['time'])[:5] + ':00' #datetime.strptime (date1.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
		
		naive = datetime.strptime(naive, '%Y-%m-%d %H:%M:%S')
		local_dt = local.localize(naive, is_dst=None)
		utc_dt = local_dt.astimezone(pytz.utc)
		utc_dt_end = utc_dt + timedelta(seconds=1800)
		print (d, utc_dt, 'KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK')



		
		patient_id = request.env['res.partner'].sudo().search([('email', '=', value['email'])])
		
		if not patient_id:
			patient_id = request.env['res.partner'].sudo().create({
															   'name': value['name'],
															   'company_type': 'person',
															   'email': value['email'],
															   'phone': value['phone'],
															   'mobile': value['phone'],
															   'ref': value['name'],
															   'is_patient': True,
															   })
		
#			 user_id = request.env['res.users'].sudo().create({
#														   'name': value['name'],
#														   'login': value['email'],
#														   'password': 'admin',
#														   'partner_id': partner_id.id,
#														   })
#			 patient_id = request.env['res.partner'].sudo().create({
#																	'name': partner_id.id,
#																	'sex': value['gender'],
#																	'marital_status': 's',
#																	})
		print (patient_id,'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP')
		pat_values = {
					  'patient_status': 'outpatient',
					  'urgency': 'a',
					  'state': 'draft',
					  'comments': value['desc'],
					  'patient': patient_id.id,
					  'doctor': value['physician_id'],
					  'appointment_sdate': utc_dt,
					  'app_time': value['time'],
					  'time_span': str(timespan),
					  #'time_span': request.env['spec.spec'].sudo().search([('name', '=', value['speciality_text'])]).id
					  }
		print (pat_values,'===================')
		appointment_id = request.env['doc.appointment'].sudo().create(pat_values)
		
		request.env['doc.appointment.temp'].sudo().search([('start', '=', value['time']), ('doctor', '=', int(value['physician_id']))]).alloted = True
		
		new_value = {'app_no': appointment_id.name}
		
		A = request.env['doc.appointment'].sudo().browse(appointment_id.id)
		
		send_user = request.env['res.users'].sudo().search([('partner_id', '=', appointment_id.doctor.id)])
		
		template = request.env.ref('clinic_appointment.ca_email', raise_if_not_found=False).sudo()
		body = """<div>Thank you for booking Appointment at %s.</div> <div>Find below Details-</div>
		<div>Appointment number: %s</div>
		<div>Date: %s</div>
		<div>Time: %s</div>
		<div>With: %s</div>""" % (send_user.company_id.name, A.name, A.appointment_sdate, A.app_time, A.doctor.name)

		
		
		print (request._context, 'CCCCCCCCCCCCCCCCCCCCC')
		template_values = {
			'email_to': kwargs['email'],
			'email_cc': False,
			'auto_delete': False,
			'partner_to': False,
			'scheduled_date': False,
			'subject': "Appointment Number",
			'body_html': body,
		}
		template.write(template_values)
		try:
			template.sudo().send_mail(send_user.id, force_send=False, raise_exception=False)
		except:
			print ("mail error")
		
		cron = request.env['ir.cron'].sudo().search([('name', '=', 'Mail: Email Queue Manager')])
		if cron:
			cron.method_direct_trigger()
		
		return request.render(
			'clinic_appointment.confirm_done', new_value
		)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

