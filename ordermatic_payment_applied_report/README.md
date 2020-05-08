Open ERP System :- Odoo 12E Version 

Installation 
============
Install the Application => Apps -> Tax Exempt Solution for Customers(Technical Name: tax_exempt_solution)


Version - 12.0.1.1.0(Added new featrue)
========================================
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
-Added state filter in wizard
-Removed filter that was not allowing to display records that has 0 tax.
-Removed "Tax Excemption" functionality(as we are now going to use from avalara).

Version - 12.0.1.2.2
======================
-Added Tax Rate in Report.
-Added Discount and Suntotal in the report.
-Removed CaptureDate and AuthorizedDate.	
-Added Invoice payemt status in the report.
-Changed value of transaction date from create date to invoice date.
-Added account in the report.