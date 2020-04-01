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