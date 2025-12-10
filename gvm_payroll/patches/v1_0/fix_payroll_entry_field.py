"""
Quick fix script to add missing field to Payroll Entry
Run this on the server: bench --site <site-name> execute gvm_payroll.patches.v1_0.fix_payroll_entry_field.execute
"""
import frappe


@frappe.whitelist()
def execute():
	"""Add missing field to Payroll Entry if it doesn't exist"""
	try:
		# Check if field exists in DocType meta
		meta = frappe.get_meta("Payroll Entry")
		field_exists = meta.has_field("deduct_tax_for_unclaimed_employee_benefits")
		
		if not field_exists:
			# Check if custom field exists
			custom_field_exists = frappe.db.exists(
				"Custom Field",
				{"dt": "Payroll Entry", "fieldname": "deduct_tax_for_unclaimed_employee_benefits"}
			)
			
			if not custom_field_exists:
				custom_field = frappe.get_doc({
					"doctype": "Custom Field",
					"dt": "Payroll Entry",
					"label": "Deduct Tax for Unclaimed Employee Benefits",
					"fieldname": "deduct_tax_for_unclaimed_employee_benefits",
					"fieldtype": "Check",
					"default": "0",
					"insert_after": "deduct_tax_for_unsubmitted_tax_exemption_proof",
				})
				custom_field.insert(ignore_permissions=True)
				frappe.db.commit()
			
			# Reload the DocType to ensure the field is accessible
			frappe.reload_doctype("Payroll Entry")
			frappe.clear_cache()
			
			return {"status": "success", "message": "Field added and DocType reloaded"}
		else:
			return {"status": "success", "message": "Field already exists"}
	except Exception as e:
		frappe.log_error(f"Error in fix_payroll_entry_field: {str(e)}", "fix_payroll_entry_field")
		return {"status": "error", "message": str(e)}

