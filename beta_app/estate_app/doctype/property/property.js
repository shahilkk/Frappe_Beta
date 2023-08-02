// Copyright (c) 2023, admin and contributors
// For license information, please see license.txt
// !---------------------------------------------------------------------------------
// frappe.ui.form.on('Property', {
// 	refresh: function(frm) {
// 		// console.log(frm)
// 		frappe.prompt('Address', ({ value }) => {
// 			if(value){
// 				frm.set_value('address',value)
// 				frm.refresh_field('address')
// 				frappe.msgprint(__(`Address Field Updated with Value ${value}`))
// 			}
// 		})

// 	}
// });


// !---------------------------------------------------------------------------------

frappe.ui.form.on('Property', {
	setup:function(frm){
		
		// check aminuteies duplicate
		frm.check_amenity_duplicate = function(frm,row){
			frm.doc.amenity.forEach(item=>{
				console.log(item,'item')
				if(row.amenity_name=='' || row.idx==item.idx){

				}
				else{
					if( row.amenity_name==item.amenity_name){
						row.amenity_name=''
						frm.refresh_field('amenity_name')
						frappe.throw(__(`${row.amenity_name} already exist row ${item.idx}`))
					}
				}
				// if(!row.amenity_name==''){
				// 	if(( row.amenity_name==item.amenity_name) && (!row.idx==item.idx)){
				// 		row.amenity_name=''
				// 		frm.refresh_field('amenity_name')
				// 		frappe.throw(__(`${row.amenity_name} already exist row ${item.idx}`))
				// 	}
				// }
				
			})
		}
	}

});

// *------------------------------------------------------------------------------------------------------------------

frappe.ui.form.on('Property Amenity Deatails', {
	amenity_name:function(frm,cdt,cdn){
		let row = locals[cdt][cdn];
		console.log(row,'row')
		frm.check_amenity_duplicate(frm,row)
	}
});

// *------------------------------------------------------------------------------------------------------------------