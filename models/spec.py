# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, RedirectWarning, ValidationError

time_text = [('12:00 AM', '12:00 AM'), ('12:30 AM', '12:30 AM'), ('01:00 AM', '01:00 AM'), ('01:30 AM', '01:30 AM'),
             ('02:00 AM', '02:00 AM'), ('02:30 AM', '02:30 AM'), ('03:00 AM', '03:00 AM'), ('03:30 AM', '03:30 AM'),
             ('04:00 AM', '04:00 AM'), ('04:30 AM', '04:30 AM'), ('05:00 AM', '05:00 AM'), ('05:30 AM', '05:30 AM'),
             ('06:00 AM', '06:00 AM'), ('06:30 AM', '06:30 AM'), ('07:00 AM', '07:00 AM'), ('07:30 AM', '07:30 AM'),
             ('08:00 AM', '08:00 AM'), ('08:30 AM', '08:30 AM'), ('09:00 AM', '09:00 AM'), ('09:30 AM', '09:30 AM'),
             ('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'), ('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'),
             ('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'), ('01:00 PM', '01:00 PM'), ('01:30 PM', '01:30 PM'),
             ('02:00 PM', '02:00 PM'), ('02:30 PM', '02:30 PM'), ('03:00 PM', '03:00 PM'), ('03:30 PM', '03:30 PM'),
             ('04:00 PM', '04:00 PM'), ('04:30 PM', '04:30 PM'), ('05:00 PM', '05:00 PM'), ('05:30 PM', '05:30 PM'),
             ('06:00 PM', '06:00 PM'), ('06:30 PM', '06:30 PM'), ('07:00 PM', '07:00 PM'), ('07:30 PM', '07:30 PM'),
             ('08:00 PM', '08:00 PM'), ('08:30 PM', '08:30 PM'), ('09:00 PM', '09:00 PM'), ('09:30 PM', '09:30 PM'),
             ('10:00 PM', '10:00 PM'), ('10:30 PM', '10:30 PM'), ('11:00 PM', '11:00 PM'), ('11:30 PM', '11:30 PM')]
all_times123 = [('12:00 AM', '12:00 AM'), ('12:15 AM', '12:15 AM'), ('12:30 AM', '12:30 AM'), ('12:45 AM', '12:45 AM'),
                ('01:00 AM', '01:00 AM'), ('01:15 AM', '01:15 AM'), ('01:30 AM', '01:30 AM'), ('01:45 AM', '01:45 AM'),
                ('02:00 AM', '02:00 AM'), ('02:15 AM', '02:15 AM'), ('02:30 AM', '02:30 AM'), ('02:45 AM', '02:45 AM'),
                ('03:00 AM', '03:00 AM'), ('03:15 AM', '03:15 AM'), ('03:30 AM', '03:30 AM'), ('03:45 AM', '03:45 AM'),
                ('04:00 AM', '04:00 AM'), ('04:15 AM', '04:15 AM'), ('04:30 AM', '04:30 AM'), ('04:45 AM', '04:45 AM'),
                ('05:00 AM', '05:00 AM'), ('05:15 AM', '05:15 AM'), ('05:30 AM', '05:30 AM'), ('05:45 AM', '05:45 AM'),
                ('06:00 AM', '06:00 AM'), ('06:15 AM', '06:15 AM'), ('06:30 AM', '06:30 AM'), ('06:45 AM', '06:45 AM'),
                ('07:00 AM', '07:00 AM'), ('07:15 AM', '07:15 AM'), ('07:30 AM', '07:30 AM'), ('07:45 AM', '07:45 AM'),
                ('08:00 AM', '08:00 AM'), ('08:15 AM', '08:15 AM'), ('08:30 AM', '08:30 AM'), ('08:45 AM', '08:45 AM'),
                ('09:00 AM', '09:00 AM'), ('09:15 AM', '09:15 AM'), ('09:30 AM', '09:30 AM'), ('09:45 AM', '09:45 AM'),
                ('10:00 AM', '10:00 AM'), ('10:15 AM', '10:15 AM'), ('10:30 AM', '10:30 AM'), ('10:45 AM', '10:45 AM'),
                ('11:00 AM', '11:00 AM'), ('11:15 AM', '11:15 AM'), ('11:30 AM', '11:30 AM'), ('11:45 AM', '11:45 AM'),
                ('12:00 PM', '12:00 PM'), ('12:15 PM', '12:15 PM'), ('12:30 PM', '12:30 PM'), ('12:45 PM', '12:45 PM'),
                ('01:00 PM', '01:00 PM'), ('01:15 PM', '01:15 PM'), ('01:30 PM', '01:30 PM'), ('01:45 PM', '01:45 PM'),
                ('02:00 PM', '02:00 PM'), ('02:15 PM', '02:15 PM'), ('02:30 PM', '02:30 PM'), ('02:45 PM', '02:45 PM'),
                ('03:00 PM', '03:00 PM'), ('03:15 PM', '03:15 PM'), ('03:30 PM', '03:30 PM'), ('03:45 PM', '03:45 PM'),
                ('04:00 PM', '04:00 PM'), ('04:15 PM', '04:15 PM'), ('04:30 PM', '04:30 PM'), ('04:45 PM', '04:45 PM'),
                ('05:00 PM', '05:00 PM'), ('05:15 PM', '05:15 PM'), ('05:30 PM', '05:30 PM'), ('05:45 PM', '05:45 PM'),
                ('06:00 PM', '06:00 PM'), ('06:15 PM', '06:15 PM'), ('06:30 PM', '06:30 PM'), ('06:45 PM', '06:45 PM'),
                ('07:00 PM', '07:00 PM'), ('07:15 PM', '07:15 PM'), ('07:30 PM', '07:30 PM'), ('07:45 PM', '07:45 PM'),
                ('08:00 PM', '08:00 PM'), ('08:15 PM', '08:15 PM'), ('08:30 PM', '08:30 PM'), ('08:45 PM', '08:45 PM'),
                ('09:00 PM', '09:00 PM'), ('09:15 PM', '09:15 PM'), ('09:30 PM', '09:30 PM'), ('09:45 PM', '09:45 PM'),
                ('10:00 PM', '10:00 PM'), ('10:15 PM', '10:15 PM'), ('10:30 PM', '10:30 PM'), ('10:45 PM', '10:45 PM'),
                ('11:00 PM', '11:00 PM'), ('11:15 PM', '11:15 PM'), ('11:30 PM', '11:30 PM'), ('11:45 PM', '11:45 PM')]
