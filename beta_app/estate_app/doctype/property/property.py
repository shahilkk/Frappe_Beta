# Copyright (c) 2023, admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Property(Document):
	def validate(self):
		# frappe.throw((f'Hi  name <b>{self.property_name} <b>'))
		if (self.property_type=='Room Stay'):
			for amenity in self.amenity:
				if(amenity.amenity_name == 'Parking'):
					frappe.throw((f'property Type <b>Flat<b> Does Not have <b>amenity<b>   <b>{amenity.amenity_name} <b>'))

	pass
