# Welcome to Seomi

## 🚀 Introducing Seom𝗶: A Powerful Open-Source SEO Analysis Tool 🕵️🔍

Ever wondered how your website could perform better in search engines? Well, wait no more! We are excited to present 𝗦𝗲𝗼𝗺𝗶, an all-in-one SEO analyzer that extracts vital data from web pages and stores it in a PostgreSQL database for further analysis. 📊

## 🔥 Seomi Features:
- ✅ Title, meta description, and headings analysis
- ✅ Internal and external link analysis
- ✅ URL, title, and meta description length
- ✅ Response time, status, and word count
- ✅ Page size and text ratio
- ✅ Canonical URL, meta robots, and image alt attributes
- ✅ Structured data, links, and language tags

## 🎓 Getting started:
- 1️⃣ Create a PostgreSQL database and table
- 2️⃣ Set up environment variables for your database credentials
- 3️⃣ Run the script by providing your sitemap URL

### 1: Create a PostgreSQL database and create a dedicated table:

```sql
CREATE TABLE seo_data (
    id SERIAL PRIMARY KEY,
    url VARCHAR(2083) NOT NULL,
    title VARCHAR(512),
    meta_description VARCHAR(512),
    h1 VARCHAR(512),
    h2 JSONB,
    internal_links JSONB,
    count_internal_links NUMERIC,
    external_links JSONB,
    count_external_links NUMERIC,
    url_length INTEGER,
    title_length INTEGER,
    meta_description_length INTEGER,
    h1_length INTEGER,
    h2_length JSONB,
    count_paragraphs INTEGER,
    response_time NUMERIC,
    status INTEGER,
    word_count INTEGER,
    page_size INTEGER,
    text_ratio NUMERIC,
    canonical_url VARCHAR(2083),
    meta_robots VARCHAR(256),
    meta_keyword VARCHAR(256),
    image_alt_attributes JSONB,
    structured_data JSONB,
    language_tags VARCHAR(32),
    timestamp TIMESTAMP,
    alert_missing_title BOOLEAN,
    alert_title_length BOOLEAN,
    alert_missing_meta_description BOOLEAN,
    alert_meta_description_length BOOLEAN,
    alert_missing_h1 BOOLEAN,
    alert_incorrect_canonical_url BOOLEAN,
    alert_missing_image_alt_attributes BOOLEAN,
    alert_missing_language_tag BOOLEAN,
    alert_low_text_ratio BOOLEAN,
    alert_no_meta_robots_or_incorrect_directives BOOLEAN,
    has_alert BOOLEAN
);
```

### 2: Set the environment variables for your database credentials.

```shell
export DB_USER=
export DB_PASSWORD=
export DB_HOST=
export DB_PORT=
export DB_NAME=postgres
```

### 3: Call the script passing your sitemap url

```shell
python seomi.py "https://valpiccola.com/sitemap.xml"

```

## Upcoming Features

1. Automatically flag fields with errors: DONE
2. Testing
3. Console recap
