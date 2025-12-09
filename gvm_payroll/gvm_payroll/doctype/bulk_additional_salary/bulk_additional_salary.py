# Copyright (c) 2025, Samuael Ketema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BulkAdditionalSalary(Document):
	pass


@frappe.whitelist()
def create_additional_salaries(docname: str):
	"""Create Additional Salary docs from Bulk Additional Salary rows."""
	doc = frappe.get_doc("Bulk Additional Salary", docname)

	if not doc.company or not doc.payroll_date:
		frappe.throw("Company and Payroll Date are required")

	if not doc.charges:
		frappe.throw("Please add at least one charge row")

	created = []
	for row in doc.charges:
		if not row.employee or not row.salary_component or row.amount is None:
			continue

		additional = frappe.get_doc(
			{
				"doctype": "Additional Salary",
				"naming_series": "HR-ADS-.YY.-.MM.-",
				"employee": row.employee,
				"salary_component": row.salary_component,
				"amount": row.amount,
				"company": doc.company,
				"payroll_date": doc.payroll_date,
				"overwrite_salary_structure_amount": 1,
				"ref_doctype": "Bulk Additional Salary",
				"ref_docname": doc.name,
			}
		)
		additional.insert()
		created.append(additional.name)

	return {"created": created}
