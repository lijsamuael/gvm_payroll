# Copyright (c) 2025, Samuael Ketema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PayMatrix(Document):
	pass


@frappe.whitelist()
def update_pay_matrix_level(level_name, level, pay_band, grade, years_data):
	"""Update Pay Matrix Level with custom years data"""
	try:
		# Get the document
		doc = frappe.get_doc("Pay Matrix Level", level_name)
		
		# Update main fields
		doc.level = level
		doc.pay_band = pay_band or ""
		doc.grade = grade or ""
		
		# Clear existing years
		doc.years = []
		
		# Add new years
		if years_data:
			import json
			if isinstance(years_data, str):
				years_data = json.loads(years_data)
			
			for year_row in years_data:
				if year_row.get("year") and year_row.get("amount") is not None:
					doc.append("years", {
						"year": year_row["year"],
						"amount": year_row["amount"]
					})
		
		# Save the document
		doc.save()
		frappe.db.commit()
		
		return {"success": True, "message": "Pay Matrix Level updated successfully"}
	except Exception as e:
		frappe.log_error(f"Error updating Pay Matrix Level: {str(e)}")
		return {"success": False, "message": str(e)}
