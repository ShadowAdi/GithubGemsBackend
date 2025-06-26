💎 GitHubGems (Backend)

GitHubGems is a backend API for a platform where users can discover, share, and discuss hidden gems on GitHub — fun, interactive, and underrated repositories.

Users can:

🔐 Create accounts and log in

🚀 Post cool repos (not just their own)

🏷️ Tag and categorize them (e.g. game, cli, visual, learning)

💬 Talk about what makes the repo unique

💎 Help others find creative, overlooked GitHub projects

⚙️ Tech Stack

FastAPI – High-performance Python web framework

SQLAlchemy – ORM for modeling and database operations

PostgreSQL (Neon) – Scalable, cloud-based relational DB

Pydantic – For request/response schema validation

Alembic – Database migrations

📦 Features (Backend)

User registration & login (JWT-based)

Post a GitHub repo with title, description, tags, and link

Add metadata (creator, why it’s interesting, category)

Like/bookmark repos

Comment and discuss

Tag-based filtering and search

🛠️ Setup Instructions

Clone the repo

git clone [https://github.com/yourusername/githubgems_backend.git](https://github.com/ShadowAdi/GithubGemsBackend)
cd githubgems_backend

Create a virtual environment & activate it

python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate

Install dependencies

pip install -r requirements.txt

Set up .envCreate a .env file with your DB and JWT config:

DATABASE_URL=postgresql+psycopg2://user:password@host:port/dbname
SECRET_KEY=your_jwt_secret

Run migrations


Start the server

🤝 Contributing

Feel free to open issues or submit PRs if you have ideas or want to improve the API.