all_times = ['12:00 AM', '12:15 AM', '12:30 AM', '12:45 AM', '01:00 AM', '01:15 AM', '01:30 AM', '01:45 AM', '02:00 AM',
             '02:15 AM', '02:30 AM', '02:45 AM', '03:00 AM', '03:15 AM', '03:30 AM', '03:45 AM', '04:00 AM', '04:15 AM',
             '04:30 AM', '04:45 AM', '05:00 AM', '05:15 AM', '05:30 AM', '05:45 AM', '06:00 AM', '06:15 AM', '06:30 AM',
             '06:45 AM', '07:00 AM', '07:15 AM', '07:30 AM', '07:45 AM', '08:00 AM', '08:15 AM', '08:30 AM', '08:45 AM',
             '09:00 AM', '09:15 AM', '09:30 AM', '09:45 AM', '10:00 AM', '10:15 AM', '10:30 AM', '10:45 AM', '11:00 AM',
             '11:15 AM', '11:30 AM', '11:45 AM', '12:00 PM', '12:15 PM', '12:30 PM', '12:45 PM', '01:00 PM', '01:15 PM',
             '01:30 PM', '01:45 PM', '02:00 PM', '02:15 PM', '02:30 PM', '02:45 PM', '03:00 PM', '03:15 PM', '03:30 PM',
             '03:45 PM', '04:00 PM', '04:15 PM', '04:30 PM', '04:45 PM', '05:00 PM', '05:15 PM', '05:30 PM', '05:45 PM',
             '06:00 PM', '06:15 PM', '06:30 PM', '06:45 PM', '07:00 PM', '07:15 PM', '07:30 PM', '07:45 PM', '08:00 PM',
             '08:15 PM', '08:30 PM', '08:45 PM', '09:00 PM', '09:15 PM', '09:30 PM', '09:45 PM', '10:00 PM', '10:15 PM',
             '10:30 PM', '10:45 PM', '11:00 PM', '11:15 PM', '11:30 PM', '11:45 PM']


class MedicalAppointmentDummy(models.Model):
    _name = "doc.appointment.temp"

    date = fields.Date("Date")
    start = fields.Char("Start Time")
    end = fields.Char("End Time")
    doctor = fields.Many2one('res.partner', 'Physician', help="Physician's Name")
    alloted = fields.Boolean('Alloted')
    slot = fields.Char('Slot')
    unique_id = fields.Char("Unique ID")
    schedule_id = fields.Many2one('doc.schedule')


