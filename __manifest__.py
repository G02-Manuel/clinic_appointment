{
    'name': 'Clinic - Website Appointments',
    'version': '12.0',
    'author': 'Simple Apps',
    'depends': ['website', 'base'],
    'data': [
            'data/website_calendar.xml',
             ],
"summary": "Website physician appointments, website appointment, patient appointment, medical, doctor appointments, book appointment, clinic, clinic appointment",
    'update_xml': [
                   'views/assets.xml',
                   'views/appointment_template.xml',
                   'views/res_company_view.xml',
                   'views/clinic_view.xml',
                   'security/website_security.xml',
                   'security/ir.model.access.csv',
                   ],
    'installable': True,
    'application': True,
    'auto_install': False,
"images": [
        "static/description/screen.png",
    ],
    "price": "29",
    "currency": "USD",
}

