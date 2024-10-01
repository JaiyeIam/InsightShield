from jira import JIRA
import datetime
import os

# Jira server and authentication
jira_server = 'https://mthanshield.atlassian.net'
jira_user = 'iamtherealjai41@gmail.com'
jira_api_token = os.getenv('JIRA_API_TOKEN')  # Store the token in an environment variable

# Connect to Jira
try:
    jira = JIRA(server=jira_server, basic_auth=(jira_user, jira_api_token))
except Exception as e:
    print(f"Error connecting to Jira: {e}")
    exit(1)

# Create a new project
project_name = 'InsightShield'
project_key = 'ISHIELD'
project_lead = jira_user

# Start date of the project
start_date = datetime.date(2024, 7, 22)

# Calculate due dates based on project phases
def calculate_due_date(start_date, weeks):
    return start_date + datetime.timedelta(weeks=weeks)

# Function to create an epic
def create_epic(name, project_key, summary):
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': '',
        'issuetype': {'name': 'Epic'},
        'customfield_10011': name  # 'customfield_10011' is the default field for Epic Name
    }
    try:
        new_epic = jira.create_issue(fields=issue_dict)
        return new_epic
    except Exception as e:
        print(f"Error creating epic {name}: {e}")
        return None

# Function to create a story
def create_story(epic_link, project_key, summary, assignee, duedate):
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': '',
        'issuetype': {'name': 'Story'},
        'customfield_10014': epic_link,  # 'customfield_10014' links the story to an epic
        'assignee': {'name': assignee},
        'duedate': duedate
    }
    try:
        new_story = jira.create_issue(fields=issue_dict)
        return new_story
    except Exception as e:
        print(f"Error creating story {summary}: {e}")
        return None

# Function to create a subtask
def create_subtask(story, project_key, summary):
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': '',
        'issuetype': {'name': 'Sub-task'},
        'parent': {'id': story.id}
    }
    try:
        new_subtask = jira.create_issue(fields=issue_dict)
        return new_subtask
    except Exception as e:
        print(f"Error creating subtask {summary}: {e}")
        return None

# Create epics, stories, and subtasks for each phase
epics = {
    "Research and Planning": ["Market Research", "Criteria and Specifications Definition"],
    "AI Development": ["Data Collection and Preparation", "AI Model Training"],
    "Website Development": ["Frontend Design and Development", "Backend Development and Integration"],
    "Testing and Deployment": ["Testing and Optimization", "Deployment and Launch"]
}

stories_subtasks = {
    "Market Research": [
        {"summary": "Analyze existing Quran reading and prayer time applications", "subtasks": ["Research top applications in the market", "Evaluate their features and user feedback"]},
        {"summary": "Research AI solutions for detecting hate speech", "subtasks": ["Identify AI tools and algorithms", "Assess their effectiveness and integration feasibility"]},
        {"summary": "Identify user needs", "subtasks": ["Conduct surveys and interviews with potential users", "Analyze the data to determine key user requirements"]}
    ],
    "Criteria and Specifications Definition": [
        {"summary": "Define evaluation criteria for applications", "subtasks": ["Develop a checklist of features and performance metrics"]},
        {"summary": "Establish functional and technical specifications", "subtasks": ["Outline the technical requirements", "Define user stories and acceptance criteria"]},
        {"summary": "Create a detailed project plan", "subtasks": ["Break down the project into phases and milestones"]}
    ],
    "Data Collection and Preparation": [
        {"summary": "Gather data on applications and online hate speech", "subtasks": ["Scrape data from social media and app stores", "Compile datasets from various sources"]},
        {"summary": "Clean and prepare data for model training", "subtasks": ["Remove duplicates and irrelevant information", "Normalize and format the data"]}
    ],
    "AI Model Training": [
        {"summary": "Develop machine learning algorithms for app analysis", "subtasks": ["Implement initial models using Python and relevant libraries", "Evaluate model performance"]},
        {"summary": "Train natural language processing models for hate speech detection", "subtasks": ["Use datasets to train NLP models", "Fine-tune hyperparameters for optimal performance"]},
        {"summary": "Test and validate models", "subtasks": ["Conduct cross-validation and test on separate datasets", "Adjust models based on performance metrics"]}
    ],
    "Frontend Design and Development": [
        {"summary": "Create UI/UX mockups and prototypes", "subtasks": ["Design wireframes and interactive prototypes"]},
        {"summary": "Develop the frontend using React/Vue.js", "subtasks": ["Implement designs into code", "Ensure responsiveness and accessibility"]}
    ],
    "Backend Development and Integration": [
        {"summary": "Develop the backend API with Node.js", "subtasks": ["Set up server and database structures"]},
        {"summary": "Integrate AI models into the backend", "subtasks": ["Connect AI services to the API endpoints"]},
        {"summary": "Connect frontend to backend", "subtasks": ["Ensure seamless data flow between frontend and backend"]}
    ],
    "Testing and Optimization": [
        {"summary": "Perform unit and functional tests", "subtasks": ["Write and run test cases for all components"]},
        {"summary": "Optimize application performance", "subtasks": ["Identify and fix performance bottlenecks"]},
        {"summary": "Bug fixing and user experience improvements", "subtasks": ["Address all reported issues"]}
    ],
    "Deployment and Launch": [
        {"summary": "Prepare for deployment on the production server", "subtasks": ["Configure deployment scripts and CI/CD pipelines"]},
        {"summary": "Officially launch the application and website", "subtasks": ["Announce the launch and ensure all services are live"]},
        {"summary": "Monitor performance post-launch and resolve issues", "subtasks": ["Set up monitoring tools", "Quickly address any emerging issues"]}
    ]
}

# Due dates
due_dates = {
    "Market Research": calculate_due_date(start_date, 2),
    "Criteria and Specifications Definition": calculate_due_date(start_date, 4),
    "Data Collection and Preparation": calculate_due_date(start_date, 8),
    "AI Model Training": calculate_due_date(start_date, 12),
    "Frontend Design and Development": calculate_due_date(start_date, 16),
    "Backend Development and Integration": calculate_due_date(start_date, 20),
    "Testing and Optimization": calculate_due_date(start_date, 24),
    "Deployment and Launch": calculate_due_date(start_date, 26)
}

# Create Epics and their respective stories and subtasks
for epic_name, stories in stories_subtasks.items():
    epic = create_epic(epic_name, project_key, epic_name)
    if epic:
        for story_info in stories:
            story = create_story(epic.key, project_key, story_info["summary"], jira_user, due_dates[epic_name])
            if story:
                for subtask_summary in story_info["subtasks"]:
                    create_subtask(story, project_key, subtask_summary)

print("Project setup complete.")