class doc_schedule(models.Model):
    _name = "doc.schedule"

    @api.onchange('time_from')
    def onchange_time_from(self):
        print(self.time_from, '========================tf')
        to_list = []
        if self.time_from:
            check = 1
            add = 0
            for item in time_text:
                if item[0] == self.time_from and check:
                    add = 1
                    check = 0
                if add:
                    to_list.append(item)

    date = fields.Date("Date")
    time_from = fields.Selection(time_text, "From")
    time_to = fields.Selection(time_text, "To")
    slot = fields.Selection([('15', '15 Minuts'), ('30', 'Half Hour'), ('60', 'One Hour')], "Slot Time")
    doc_id = fields.Many2one('res.partner', string='Physician')

    def write(self, vals):

        res = super(doc_schedule, self).write(vals)
        for line in self:
            self.env['doc.appointment.temp'].search([('schedule_id', '=', line.id)]).unlink()

            start_time = line.time_from
            end_time = line.time_to
            temp_all_times = all_times

            idx = temp_all_times.index(start_time)
            temp_all_times = temp_all_times[idx:]

            idx = temp_all_times.index(end_time)
            temp_all_times = temp_all_times[:idx]

            i = 0
            rec = False
            print(temp_all_times)
            for item in temp_all_times:
                app_vals = {
                    'date': line.date,
                    'start': item,
                    'end': '',
                    'doctor': line.doc_id.id,
                    'alloted': False,
                    'slot': '15',
                    'schedule_id': line.id,
                }

                if line.slot == '15':
                    rec = self.env['doc.appointment.temp'].create(app_vals)

                if line.slot == '30':
                    app_vals.update({'slot': '30'})
                    if i % 2 == 0:
                        rec = self.env['doc.appointment.temp'].create(app_vals)

                if line.slot == '60':
                    app_vals.update({'slot': '60'})
                    if i == 0:
                        rec = self.env['doc.appointment.temp'].create(app_vals)
                    i += 1
                    if i == 4:
                        i = 0

                if len(self.env['doc.appointment.temp'].search(
                        [('date', '=', line.date), ('doctor', '=', line.doc_id.id), ('start', '=', item)]).ids) > 1:
                    raise ValidationError("Overlapping the slots!\n Some slots are already Scheduled")

        return res

    @api.model
    def create(self, vals):
        res = super(doc_schedule, self).create(vals)
        start_time = vals['time_from']
        end_time = vals['time_to']
        temp_all_times = all_times

        idx = temp_all_times.index(start_time)
        temp_all_times = temp_all_times[idx:]

        idx = temp_all_times.index(end_time)
        temp_all_times = temp_all_times[:idx]

        i = 0
        rec = False
        for item in temp_all_times:
            app_vals = {
                'date': vals['date'],
                'start': item,
                'end': '',
                'doctor': vals['doc_id'],
                'alloted': False,
                'slot': '15',
                'schedule_id': res.id,
            }

            if vals['slot'] == '15':
                app_vals.update({'slot': '15'})
                rec = self.env['doc.appointment.temp'].create(app_vals)

            if vals['slot'] == '30':
                app_vals.update({'slot': '30'})
                if i % 2 == 0:
                    rec = self.env['doc.appointment.temp'].create(app_vals)
                i += 1

            if vals['slot'] == '60':
                app_vals.update({'slot': '60'})
                if i == 0:
                    rec = self.env['doc.appointment.temp'].create(app_vals)
                i += 1
                if i == 4:
                    i = 0

            if len(self.env['doc.appointment.temp'].search(
                    [('date', '=', rec.date), ('doctor', '=', vals['doc_id']), ('start', '=', item)]).ids) > 1:
                raise ValidationError("Overlapping the slots!\n Some slots are already Scheduled")

        return res

    @api.multi
    def unlink(self):
        for item in self:
            self.env['doc.appointment.temp'].search([('schedule_id', '=', item.id)]).unlink()
        res = super(doc_schedule, self).unlink()


class partner(models.Model):
    _inherit = "res.partner"

    is_doctor = fields.Boolean("Doctor", default=False)
    is_patient = fields.Boolean("Patient", default=False)
    code = fields.Char('ID/Code', size=128, help="MD License ID")
    specialty_ids = fields.Many2one('spec.spec', string='Specialty')
    phy_description = fields.Html("description", readonly=False)

    schedule_ids = fields.One2many('doc.schedule', 'doc_id', 'Appointment Schedules')

    @api.model
    def create(self, vals):
        if 'is_patient' in self._context:
            vals['is_patient'] = True

        if 'is_doctor' in self._context:
            vals['is_doctor'] = True

        res = super(partner, self).create(vals)

        return res

    @api.model
    def default_get(self, fields):
        res = super(partner, self).default_get(fields)

        if 'is_doctor' in self._context:
            res['is_doctor'] = True

        return res


class spec(models.Model):
    _name = "spec.spec"

    name = fields.Char('Description', size=128, required=True, help="eg. Dentist, Surgeon")
    code = fields.Char('Code', size=128, )

    _sql_constraints = [
        ('code_uniq', 'unique (name)', 'Code must be unique')]


