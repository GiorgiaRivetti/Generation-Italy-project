INTRO
This project was born with two main goals in mind:
1. showing the most required hard skills for tech jobs in Italy (Data Engineer, Data Analyst, Cloud Specialist, Java Developer, Salesforce Developer, Microsoft Developer and Cybersecurity Analyst)
2. comparing the performances of different databases (MySQL, MongoDB and Firebase)

TOOLS: Serpapi, Python (dotenv, numpy, pandas, matplotlib, seaborn, pymongo, SQLAlchemy, flask), MySQL, Mongodb, Firebase, HTML

- In order for this program to work, you need to create a .env file with the following parameters: API_KEY, USERNAME_SQL, PASSWORD_SQL, SERVER (of Mysql), DB_NAME (of mysql),
MONGO_HOST, MONGO_DB, MONGO_COLLECTION. Put it in the .gitignore
  
ISSUES
- Limited number of data: the Serpapi free plan has a limited number of calls (100), which resulted in very few entries. As a consequence, the results and the final analysis are only superficial and give only a general idea about the real job market
- For the same reason, the performance analysis isn't significant, even though it's scalable

IDEAS TO IMPROVE/EXPAND THE PROJECT
- More data (quantity), either by choosing another Serpapi plan or by getting the data from different apis/sources (or both)
- More data (quality). For example, analysis on salaries could be included
- Changes in the structure. For example:  a. the "fetch_all_jobs" function in the "data_extractor" module isn't general enough, b. even though there is a "performance_test" directory, part of the performance analysis are in "loader"(etl->L->loader)
