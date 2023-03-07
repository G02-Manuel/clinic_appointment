# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api
from odoo.tools import ustr
from odoo.exceptions import ValidationError



# class ProductTemplate(models.Model):
#	 _inherit = 'product.template'
# 
#	 duration = fields.Float(string='Service Time', default=0.50,
#							 help='Approximate time of Service')
#	 employee_ids = fields.Many2many('hr.employee',
#									 'hr_emp_product_product_rel',
#									 'product_id', 'emp_id', string='Employees',
#									 help='Beautician for the service')
#	 patch_test = fields.Boolean(string='Patch Test')
#	 is_creadit_product = fields.Boolean(
#		 string='Is Credit Product', default=False)
# 
#	 @api.model
#	 def default_get(self, fields):
#		 res = super(ProductTemplate, self).default_get(fields)
#		 if res:
#			 res['supplier_taxes_id'] = []
#		 return res
	
	
	
	
class WebMenu(models.Model):
	_inherit = 'website.menu'
	
	code = fields.Char("Code")
	
	@api.model
	def post_install_adjustment(self):
		self._cr.execute("update website_menu set parent_id=(select id from website_menu where code='clinic_base') where name='clinic_book';")

	
class ResCompany(models.Model):
	_inherit = 'res.company'

	start_time = fields.Float('Start Time', default=10.00)
	end_time = fields.Float('End Time', default=19.00)

	@api.constrains('start_time', 'end_time')
	def check_strat_time_end_time(self):
		for rec in self:
			if rec.start_time > 24 or rec.end_time > 24:
				raise ValidationError("you can not add more that 24 hour")
			st_time = (rec.start_time * 60)
			ed_time = (rec.end_time * 60)
			st_hours, st_minutes = divmod(st_time, 60)
			ed_hours, ed_minutes = divmod(ed_time, 60)
			st_minute = ustr(st_minutes).split('.', 1)[0]
			end_hour = ustr(ed_hours).split('.', 1)[0]
			end_minute = ustr(ed_minutes).split('.', 1)[0]
			if int(st_minute) % 15 != 0 or int(end_minute) % 15 != 0:
				raise ValidationError("Please add minutes in multiply of 15.")
			if int(end_hour) < int(st_hours):
				raise ValidationError("End Time can not be \
									  less than Start Time")
			if int(st_hours) == int(end_hour):
				raise ValidationError("Start time and End time \
				 can not be same")
