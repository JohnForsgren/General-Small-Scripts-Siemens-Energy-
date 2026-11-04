


## === UPDATE 1 ===
- Ensure that it can handle sub-folders so that it counts all pdfs, both directly in the target root folder and in subsequent folders under it. 

# ======= INITIAL PROMPT =======

PDF Page Counter - Basic description 

Essentially, I have been given a request for creating a simple application that counts the amont of PDF:s in the current file.



## The application

* Basically, the application should just tell basic statistics of the current folder, without cluttering the data. I am picturing: 

    * The user points the app to the folder
    * The Application tells the user info about the folder: 
        * To keep it simple, the  main info provided is simply: Amount of Documents, Total page count. 
        * There is a dropdown (or if it is a shell script, a de-emphasized section further down that is separated clearly from the main results) with additional information, such as a table with the document names, file sizes, individual page count. Potentially some other metadata is ok, but we dont want to make it cluttered. 

## The testings
- I will add some own pdfs here as text to see if the app is working. I also add a Docx; If it isnt too complicated, it should display data for this too. 

## The format

I am not sure if it should be an exe or a shell script, as there are pros and cons of both. As such, we should make both of them. 
They should be standalone so that you can just ship them as (ideally) a single file, or if required, a zip that is easy to unzip and run. 

* Exe-file: This is done in an enterprise firm, so in general, people might feel somewhat uncertain about using unknown .exe files. However, there is a case for making an exe as this allows the application to have a window, making it easy to use for people; this is relevant since lots of people might not be tech-savy. 
    * As such, the interface should look good, but easy to use and not cluttered with details (especially since it is made to be a straightforward app) but rather have nice quality of life features. For example, there is a clear "browse" button where the user can browse to select the folder. 


* Shell / script: Having an extension that isn't exe may make people more comfortable in using it as exe:s are associated iwth security risks.
    * Here, i am picturing that when the script is run, it simply displays the data for the current folder that the script is located in. 
    * The user is asked if the pdf:files to check are in the current folder from which the script is run. If yes, it prints the result, if no, the user is asked for the path and can copy and paste it. Ideally, it shouldn't require that the user pastes it with quotes (assuming this is feasible). 


## Original message 
From: Randmäe, Cecilia <cecilia.randmae@siemens-energy.com> 


Hej,
En liten fundering.

Går det att identifiera ett standardprojekt av lite nyare slag där vi har haft As Built leverans och få ut en förteckning över ingående dok plus antal sidor på doken från TPS?

Om det går är det önskvärt med en sån förteckning för varje maskintyp.


Det här skulle underlätta massor när det gäller sammanställning av underlag för offert i våra projekt med översättning.

Som det är nu är det väldigt svårt att ens gissa sig till ens hur många dok det handlar om.



