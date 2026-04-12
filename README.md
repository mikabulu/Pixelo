# Pixelo

Pixelo is a social media platform built for animators and artists to share their creative work. Users can upload and share artwork, animations, GIFs and videos, organise their posts with tags, and connect with other creatives.

## Features

- **Media sharing** — supports images, GIFs and video uploads
- **User profiles** — each profile includes a gallery and portfolio section
- **Tag system** — posts can be tagged to organise work by project or theme. Selecting a tag on a profile filters all posts with that tag, creating a chronological timeline of progress on a given project
- **Social interactions** — liking, commenting and following other users
- **Hashtags** — posts can be discovered through hashtags
- **Explore page** — surfaces content using item-based collaborative filtering with Jaccard similarity, analysing relationships between posts to generate recommendations
- **User matching** — discover and connect with other animators and artists with similar interests
- **Authentication** — user registration and login
- **Pagination** — smooth scrolling through posts and feeds
- **Responsive design** — works across different screen sizes

## Tech Stack

- **Frontend:** Vue.js, Tailwind CSS
- **Backend:** Django, Django REST Framework
- **Database:** SQLite
- **Version Control:** Git/GitHub

## Getting Started

**Prerequisites:** Python 3, pip, Node.js

### Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be running at `http://localhost:5173`
