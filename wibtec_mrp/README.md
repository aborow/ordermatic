Open ERP System :- Odoo 12E Version 

Installation 
============
Install the Application => Apps -> Wibtec Sales (Technical Name: wibtec_sales)

OMC-117
====================
-Work order kanban card colors based on status
-----------------------------------------------
Dark Blue - In Progress
Light Blue - Available / Ready
Yellow - Pending
Green - Finished

OMC-197 
===========
- Add Default Finished Good location to the Routing

OMC-169
===============
Update BOM view to show 150 records instead of 40 records.

OMC-198
========
Material Availability Change

Version - 12.0.1.0.1
======================
-Change color to kanban based on status.

Version - 12.0.1.0.2
====================
-Change card size for kanban and solved issue of overlapping.

Version - 12.0.1.0.3
====================
-Solved issue of click in kanban.

Version - 12.0.1.0.4
=====================
-Added "Default Finished Good Location" to the Routing.
-Added functionality that if the routing used in the MO has a “Finished products location”  then it should update the "Finsished Production Location" in the MO with this location.

Version - 12.0.1.0.5
====================
-Added functionality that BOM view should show 150 records instead of 40 records.

Version - 12.0.1.0.6
======================
-Added field "Available" to the  "Consume Material" one2many.

Version - 12.0.1.0.7
===================
-Added a functionality that expands all the boms with the childs.

Version - 12.0.1.0.8
===================
-Update Work Order with correct Time().
-Added field "Remaining Duration".
-Update "Remaining Duration" based "Quantity Produced".

Version - 12.0.1.0.9
===================
-Fix the issue of updating the effective end date.

Version - 12.0.1.0.10
======================
-Forcefully added "False" in settings so, MRP II do not get installed automatically.

Version - 12.0.1.0.11
=======================
-Added a functionality of leadtimes.
