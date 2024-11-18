from flask import Flask, render_template
import pandas as pd
from pymongo import MongoClient
import os
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from dotenv import load_dotenv

app = Flask(__name__)


# Get DataFrame from MongoDB collection
def get_df():
    load_dotenv()
    host = os.getenv("MONGO_HOST")
    database = os.getenv("MONGO_DB")
    collection = os.getenv("MONGO_COLLECTION")
    client = MongoClient(f"mongodb://localhost:{host}/")
    db = client[f"{database}"]
    coll = db[f"{collection}"]
    df = pd.DataFrame(list(coll.find()))
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    df_final = df.assign(description=df['description'].str.split(',')).explode('description')
    df_final['description'] = df_final['description'].str.strip()
    df_final.reset_index(drop=True, inplace=True)
    return df_final


# Helper to plot and encode graphs as images
def plot_to_image(plt_figure):
    img = BytesIO()
    plt_figure.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()


@app.route('/')
def home():
    # return ("Hard skills for tech jobs in Italy API Facade: use /data-engineer, /data-analyst, java-developer, "
    #         "salesforce-developer, microsoft-developer, cloud-specialist, system-cybersecurity")
    return render_template('home.html')


# Endpoint for card rarity distribution
@app.route('/data-engineer', methods=['GET'])
def data_engineer_skills():
    jobs = get_df()
    skills = jobs.loc[jobs['title'] == 'Data Engineer', 'description'].tolist()

    # Sort skills by count
    skill_counts = {skill: skills.count(skill) for skill in set(skills)}
    sorted_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)

    # Plotting
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.countplot(y=skills, order=sorted_skills, width=0.8, palette="flare")
    plt.title('Hard skills required for Data Engineers in Italy')
    plt.xlabel('Skill count')
    plt.ylabel('Skills')
    plt.yticks(fontsize=8)
    plt.subplots_adjust(bottom=0.25)
    plt.tight_layout()

    # Convert the plot to an image
    image = plot_to_image(plt)
    plt.close()

    # Return image as base64 string
    return f"<img src='data:image/png;base64,{image}'/>"


@app.route('/data-analyst', methods=['GET'])
def data_analyst_skills():
    jobs = get_df()
    skills = jobs.loc[jobs['title'] == 'Data Analyst', 'description'].tolist()

    # Sort skills by count
    skill_counts = {skill: skills.count(skill) for skill in set(skills)}
    sorted_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)

    # Plotting
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.countplot(y=skills, order=sorted_skills, width=0.8, palette="flare")
    plt.title('Hard skills required for Data Analysts in Italy')
    plt.xlabel('Skill count')
    plt.ylabel('Skills')
    plt.yticks(fontsize=8)
    plt.subplots_adjust(bottom=0.25)
    plt.tight_layout()

    # Convert the plot to an image
    image = plot_to_image(plt)
    plt.close()

    # Return image as base64 string
    return f"<img src='data:image/png;base64,{image}'/>"


@app.route('/java-developer', methods=['GET'])
def java_developer_skills():
    jobs = get_df()
    skills = jobs.loc[jobs['title'] == 'Java Developer', 'description'].tolist()

    # Sort skills by count
    skill_counts = {skill: skills.count(skill) for skill in set(skills)}
    sorted_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)

    # Plotting
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.countplot(y=skills, order=sorted_skills, width=0.8, palette="flare")
    plt.title('Hard skills required for Java Developers in Italy')
    plt.xlabel('Skill count')
    plt.ylabel('Skills')
    plt.yticks(fontsize=8)
    plt.subplots_adjust(bottom=0.25)
    plt.tight_layout()

    # Convert the plot to an image
    image = plot_to_image(plt)
    plt.close()

    # Return image as base64 string
    return f"<img src='data:image/png;base64,{image}'/>"


@app.route('/salesforce-developer', methods=['GET'])
def salesforce_developer_skills():
    jobs = get_df()
    skills = jobs.loc[jobs['title'] == 'Salesforce Developer', 'description'].tolist()

    # Sort skills by count
    skill_counts = {skill: skills.count(skill) for skill in set(skills)}
    sorted_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)

    # Plotting
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.countplot(y=skills, order=sorted_skills, width=0.8, palette="flare")
    plt.title('Hard skills required for Salesforce Developers in Italy')
    plt.xlabel('Skill count')
    plt.ylabel('Skills')
    plt.yticks(fontsize=8)
    plt.subplots_adjust(bottom=0.25)
    plt.tight_layout()

    # Convert the plot to an image
    image = plot_to_image(plt)
    plt.close()

    # Return image as base64 string
    return f"<img src='data:image/png;base64,{image}'/>"


@app.route('/microsoft-developer', methods=['GET'])
def microsoft_developer_skills():
    jobs = get_df()
    skills = jobs.loc[jobs['title'] == 'Microsoft Developer', 'description'].tolist()

    # Sort skills by count
    skill_counts = {skill: skills.count(skill) for skill in set(skills)}
    sorted_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)

    # Plotting
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.countplot(y=skills, order=sorted_skills, width=0.8, palette="flare")
    plt.title('Hard skills required for Microsoft Developers in Italy')
    plt.xlabel('Skill count')
    plt.ylabel('Skills')
    plt.yticks(fontsize=8)
    plt.subplots_adjust(bottom=0.25)
    plt.tight_layout()

    # Convert the plot to an image
    image = plot_to_image(plt)
    plt.close()

    # Return image as base64 string
    return f"<img src='data:image/png;base64,{image}'/>"


@app.route('/cloud-specialist', methods=['GET'])
def cloud_specialist_skills():
    jobs = get_df()
    skills = jobs.loc[jobs['title'] == 'Cloud Specialist', 'description'].tolist()

    # Sort skills by count
    skill_counts = {skill: skills.count(skill) for skill in set(skills)}
    sorted_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)

    # Plotting
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.countplot(y=skills, order=sorted_skills, width=0.8, palette="flare")
    plt.title('Hard skills required for Cloud Specialists in Italy')
    plt.xlabel('Skill count')
    plt.ylabel('Skills')
    plt.yticks(fontsize=8)
    plt.subplots_adjust(bottom=0.25)
    plt.tight_layout()

    # Convert the plot to an image
    image = plot_to_image(plt)
    plt.close()

    # Return image as base64 string
    return f"<img src='data:image/png;base64,{image}'/>"


@app.route('/system-cybersecurity', methods=['GET'])
def system_and_cybersecurity_skills():
    jobs = get_df()
    skills = jobs.loc[jobs['title'] == 'System and Cybersecurity', 'description'].tolist()

    # Sort skills by count
    skill_counts = {skill: skills.count(skill) for skill in set(skills)}
    sorted_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)

    # Plotting
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.countplot(y=skills, order=sorted_skills, width=0.8, palette="flare")
    plt.title('Hard skills required for System and Cybersecurity specialists in Italy')
    plt.xlabel('Skill count')
    plt.ylabel('Skills')
    plt.yticks(fontsize=8)
    plt.subplots_adjust(bottom=0.25)
    plt.tight_layout()

    # Convert the plot to an image
    image = plot_to_image(plt)
    plt.close()

    # Return image as base64 string
    return f"<img src='data:image/png;base64,{image}'/>"


if __name__ == '__main__':
    app.run(debug=True)
