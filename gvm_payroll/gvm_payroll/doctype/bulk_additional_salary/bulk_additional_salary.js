// Copyright (c) 2025, Samuael Ketema and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Additional Salary", {
	refresh(frm) {
		if (!frm.doc.name) return;


		const btn = frm.page.add_button(__("Create Additional Salaries"), () =>
			create_bulk_additional_salary(frm)
		);
		if (btn) {
			$(btn).removeClass("btn-default btn-secondary btn-primary").addClass("btn-dark");
		}
	},
});

async function create_bulk_additional_salary(frm) {
    if (!frm.doc.company || !frm.doc.payroll_date) {
        frappe.msgprint({
            title: __("Missing Data"),
            message: __("Please set Company and Payroll Date before processing."),
            indicator: "orange",
        });
        return;
    }

    if (!frm.doc.charges || !frm.doc.charges.length) {
        frappe.msgprint({
            title: __("Missing Data"),
            message: __("Add at least one charge row to process."),
            indicator: "orange",
        });
        return;
    }

    try {
        await frappe.call({
            method: "gvm_payroll.gvm_payroll.doctype.bulk_additional_salary.bulk_additional_salary.create_additional_salaries",
            args: {
                docname: frm.doc.name,
            },
            freeze: true,
            freeze_message: __("Creating Additional Salaries..."),
        });
        frappe.msgprint(__("Additional Salary records created"));
    } catch (e) {
        console.error(e);
        frappe.msgprint({
            title: __("Error"),
            message: e.message || __("Could not create Additional Salaries"),
            indicator: "red",
        });
    }
}