class NoteNote(models.Model):
    _name = "note.note"

    note_date = fields.Datetime('Time')
    note_text = fields.Text("Details")
    appoint_id = fields.Many2one('doc.appointment')


class MedicalAppointment(models.Model):
    _name = "doc.appointment"
    _order = "appointment_sdate desc"

    def do_confirm(self):
        for item in self:
            item.state = 'confirmed'

    def do_cancel(self):
        for item in self:
            item.state = 'cancel'
            self.env['doc.appointment.temp'].sudo().search([('unique_id', '=', item.name)]).alloted = False

    def do_done(self):
        for item in self:
            item.state = 'done'

    @api.model
    def _get_default_doctor(self):
        doc_ids = None
        partner_ids = self.env['res.partner'].search([('user_id', '=', self.env.user.id), ('is_doctor', '=', True)])
        if partner_ids:
            doc_ids = self.env['medical.physician'].search([('name', 'in', partner_ids)])
        return doc_ids

    doctor = fields.Many2one('res.partner', 'Physician', help="Physician's Name", domain=[('is_doctor', '=', True)],
                             default=_get_default_doctor)
    name = fields.Char('Appointment ID', size=64, readonly=True, default=lambda self: _('New'))
    patient = fields.Many2one('res.partner', 'Patient', help="Patient Name", required=True, )
    appointment_sdate = fields.Date('Appointment Date', required=True)
    app_time = fields.Selection(time_text, 'Appointment Time', required=True, )
    time_span = fields.Selection([('15', '15 Minuts'), ('30', 'Half Hour'), ('60', 'One Hour')], 'Time Span')
    speciality = fields.Many2one('spec.spec', 'Speciality', )
    urgency = fields.Selection([('a', 'Normal'), ('b', 'Urgent'), ('c', 'Medical Emergency'), ], 'Urgency Level',
                               default='a')
    comments = fields.Text('Comments')
    patient_status = fields.Selection(
        [('ambulatory', 'Ambulatory'), ('outpatient', 'Outpatient'), ('inpatient', 'Inpatient'), ], 'Patient status',
        default='ambulatory')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancel')],
                             'State', readonly="1", default='draft')

    note_ids = fields.One2many("note.note", 'appoint_id', string="Notes")

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    @api.onchange('doctor')
    def onchange_doctor(self):
        if self.doctor:
            self.speciality = self.doctor.specialty_ids.id

    def write(self, values):
        if 'appointment_sdate' in values:
            now = datetime.now()
            if values['appointment_sdate'] < str(now)[0:19]:
                raise ValidationError(_('Start of Appointment Date is back date.'))
        return super(MedicalAppointment, self).write(values)

    @api.model
    def create(self, vals):
        #		 for appointmnet in self:
        #			 now=datetime.now()
        #			 if vals['appointment_sdate'] < str(now)[0:19]:
        #				 raise ValidationError(_('Start of Appointment Date is back date.'))
        #			 if appointmnet.doctor.id==vals['doctor']:
        #
        #				 if appointmnet.appointment_sdate<=vals['appointment_sdate'] and vals['appointment_edate'] <=appointmnet.appointment_edate:
        #					 raise ValidationError(_('Appointment Overlapping.'))
        #
        #				 if appointmnet.appointment_sdate<=vals['appointment_sdate'] and appointmnet.appointment_edate>=vals['appointment_sdate'] :
        #					 raise ValidationError(_('Appointment Overlapping.'))
        #
        #				 if appointmnet.appointment_sdate<=vals['appointment_edate'] and appointmnet.appointment_edate>=vals['appointment_edate'] :
        #					 raise ValidationError(_('Appointment Overlapping.'))
        #
        #				 if appointmnet.appointment_sdate>=vals['appointment_sdate'] and appointmnet.appointment_edate<=vals['appointment_edate'] :
        #					 raise ValidationError(_('Appointment Overlapping.'))
        #
        #				 if vals['appointment_sdate']>=vals['appointment_edate']:
        #					 raise ValidationError(_('Start of Appointment Date is greater than End of Appointment Date.'))

        vals['name'] = self.env['ir.sequence'].next_by_code('doc.appointment') or 'New'

        result = super(MedicalAppointment, self).create(vals)

        self.env['doc.appointment.temp'].sudo().search(
            [('date', '=', result.appointment_sdate), ('start', '=', result.app_time),
             ('doctor', '=', result.doctor.id)]).alloted = True
        self.env['doc.appointment.temp'].sudo().search(
            [('date', '=', result.appointment_sdate), ('start', '=', result.app_time),
             ('doctor', '=', result.doctor.id)]).unique_id = result.name
        return result

