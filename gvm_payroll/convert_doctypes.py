import frappe


def convert_custom_to_standard(module: str = "Gvm Payroll", app_name: str = "gvm_payroll", names: list[str] | None = None) -> list[str]:
    """
    Turn Custom DocTypes in a module into Standard DocTypes so they are written to files.
    """
    if names is None:
        names = [d.name for d in frappe.get_all("DocType", filters={"module": module, "custom": 1})]

    converted = []
    for name in names:
        doc = frappe.get_doc("DocType", name)
        doc.custom = 0
        doc.module = module
        # app_name field exists on DocType in recent Frappe versions
        if hasattr(doc, "app_name"):
            doc.app_name = app_name
        doc.save()
        converted.append(name)

    return converted

