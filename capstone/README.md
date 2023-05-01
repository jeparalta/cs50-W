# MiniLogistic - a management tool for little enterprises

## Description

For this final project I wanted to build something that not only applies everything I've learned in this course but something that I could continue to work on and possibly put to good use. The name of the application is MiniLogistic and it helps property managers schedule cleans and check-ins for multiple properties. 

As my partner has a property management company and uses a very complex and cumbersome excel sheet system to keep on top of logistics regarding the cleaning and arrivals for all her properties, I thought I could try and help by making something that would simplify her job. 
This was also a great oportunity to build something for someone else, I asked her if I could review her existing system, interviewed her about what her ideal program would be like and have been checking in with her making sure the application the best fit possible. 

MiniLogistic is a very simple scheduling app, where you add properties you wish to manage and cleaners you work with. Then once these assets have been added, you can schedule cleans and bookings on an agenda that has two distinct views (list view and horizontal view). Once cleans and bookings are added these can be viewed and edited in a full day version with all relevant information for the property manager to organise their daily logistics.

## Distinctiveness and Complexity:

This final project borrows knowledge from the previous assignments, but I beleive it is very distinct and doesn't resemble in any way a social media or marketplace app. I decided to not use React and stick to just simple Javascript so that I could get a more solid foundation, this made the front-end code, in my optinion, fairly long and a bit verbose and confusing. I also chose to keep the javascript all in one file instead of spreading it out in separate files which maybe would have been wiser, especially if the app keeps getting more dynamic and complex. 

As this is a form of calendar scheduling app, with several ways to view the same data (List, Horizontal and Full page), the front end is where most of the complexity lies.
I also found the best approach to updating content when chenging dates, was to create separate html templates for the areas that the data gets updated, I also used this approach for the forms that get added asyncronasly when selected. This approach works but feels a bit dificult to stay on top of changes, as when I edit html on the main view I must also copy paste the new version to the separate template. I will definately be looking into alternatives to this approach, as this could get very unmanageable as the app gains more complexity.

Although I have preferred designing the back-end of the past projects, I tried to make the focus of this project the front-end, keeping the back-end very simple and spending the majority of the effort on making the app as dynamic and user friendly on the front-end. This is obviously a work in progress, but I feel that with a bit more time spent on this, it could actually become a helpful tool for my partner use in her business.

## Whats next?

I'm not sure this is part of the course requirement, but I just wanted to add that I will also use this project to explore how to deploy a web application. So once the Capstone requirment has been filled I will start researching into the best way to deploy and host this application cheaply as a pet project where I can continue to improve on it and my skills.

## Files:

- urls.py

The app has currently 20 urls. This feels like alot of urls compared to the previous projects and is mainly because of the way the diferent views get accessed for the forms. You'll notice that there is a url to add edit and delete each clean or booking and additionally to add or delete each comment within each clean or booking. This is why I mentioned above in Distinctiveness and Complexity that I felt this might not be the best design, and would further look into maybe changing it if possible.

Apart from these urls related to the forms, tthe rest are just the standard urls to manage user login, logout, register and rendering of diferent parts of the app.

- views.py

Just as there are many urls for forms, each of these has a view that gets accessed through it, this might be somewhere I can simplify into less urls to fiewer views that do a bit more in each. 

Besides the user authentication views we have three main views `agenda_view`, `settings_view` and `fullday_view` to access the main Agenda with several dates, the Full day page and the settings page. 

To update these pages asyncronasly we have an additional two views `fullday` and `days` that replace the data with new dates selected.

Within the the main Agenda page the user has the option to change the layout from vertical list to horizontal calendar, to make this change we use the `update_toggle` view that simply updates a model called `Selector` that keeps each users preferences. Depending on what the user has on his selector the HTML has a condition to display one format or the other.

- main.js

Once document is fully loaded, variables are assigned to the calender date pickers, toggle value from Selector model and container sections of the pages that can be updated asyncronasly.

For each calender picker I have a function that updates the container sections with the new dates and scheduled cleans/bookings.

Every time the date gets updated I re-apply all the event listeners to maintain functionality after sections by using the `createEventListeners()`function. This function applies event listeners for for the datepickers, but also applies event listeners along with functions for the remainder of the app.

Within this file you have functions to update asyncronasly the format of the main agenda page via the horizontal toggle, display and submit forms to create/edit/delete bookings and cleans plus some additional editing of assets by adding and deleting comments within themselves.

Aditionally I've also added a function `getCookie()` to help add the CSRF token to each request made asyncronasly.

- styles.css

For the styling of the appliction I used a combination of Bootstrap, Fontawesome and custom CSS. 
Within this stylesheet besides some visual styling of the elements of each page, I have also used some small forms of animation to make opening forms and making buttons appear/dissapear when needed.

- models.py

Regarding the user authentication models, you'll notice there is an `AccountUser` model and a `PermissionLevel`class that at the moment don't have much utility. This is in place as the next step will be to implement multiple accounts per user functionality and account share functionality with other users. This will allow the user to create accounts for specific properties and share these with collaborators (cleaners, contractors, location owners).
Ive also added a `Contractor` model because in the full day view There will be a "notes" section that can add maintanence jobs amongst other interventions. 
 
The `Cleaner`and `Contractor`models will also eventually have the hours assigned to them eventually trackable.

As mentioned above briefly the `Selector` model allows to store user preferences like how the prefer to view the agenda (horizontal or list), the last date selected so that the app stays on that date until changed and eventually more preferences like darkmode, language, etc...


## How to run this application:

Run command: python manage.py runserver

visit: http://127.0.0.1:8000/minilogistic/

1. Register as a new user.
2. Go to settings and add at least one location and one cleaner
3. Add and manage your cleans and bookings!

