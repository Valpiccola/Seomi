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
- ✅ Structured data, broken links, and language tags

## 🎓 Getting started:
- 1️⃣ Create a PostgreSQL database and table
- 2️⃣ Set up environment variables for your database credentials
- 3️⃣ Run the script by providing your sitemap URL

Built with Python, BeautifulSoup, and Requests, Seomi is designed to be user-friendly and efficient, providing you with a comprehensive set of metrics to analyze your website's SEO performance. 🐍🌐

## More infos

### Output
The seo_data table contains the following columns:

- **id**: A unique identifier for each record.
- **url**: The URL of the web page being analyzed.
- **title**: The title of the web page.
- **meta_description**: The meta description of the web page.
- **h1**: The first level heading of the web page.
- **h2**: A JSON object containing the text content of all second level headings.
- **internal_links**: A JSON object containing all internal links found on the web page.
- **external_links**: A JSON object containing all external links found on the web page.
- **url_length**: The length of the URL.
- **title_length**: The length of the title.
- **meta_description_length**: The length of the meta description.
- **h1_length**: The length of the first level heading.
- **h2_length**: A JSON object containing the length of each second level heading.
- **count_paragraphs**: The number of paragraphs on the web page.
- **response_time**: The time it took to receive a response from the web server.
- **status**: The HTTP status code of the web page.
- **word_count**: The total number of words on the web page.
- **page_size**: The size of the web page in bytes.
- **text_ratio**: The ratio of text content to total content on the web page.
- **canonical_url**: The canonical URL of the web page.
- **meta_robots**: The value of the meta robots tag of the web page.
- **image_alt_attributes**: A JSON object containing the alt attribute of all images on the web page.
- **structured_data**: A JSON object containing the structured data found on the web page.
- **broken_links**: A JSON object containing all broken links found on the web page.
- **language_tags**: The language tag of the web page.
- **timestamp**: The date and time the record was created.

## HOW TO

#### 1: Create a PostgreSQL database and create a dedicated table:

```sql
CREATE TABLE seo_data (
    id SERIAL PRIMARY KEY,
    url VARCHAR(2083) NOT NULL,
    title VARCHAR(512),
    meta_description VARCHAR(512),
    h1 VARCHAR(512),
    h2 JSONB,
    internal_links JSONB,
    external_links JSONB,
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
    image_alt_attributes JSONB,
    structured_data JSONB,
    broken_links JSONB,
    language_tags VARCHAR(32),
    timestamp TIMESTAMP
);
```

#### 2: Set the environment variables for your database credentials.

```shell
export DB_USER=
export DB_PASSWORD=
export DB_HOST=
export DB_PORT=
export DB_NAME=postgres
```

#### 3: Call the script passing your sitemap url

```shell
python seomi.py "https://valpiccola.com/sitemap.xml"

```


## Upcoming Features

1. Automatically flag fields with errors
