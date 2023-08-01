// Copyright (c) 2023, admin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Property', {
	refresh: function(frm) {
		// console.log(frm)
		frappe.prompt('Address', ({ value }) => {
			if(value){
				frm.set_value('address',value)
				frm.refresh_field('address')
				frappe.msgprint(__(`Address Field Updated with Value ${value}`))
			}
		})

	}
});
