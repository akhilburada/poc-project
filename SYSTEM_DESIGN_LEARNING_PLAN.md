# System Design Learning Plan for 2 YOE Candidates

> A structured 7-day roadmap to master system design for Associate/Junior SDE interviews

---

## Table of Contents

1. [What to Expect at 2 YOE Level](#what-to-expect-at-2-yoe-level)
2. [7-Day Learning Roadmap](#7-day-learning-roadmap)
3. [Core Concepts Deep Dive](#core-concepts-deep-dive)
4. [Interview Framework](#interview-framework)
5. [Common Interview Questions](#common-interview-questions)
6. [Practice Problems with Solutions](#practice-problems-with-solutions)
7. [Mistakes to Avoid](#mistakes-to-avoid)
8. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## What to Expect at 2 YOE Level

### Interview Expectations

At 2 years of experience, interviewers **DO NOT** expect you to:
- Design Netflix's entire architecture
- Know every distributed system concept
- Have deep expertise in databases or infrastructure

Interviewers **DO** expect you to:
- Understand basic building blocks (APIs, databases, caching)
- Break down a problem logically
- Ask clarifying questions
- Make reasonable trade-off decisions
- Communicate your thought process clearly

### Typical Question Scope

| Junior (2 YOE) | Senior (5+ YOE) |
|----------------|-----------------|
| URL Shortener | Distributed URL Shortener with analytics |
| Simple Chat App | WhatsApp-scale messaging |
| Basic Rate Limiter | Distributed rate limiting |
| Notification System | Multi-channel notification at scale |

---

## 7-Day Learning Roadmap

### Day 1: Fundamentals & APIs

**Morning (2-3 hours):**
- Client-Server Architecture
- HTTP/HTTPS basics
- REST API design principles
- Request/Response lifecycle

**Afternoon (2-3 hours):**
- API design best practices
- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Status codes (200, 201, 400, 401, 403, 404, 500)
- API versioning

**Practice:**
- Design APIs for a simple todo app
- Design APIs for a user registration system

---

### Day 2: Databases

**Morning (2-3 hours):**
- SQL vs NoSQL - when to use what
- ACID properties
- Database indexing basics
- Primary keys, foreign keys, relationships

**Afternoon (2-3 hours):**
- Database schema design
- Normalization basics (1NF, 2NF, 3NF)
- When to denormalize
- Common database choices (MySQL, PostgreSQL, MongoDB, Redis)

**Practice:**
- Design schema for an e-commerce product catalog
- Design schema for a social media posts system

---

### Day 3: Caching

**Morning (2-3 hours):**
- What is caching and why use it
- Cache hit vs cache miss
- Cache placement (client, CDN, server, database)
- Popular caching solutions (Redis, Memcached)

**Afternoon (2-3 hours):**
- Caching strategies:
  - Cache-aside (Lazy loading)
  - Write-through
  - Write-behind
  - Read-through
- Cache eviction policies (LRU, LFU, TTL)
- Cache invalidation challenges

**Practice:**
- Design caching strategy for a news website
- Identify what to cache in an e-commerce system

---

### Day 4: Load Balancing & Scaling

**Morning (2-3 hours):**
- Vertical vs Horizontal scaling
- Load balancer basics
- Load balancing algorithms:
  - Round Robin
  - Least Connections
  - IP Hash
  - Weighted Round Robin

**Afternoon (2-3 hours):**
- Stateless vs Stateful services
- Session management with load balancers
- Health checks
- Auto-scaling concepts

**Practice:**
- Explain how you'd scale a web application from 100 to 10,000 users
- Draw a basic load-balanced architecture

---

### Day 5: Message Queues & Async Processing

**Morning (2-3 hours):**
- Synchronous vs Asynchronous communication
- Why use message queues
- Popular message queues (RabbitMQ, Kafka, SQS)
- Producer-Consumer pattern

**Afternoon (2-3 hours):**
- Use cases for async processing:
  - Email sending
  - Image processing
  - Report generation
- Pub/Sub pattern
- Event-driven architecture basics

**Practice:**
- Design notification system using message queues
- Identify async use cases in an e-commerce order flow

---

### Day 6: System Design Framework & Practice

**Morning (2-3 hours):**
- Master the interview framework (see section below)
- Back-of-envelope calculations
- Capacity estimation basics
- Practice structured thinking

**Afternoon (3-4 hours):**
- Practice Problem 1: URL Shortener
- Practice Problem 2: Pastebin
- Review and refine answers

---

### Day 7: Advanced Topics & Mock Practice

**Morning (2-3 hours):**
- Database replication basics
- Database sharding concepts
- CAP theorem (understand, don't memorize)
- Consistency patterns (eventual vs strong)

**Afternoon (3-4 hours):**
- Practice Problem 3: Rate Limiter
- Practice Problem 4: Notification System
- Full mock interview simulation

---

## Core Concepts Deep Dive

### 1. APIs (Application Programming Interfaces)

#### REST API Design Principles

```
GET    /users          → List all users
GET    /users/{id}     → Get specific user
POST   /users          → Create new user
PUT    /users/{id}     → Update entire user
PATCH  /users/{id}     → Partial update
DELETE /users/{id}     → Delete user
```

#### Key Points for Interviews:
- Use nouns, not verbs in endpoints
- Use proper HTTP status codes
- Version your APIs (`/api/v1/users`)
- Support pagination for lists
- Use proper authentication (JWT, OAuth)

#### Example API Design:

**Design APIs for a Blog Platform:**

```
Posts:
GET    /api/v1/posts?page=1&limit=10    → List posts with pagination
GET    /api/v1/posts/{id}                → Get single post
POST   /api/v1/posts                     → Create post
PUT    /api/v1/posts/{id}                → Update post
DELETE /api/v1/posts/{id}                → Delete post

Comments:
GET    /api/v1/posts/{id}/comments       → Get comments for a post
POST   /api/v1/posts/{id}/comments       → Add comment to post

User:
GET    /api/v1/users/{id}/posts          → Get all posts by user
```

---

### 2. Database Design

#### SQL vs NoSQL Decision Guide

| Choose SQL When | Choose NoSQL When |
|-----------------|-------------------|
| Need ACID transactions | Flexible schema needed |
| Complex queries/joins | High write throughput |
| Data integrity is critical | Horizontal scaling priority |
| Structured data | Unstructured/semi-structured data |

**Examples:**
- User accounts → SQL (relationships, integrity)
- Product catalog → SQL (structured, relationships)
- User activity logs → NoSQL (high volume, simple queries)
- Session data → NoSQL/Redis (fast access, temporary)
- Chat messages → NoSQL (flexible, high volume)

#### Database Schema Example: E-commerce

```sql
-- Users table
CREATE TABLE users (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    email       VARCHAR(255) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    name        VARCHAR(100),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    price       DECIMAL(10,2) NOT NULL,
    stock       INT DEFAULT 0,
    category_id BIGINT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category_id),
    INDEX idx_price (price)
);

-- Orders table
CREATE TABLE orders (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id     BIGINT NOT NULL,
    total       DECIMAL(10,2) NOT NULL,
    status      ENUM('pending', 'paid', 'shipped', 'delivered') DEFAULT 'pending',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order items table
CREATE TABLE order_items (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id    BIGINT NOT NULL,
    product_id  BIGINT NOT NULL,
    quantity    INT NOT NULL,
    price       DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

#### Indexing Guidelines:
- Index columns used in WHERE clauses
- Index columns used in JOIN conditions
- Index columns used in ORDER BY
- Don't over-index (slows down writes)

---

### 3. Caching

#### Cache-Aside Pattern (Most Common)

```
Read Flow:
1. Application checks cache
2. If cache hit → return data
3. If cache miss → query database
4. Store result in cache
5. Return data

Write Flow:
1. Update database
2. Invalidate/update cache
```

#### What to Cache:
- Frequently accessed data (product details, user profiles)
- Expensive computations (aggregations, recommendations)
- Session data
- API responses

#### What NOT to Cache:
- Rapidly changing data
- User-specific sensitive data (without proper security)
- Data that must be real-time accurate

#### Redis Example Use Cases:

```
# Session storage
SET session:user123 "{user_data}" EX 3600

# Rate limiting
INCR requests:user123:minute
EXPIRE requests:user123:minute 60

# Leaderboard
ZADD leaderboard 1000 "player1"
ZREVRANGE leaderboard 0 9  # Top 10

# Caching
SET product:123 "{product_json}" EX 300
GET product:123
```

---

### 4. Load Balancing & Scaling

#### Horizontal vs Vertical Scaling

```
Vertical Scaling (Scale Up):
┌─────────────────┐
│   Bigger Server │
│   More CPU/RAM  │
└─────────────────┘
- Simpler to implement
- Has hardware limits
- Single point of failure

Horizontal Scaling (Scale Out):
┌────────┐ ┌────────┐ ┌────────┐
│Server 1│ │Server 2│ │Server 3│
└────────┘ └────────┘ └────────┘
- No hardware limit
- Requires load balancer
- More complex
- Better fault tolerance
```

#### Basic Load-Balanced Architecture

```
                    ┌─────────────┐
                    │   Clients   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │Load Balancer│
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │  Server 1   │ │  Server 2   │ │  Server 3   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    ┌──────▼──────┐
                    │   Database  │
                    └─────────────┘
```

#### Making Services Stateless

**Problem:** Server stores session data locally
**Solution:** Store session in shared cache (Redis)

```
Before (Stateful):
- User logs in to Server 1
- Session stored on Server 1
- Next request goes to Server 2
- User appears logged out ❌

After (Stateless):
- User logs in to Server 1
- Session stored in Redis
- Next request goes to Server 2
- Server 2 reads session from Redis ✓
```

---

### 5. Message Queues

#### When to Use Message Queues

1. **Time-consuming tasks:** Email, SMS, push notifications
2. **Batch processing:** Report generation, data exports
3. **Third-party integrations:** Payment processing, shipping
4. **Decoupling services:** Order → Inventory → Shipping

#### Basic Queue Architecture

```
┌──────────┐     ┌───────────┐     ┌──────────┐
│ Producer │────►│   Queue   │────►│ Consumer │
└──────────┘     └───────────┘     └──────────┘

Example: Order Processing
┌────────────┐     ┌───────────┐     ┌─────────────────┐
│Order Service│───►│Order Queue│───►│Inventory Service│
└────────────┘     └───────────┘     └─────────────────┘
                                              │
                                     ┌────────▼────────┐
                                     │Email Queue      │
                                     └────────┬────────┘
                                              │
                                     ┌────────▼────────┐
                                     │Email Service    │
                                     └─────────────────┘
```

#### Benefits:
- **Decoupling:** Services don't need to know about each other
- **Async processing:** Faster response to users
- **Reliability:** Messages persist even if consumer is down
- **Scalability:** Add more consumers to handle load

---

## Interview Framework

### The RADIO Framework (Recommended for 2 YOE)

Use this structure for every system design interview:

#### R - Requirements Clarification (3-5 minutes)

Ask these questions before designing:

**Functional Requirements:**
- What are the core features?
- Who are the users?
- What actions can users perform?

**Non-Functional Requirements:**
- Expected scale (users, requests/second)?
- Latency requirements?
- Availability requirements?
- Consistency requirements?

**Example for URL Shortener:**
```
"Before I start, let me clarify a few things:
1. Should URLs expire? If yes, what's the default TTL?
2. Do we need analytics (click counts)?
3. Can users create custom short URLs?
4. Expected scale - how many URLs per day?
5. Read-heavy or write-heavy?"
```

#### A - API Design (3-5 minutes)

Define the main APIs:

```
URL Shortener APIs:

POST /api/v1/urls
Request:  { "long_url": "https://...", "custom_alias": "my-link" }
Response: { "short_url": "https://short.ly/abc123", "expires_at": "..." }

GET /{short_code}
Response: 301 Redirect to original URL

GET /api/v1/urls/{short_code}/stats
Response: { "clicks": 1000, "created_at": "...", "long_url": "..." }
```

#### D - Data Model (5 minutes)

Design database schema:

```sql
-- For URL Shortener
CREATE TABLE urls (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code  VARCHAR(10) UNIQUE NOT NULL,
    long_url    TEXT NOT NULL,
    user_id     BIGINT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at  TIMESTAMP,
    click_count BIGINT DEFAULT 0,
    INDEX idx_short_code (short_code),
    INDEX idx_expires (expires_at)
);
```

#### I - High-Level Design (10 minutes)

Draw the architecture:

```
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│ Client  │────►│Load Balancer│────►│ API Servers │
└─────────┘     └─────────────┘     └──────┬──────┘
                                           │
                      ┌────────────────────┼────────────────────┐
                      │                    │                    │
               ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
               │    Cache    │      │  Database   │      │Key Generator│
               │   (Redis)   │      │   (MySQL)   │      │   Service   │
               └─────────────┘      └─────────────┘      └─────────────┘
```

#### O - Optimizations & Deep Dive (10 minutes)

Discuss trade-offs and improvements:

- **Caching strategy:** Cache popular URLs in Redis
- **Key generation:** Pre-generate keys vs generate on demand
- **Database choice:** SQL for consistency, consider sharding for scale
- **Analytics:** Use separate analytics service + message queue

---

### Back-of-Envelope Calculations

Basic numbers to remember:

```
1 day = 86,400 seconds ≈ 100,000 seconds
1 month ≈ 2.5 million seconds
1 year ≈ 30 million seconds

Storage:
1 KB = 1,000 bytes
1 MB = 1,000 KB
1 GB = 1,000 MB
1 TB = 1,000 GB

Latency:
Memory access: 100 nanoseconds
SSD read: 100 microseconds
Network (same datacenter): 500 microseconds
Network (cross-continent): 150 milliseconds
```

**Example Calculation for URL Shortener:**

```
Assumptions:
- 100 million URLs created per month
- Read:Write ratio = 100:1

Writes per second:
100M / (30 days × 24 hours × 3600 seconds)
= 100M / 2.5M seconds
≈ 40 writes/second

Reads per second:
40 × 100 = 4,000 reads/second

Storage (5 years):
- Each URL entry: ~500 bytes
- 100M URLs/month × 12 months × 5 years = 6 billion URLs
- 6B × 500 bytes = 3 TB
```

---

## Common Interview Questions

### Tier 1: Most Common for 2 YOE

1. **URL Shortener** (like bit.ly)
   - Difficulty: Easy
   - Focus: Basic system design, database, caching

2. **Pastebin / Text Sharing**
   - Difficulty: Easy
   - Focus: Similar to URL shortener with file storage

3. **Rate Limiter**
   - Difficulty: Easy-Medium
   - Focus: Algorithms, Redis, distributed systems intro

4. **Notification System**
   - Difficulty: Medium
   - Focus: Message queues, async processing

5. **Chat Application (1-on-1)**
   - Difficulty: Medium
   - Focus: WebSockets, message storage

### Tier 2: Sometimes Asked

6. **News Feed / Timeline**
   - Difficulty: Medium
   - Focus: Fan-out, caching, pagination

7. **File Storage System**
   - Difficulty: Medium
   - Focus: Object storage, metadata

8. **Parking Lot System**
   - Difficulty: Easy-Medium
   - Focus: OOP + basic system design

9. **Booking System** (movie tickets, appointments)
   - Difficulty: Medium
   - Focus: Concurrency, transactions

10. **Leaderboard System**
    - Difficulty: Medium
    - Focus: Redis sorted sets, real-time updates

---

## Practice Problems with Solutions

### Problem 1: Design a URL Shortener

#### Requirements:
- Shorten long URLs to short codes
- Redirect short URLs to original
- Optional: Analytics, expiration, custom aliases

#### Solution:

**1. Functional Requirements:**
- Create short URL from long URL
- Redirect to original URL
- URLs expire after configurable time

**2. API Design:**

```
POST /api/v1/shorten
{
  "long_url": "https://example.com/very/long/path",
  "custom_alias": "my-link",  // optional
  "expires_in": 86400         // optional, seconds
}
Response: { "short_url": "https://short.ly/abc123" }

GET /{short_code}
Response: 301 Redirect

GET /api/v1/urls/{short_code}/stats
Response: { "long_url": "...", "clicks": 100, "created_at": "..." }
```

**3. Database Schema:**

```sql
CREATE TABLE urls (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code  VARCHAR(7) UNIQUE NOT NULL,
    long_url    TEXT NOT NULL,
    user_id     BIGINT,
    clicks      BIGINT DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at  TIMESTAMP,
    INDEX idx_short_code (short_code)
);
```

**4. Short Code Generation:**

Option A: Base62 encoding of auto-increment ID
- Pros: Simple, guaranteed unique
- Cons: Predictable, single point of failure

Option B: Random string generation
- Pros: Unpredictable
- Cons: Need collision checking

Option C: Pre-generated key service
- Pros: Fast, no collision checking needed
- Cons: Additional service to maintain

**5. Architecture:**

```
                         ┌─────────────┐
         ┌──────────────►│    Cache    │
         │               │   (Redis)   │
         │               └─────────────┘
         │                      │
┌────────┴───────┐              │ cache miss
│  API Server    │◄─────────────┘
└────────┬───────┘
         │
         ▼
┌─────────────────┐
│    Database     │
│    (MySQL)      │
└─────────────────┘
```

**6. Read Flow:**
1. User requests short.ly/abc123
2. Check Redis cache for short_code
3. If hit, redirect to long_url
4. If miss, query database
5. Store in cache, redirect

**7. Write Flow:**
1. Receive long URL
2. Generate short code
3. Store in database
4. Return short URL

---

### Problem 2: Design a Rate Limiter

#### Requirements:
- Limit API requests per user
- Support different limits for different APIs
- Return proper error when limit exceeded

#### Solution:

**1. Requirements Clarified:**
- 100 requests per minute per user
- Different limits for different endpoints
- Distributed system (multiple servers)

**2. Algorithm Options:**

**Token Bucket (Recommended for interviews):**
```
- Bucket has max capacity (e.g., 100 tokens)
- Tokens added at fixed rate (e.g., 100/minute)
- Each request consumes 1 token
- Request denied if no tokens available
```

**Sliding Window:**
```
- Track timestamps of recent requests
- Count requests in last N seconds
- Allow if count < limit
```

**3. Redis Implementation (Token Bucket):**

```python
def is_allowed(user_id, limit=100, window=60):
    key = f"rate_limit:{user_id}"
    current = redis.get(key)
    
    if current is None:
        redis.setex(key, window, 1)
        return True
    
    if int(current) < limit:
        redis.incr(key)
        return True
    
    return False
```

**4. Redis Implementation (Sliding Window Log):**

```python
def is_allowed(user_id, limit=100, window=60):
    key = f"rate_limit:{user_id}"
    now = time.time()
    window_start = now - window
    
    # Remove old entries
    redis.zremrangebyscore(key, 0, window_start)
    
    # Count current window
    count = redis.zcard(key)
    
    if count < limit:
        redis.zadd(key, {str(now): now})
        redis.expire(key, window)
        return True
    
    return False
```

**5. Architecture:**

```
┌─────────┐     ┌─────────────┐     ┌──────────────┐
│ Client  │────►│Rate Limiter │────►│  API Server  │
└─────────┘     │ Middleware  │     └──────────────┘
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │    Redis    │
                │  (Shared)   │
                └─────────────┘
```

**6. Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000

If exceeded:
HTTP 429 Too Many Requests
Retry-After: 30
```

---

### Problem 3: Design a Notification System

#### Requirements:
- Send notifications via Email, SMS, Push
- Handle millions of notifications daily
- Retry failed notifications
- User preferences (opt-out)

#### Solution:

**1. API Design:**

```
POST /api/v1/notifications
{
  "user_id": "123",
  "type": "order_shipped",
  "channels": ["email", "push"],
  "data": {
    "order_id": "456",
    "tracking_number": "ABC123"
  }
}

GET /api/v1/users/{id}/preferences
{
  "email": true,
  "sms": false,
  "push": true,
  "quiet_hours": { "start": "22:00", "end": "08:00" }
}
```

**2. Database Schema:**

```sql
CREATE TABLE notifications (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id     BIGINT NOT NULL,
    type        VARCHAR(50) NOT NULL,
    channel     ENUM('email', 'sms', 'push') NOT NULL,
    status      ENUM('pending', 'sent', 'failed') DEFAULT 'pending',
    content     JSON NOT NULL,
    retry_count INT DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at     TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_status (status)
);

CREATE TABLE user_preferences (
    user_id         BIGINT PRIMARY KEY,
    email_enabled   BOOLEAN DEFAULT TRUE,
    sms_enabled     BOOLEAN DEFAULT TRUE,
    push_enabled    BOOLEAN DEFAULT TRUE,
    quiet_start     TIME,
    quiet_end       TIME
);
```

**3. Architecture:**

```
┌──────────────┐
│ API Server   │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌─────────────────┐
│Notification  │────►│  Message Queue  │
│  Service     │     │   (Kafka/SQS)   │
└──────────────┘     └────────┬────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Email Worker  │    │  SMS Worker   │    │ Push Worker   │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        ▼                    ▼                    ▼
   SendGrid/SES         Twilio            Firebase/APNs
```

**4. Flow:**
1. Service receives notification request
2. Check user preferences
3. Create notification records for enabled channels
4. Push to respective message queues
5. Workers consume and send via third-party services
6. Update status, retry on failure

**5. Key Considerations:**
- **Retry logic:** Exponential backoff (1s, 2s, 4s, 8s...)
- **Dead letter queue:** For notifications that fail after max retries
- **Rate limiting:** Don't spam users
- **Templates:** Store notification templates separately

---

### Problem 4: Design a Simple Chat System (1-on-1)

#### Requirements:
- Send messages between two users
- Show online/offline status
- Message delivery status (sent, delivered, read)
- Message history

#### Solution:

**1. API Design:**

```
WebSocket: /ws/chat

Send message:
{
  "type": "message",
  "to": "user456",
  "content": "Hello!",
  "message_id": "uuid"
}

Receive message:
{
  "type": "message",
  "from": "user123",
  "content": "Hello!",
  "message_id": "uuid",
  "timestamp": "2024-01-15T10:30:00Z"
}

REST APIs:
GET /api/v1/conversations                    → List conversations
GET /api/v1/conversations/{id}/messages      → Get message history
POST /api/v1/messages/{id}/read              → Mark as read
```

**2. Database Schema:**

```sql
CREATE TABLE conversations (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_1   BIGINT NOT NULL,
    participant_2   BIGINT NOT NULL,
    last_message_at TIMESTAMP,
    UNIQUE KEY unique_participants (participant_1, participant_2)
);

CREATE TABLE messages (
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    conversation_id BIGINT NOT NULL,
    sender_id       BIGINT NOT NULL,
    content         TEXT NOT NULL,
    status          ENUM('sent', 'delivered', 'read') DEFAULT 'sent',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_conversation (conversation_id, created_at)
);

-- Online status in Redis
-- Key: online:user123, Value: server_id, TTL: 30 seconds
```

**3. Architecture:**

```
┌──────────┐                              ┌──────────┐
│  User A  │◄────── WebSocket ──────────► │  User B  │
└────┬─────┘                              └────┬─────┘
     │                                         │
     └──────────────┬─────────────────────────┘
                    │
             ┌──────▼──────┐
             │   Gateway   │
             │  (WebSocket)│
             └──────┬──────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
┌────▼────┐   ┌─────▼─────┐  ┌─────▼─────┐
│ Chat    │   │  Session  │  │  Message  │
│ Server 1│   │  Service  │  │  Queue    │
└────┬────┘   └───────────┘  └───────────┘
     │
┌────▼────┐
│Database │
│+ Redis  │
└─────────┘
```

**4. Message Flow:**
1. User A sends message via WebSocket
2. Server validates and stores in database
3. Check if User B is online (Redis)
4. If online: Push via WebSocket
5. If offline: Store for later delivery
6. Update delivery status

**5. Online Status:**
- User connects: Set Redis key with TTL
- Heartbeat every 20s: Refresh TTL
- User disconnects: Key expires

---

## Mistakes to Avoid

### 1. Jumping Into Solution Too Quickly

**Wrong:**
> "For a URL shortener, I'll use MySQL with a urls table and generate random strings..."

**Right:**
> "Before I design, let me understand the requirements. How many URLs per day? Do we need analytics? Should URLs expire?"

---

### 2. Not Drawing Diagrams

**Wrong:** Explaining everything verbally without visual representation

**Right:** Draw boxes and arrows showing:
- Client → Load Balancer → Servers → Database
- Data flow between components
- Where caching happens

---

### 3. Over-Engineering for 2 YOE Level

**Wrong:**
> "We'll use Kafka for message streaming, implement CQRS pattern, use Cassandra for writes and Elasticsearch for reads, implement saga pattern for distributed transactions..."

**Right:**
> "For this scale, I'd start with a simple architecture: Load balancer, a few application servers, MySQL database, and Redis for caching. We can add complexity as we scale."

---

### 4. Ignoring Trade-offs

**Wrong:**
> "We'll use Redis for everything because it's fast."

**Right:**
> "Redis is great for caching and session storage because of its speed, but it stores data in memory which is expensive. For persistent data like user accounts, I'd use MySQL for durability and ACID compliance."

---

### 5. Not Considering Failure Scenarios

**Wrong:** Assuming everything works perfectly

**Right:**
> "What happens if the database goes down? We should have read replicas for redundancy. What if a server crashes mid-request? We need idempotent operations to safely retry."

---

### 6. Forgetting About Data Size

**Wrong:** Not considering how much data you're storing

**Right:**
> "If we have 100M URLs and each record is ~500 bytes, that's 50GB of data. This fits on a single database server, but we should plan for sharding if we grow 10x."

---

### 7. Not Explaining Your Thought Process

**Wrong:** Silently thinking and then presenting a solution

**Right:**
> "I'm thinking about whether to use SQL or NoSQL here. Since we need transactions for order processing and the data is well-structured, I'll go with MySQL. Does that make sense?"

---

### 8. Memorizing Solutions Without Understanding

**Wrong:** Reciting a memorized URL shortener design

**Right:** Understanding WHY each component is there so you can adapt to different requirements or follow-up questions

---

## Quick Reference Cheat Sheet

### Database Selection

| Use Case | Database | Reason |
|----------|----------|--------|
| User data | PostgreSQL/MySQL | ACID, relationships |
| Sessions | Redis | Fast, TTL support |
| Product catalog | PostgreSQL | Complex queries |
| Chat messages | MongoDB/Cassandra | High write volume |
| Search | Elasticsearch | Full-text search |
| Analytics | ClickHouse/BigQuery | Column-oriented |

### Caching Patterns

| Pattern | Use When |
|---------|----------|
| Cache-aside | Read-heavy, can tolerate stale data |
| Write-through | Need consistency |
| Write-behind | High write volume, async OK |

### Scaling Checklist

1. [ ] Add caching layer (Redis)
2. [ ] Use CDN for static assets
3. [ ] Add read replicas for database
4. [ ] Make services stateless
5. [ ] Add load balancer
6. [ ] Consider database sharding
7. [ ] Use message queues for async tasks

### Common Estimations

| Metric | Value |
|--------|-------|
| Daily active users | Given or estimate |
| Requests per user per day | 10-50 typical |
| Peak to average ratio | 3-5x |
| Storage per record | 100B - 1KB typical |
| Cache hit ratio target | 80-95% |

### Interview Time Management (45 min)

| Phase | Time | Activities |
|-------|------|------------|
| Requirements | 5 min | Ask questions, clarify scope |
| API Design | 5 min | Define main endpoints |
| Data Model | 5 min | Design schema |
| High-level Design | 15 min | Draw architecture, explain flow |
| Deep Dive | 10 min | Discuss trade-offs, optimizations |
| Q&A | 5 min | Answer interviewer questions |

---

## Additional Resources

### Recommended Practice Order

1. URL Shortener (warm-up)
2. Pastebin (similar pattern)
3. Rate Limiter (introduces distributed concepts)
4. Notification System (async processing)
5. Chat Application (real-time systems)

### Key Topics Summary for 2 YOE

**Must Know:**
- REST API design
- SQL database design
- Caching basics (Redis)
- Load balancing concepts
- Horizontal vs vertical scaling

**Good to Know:**
- Message queues
- Database replication
- CAP theorem basics
- Consistent hashing concepts

**Nice to Have:**
- Database sharding
- Microservices patterns
- Event-driven architecture

---

## Final Tips

1. **Practice out loud** - System design is about communication
2. **Use a whiteboard/paper** - Draw your designs
3. **Start simple** - Add complexity only when needed
4. **Be honest** - Say "I'm not sure, but I think..." if uncertain
5. **Ask for feedback** - "Does this approach make sense?"
6. **Think about the user** - How does this affect user experience?

Good luck with your interviews! Remember, at 2 YOE, interviewers want to see your thought process and potential, not perfection.
