Open ERP System :- Odoo 12E Version 

Installation 
============
Install the Application => Apps -> Tax Exempt Solution for Customers(Technical Name: tax_exempt_solution)

OMC-141
============
Accounting: Tax Exempt Solution for Customers

Version - 12.0.1.0.1
=====================
-Added fields into the partner view.
-Added the functionality so that the user can mark a partner as “tax exempt” with a flag field and if the flag field “Tax Exempt” is checked than the system will update the tax lines to be Tax Exempt and not calculate a tax for any line items on the sales order or purchase order for the partner.
-Added functionality if the line shows “tax exempt” then it should not update taxes. 

Version - 12.0.1.0.2
=====================
-Solved a issue that taxcloud should not create a record if the tax is "exempt" in sale and purchase.

Version - 12.0.1.0.3
=====================
-Fix issue that taxcloud should not create a record if the tax is "exempt" in sale and purchase.

Version - 12.0.1.1.0(Added new featrue)
========================================
-Disable capture calls in Odoo to taxcloud (only lookup should work)
-Create Odoo export to comply with Odoo upload process template
(only import Taxable sales in the export)be able to run the report anytime in date range
-Check tax exempt functionality for company tax status and make sure it is working for tax exempt line items.

Version - 12.0.1.1.1
======================
-Solve issues for report upload.
-Changed customerid to internal reference of partner.

Version - 12.0.1.2.0
=====================
-Date Range filter for the report should be looking at the invoice VALIDATION date and not at the invoice CREATE date
-Do not include CANCELLED invoices, 
-Do not include DRAFT invoices
-Do not include NON TAX invoices (only invoices that have taxable amounts should be included in the report)
-Include Credit Notes (should be negative amount for Tax)
-Date Range filter for the report should be looking at the credit note VALIDATION date and not at the credit note CREATE date
-Do not include cancelled credit notes
-Do not include DRAFT credit notes
-There are several that are not showing up in the report that have something in the customer’s internal reference field for example, Not currently showing Braums BRA0003 Braums BRAUMS
-The Order ID column in the report should pull from the Invoice number, not the Odoo ID (Invoice # is much easier to find and reference)
-Fix Tax Exempt issue with Company, I marked a company “Tax exempt” and it still generated a tax amount for that company after adding a product with “Tax Cloud” as the default tax in the sales order line.  If the company is tax exempt than it should not generate taxable amount for any reason.

Version - 12.0.1.2.1
=====================
-Saprate the module for Sale Tax Report