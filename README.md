# Lighthouse
A subscription renewals management and reminder system for IT professionals, service providers and even individual users/companies. Lighthouse can be used to manage customers, their details, products with cost and retail prices, and keep track of subscription/licence counts, renewal dates and pricing.


GitHub Repository: https://github.com/markcapelle/Lighthouse

GitHub Commits: https://github.com/markcapelle/Lighthouse/commits/main/

GitHub Project: https://github.com/users/markcapelle/projects/3

Readme.md: https://markcapelle.github.io/Lighthouse/

Render Deployment: https://lighthouse-lljr.onrender.com/


# Walkthrough

This document contains explanations on how to use all the features, and the sections are ordered in a way you can follow along to demonstrate all the features, from creating the users accessing the system through using each of the functions.

I advise having two separate browsers open (or one inprivate/incognito window) with separate sessions so one is logged in with your Lighthouse company admin, the other with a user.

If you only have one active email address available, I recommend setting up your administrator with a valid email.


# Creating New UserID

Users on-boarding is done in one two ways.

A new user with a new company/tenant.

A new user joining an existing company.


## New Company

When a new user is created with a new company, they automatically are enabled and become the administrator of that company, from where they can begin approving any new users joining the company.

On the Lighthouse home page, click ‘Register.’

Input all the important user detail. The email address doubles as the username.

Set ‘Registration Type’ to ‘Create New Company’

Give your new company a name.

Once you click ‘Register’ the new company will be created along with your userID with the administrator role for that new company. You’ll be able to access the ‘Manage Users’ interface to see all the other users in the company as they enrol themselves and approve or delete them.


## Existing Company

When a new user is created joining a company, they will not be able to login until an administrator has approved them.

On the Lighthouse home page, click ‘Register.’

Input all the important user detail. The email address doubles as the username.

Set ‘Registration Type’ to ‘Join Existing Company.’

Select the company you want to join from the drop down list.

Once registration is complete, wait for an administrator to activate your account before logging in.


## Approving a new user as Administrator

Logged into Lighthouse as an administrator, click your user icon at the top right and select ‘Manage Users.’ Here you can view, edit and delete all of the users in your company.

‘View’ will show whether the user is active or not.

Select ‘edit’ and complete the user profile. Select ‘active user’ and assign the user a role.

Once active, the user will be able to login.


# Forgotten Password

Any user that has forgotten their password can click on ‘forgot password’ on the login page.

There are two methods of resetting the password. The user can input their email address and have a password reset link sent to them. Or they can have the system send a notification to their company administrator for assistance.


## Self Service

The user inputs their email in the form and clicks ‘Send Reset Link.’

They will receive an email in their inbox shortly (be sure to check junk) with a link to reset their password to something new.

They can then login again.


## Admin Assistance

If the user does not have access to their email for whatever reason, they can input their email in the form and instead click ‘Contact Administrator.’

Lighthouse will send a message to all of your company admins informing them you need assistance with a password change. From here the administrator can use user management permissions to change your password and can contact you directly with the new password.


## Change Password at Next Login

The administrator is able to force users to change their password at next login by ticking the box on the change password form.

When the user has logged in with the temporary password, they will be denied access to any of Lighthouse’s features until they complete the password change prompt.


# User Roles


## Administrator

Administrator has full access to all features in Lighthouse. They can create, view, edit and delete Renewals/Products/Customers.

Administrators can view the archived Renewals.

They can also manage users in the company.


## User

User has access to all features in Lighthouse. They can create, view and edit Renewals/Products/Customers.

Users cannot delete Renewals/Products/Customers.

Users can close and archive Renewals.

Users can edit their own profile, but cannot access or edit any other users in the company.


# Features

The dashboard has a weekend weather report and will show any renewals that are 7 days out, urgent or overdue.


## Customers

On the Customers management page you can view all of the Customers.

Click ‘New Customer’ to create a new customer.

Once a new customer has been created, you can view the individual customer by clicking their name.

On the customer detailed view is an edit button, and all the renewals associated with that customer are viewable on the same page.

‘Edit’ allows you to change all the customer details, and delete the customer if needed.


## Products

On the Products management page you can view all of the Products.

Click ‘New Product’ to create a new product.

Once a new product has been created, you can view the individual product by clicking its name.

On the product detailed view is an edit button, and all the renewals associated with that product are viewable on the same page.

‘Edit’ allows you to change all the product details, and delete the customer if needed.


## Renewals

On the Renewals management page you can view all of the renewals and filter them by status, product and/or customer. The table can be sorted by clicking on the column header.

Renewals that are due in 7 days are highlighted in amber for attention.

Renewals that are due in 24 hours, or are over the renewal date are highlighted red for immediate attention.

Renewals come in below states to keep track of where in the process each renewal sits.

Open:
The renewal is pending action closer to the renewal date.

Quoted:
A quote has been issued to the customer for action.

For Invoicing:
The customer has approved, and the renewal is pending Accounts/Bookkeeping action to issue an invoice, check for payment, approve renewal purchase with the product supplier.

Closed:
Invoices are issued. Payment has been received. When setting a renewal to ‘closed’ and clicking save, the renewal is copied to the Archive for historical purposes. The renewal is then re-opened with the current start date and a new frequency/renewal date can be set.

Administrators can access the Archive table in a button under their user icon to the top right.

On the renewal view page is a button ‘Get Quote’ that will put a quotation for that renewal in the user’s clipboard so they can paste it into an email and forward to the customer.


# Deleting Renewals, Customers and Products

Renewals are intrinsically linked to Customers and Products, so be aware there are consequences to deleting any one.

Deleting a Renewal just removes it. Customers and Products attached to that Renewal remain in the system to be used elsewhere.

Deleting a Customer, deletes all of the Renewals attached to that Customer. Products are unaffected.

Deleting a Product deletes all of the Renewals attached to that Product. Customers are unaffected.

Walkthrough Note: there is a delete cascade test in renewals/tests/
