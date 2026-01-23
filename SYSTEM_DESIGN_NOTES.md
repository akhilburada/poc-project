# System Design Notes for 2 YOE Interviews

> Quick reference notes for interview preparation

---

## 1. API Design

### REST API Basics

| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Read data | Yes |
| POST | Create new | No |
| PUT | Replace entire resource | Yes |
| PATCH | Partial update | Yes |
| DELETE | Remove resource | Yes |

### HTTP Status Codes

```
2xx - Success
  200 OK              - Request successful
  201 Created         - Resource created
  204 No Content      - Success, no body returned

4xx - Client Error
  400 Bad Request     - Invalid request
  401 Unauthorized    - Not authenticated
  403 Forbidden       - Authenticated but not allowed
  404 Not Found       - Resource doesn't exist
  429 Too Many Requests - Rate limited

5xx - Server Error
  500 Internal Error  - Server crashed
  502 Bad Gateway     - Upstream server error
  503 Service Unavailable - Server overloaded
```

### API Design Rules

1. Use **nouns**, not verbs: `/users` not `/getUsers`
2. Use **plural** names: `/users` not `/user`
3. Use **proper nesting**: `/users/123/orders`
4. Add **versioning**: `/api/v1/users`
5. Support **pagination**: `?page=1&limit=20`
6. Use **query params** for filtering: `?status=active&sort=created_at`

### Example API Design

```
User Management:
GET    /api/v1/users              - List users
GET    /api/v1/users/:id          - Get user
POST   /api/v1/users              - Create user
PUT    /api/v1/users/:id          - Update user
DELETE /api/v1/users/:id          - Delete user

Nested Resources:
GET    /api/v1/users/:id/orders   - User's orders
POST   /api/v1/users/:id/orders   - Create order for user
```

---

## 2. Database Concepts

### SQL vs NoSQL

| SQL (Relational) | NoSQL (Non-Relational) |
|------------------|------------------------|
| Fixed schema | Flexible schema |
| ACID transactions | Eventually consistent (usually) |
| Complex joins | Simple queries |
| Vertical scaling | Horizontal scaling |
| MySQL, PostgreSQL | MongoDB, Cassandra, Redis |

### When to Use What

**Use SQL for:**
- User accounts
- Financial transactions
- Order management
- Inventory
- Any data needing ACID

**Use NoSQL for:**
- Session storage
- User activity logs
- Real-time analytics
- Chat messages
- Caching

### ACID Properties

```
A - Atomicity    : All or nothing (transaction completes fully or rolls back)
C - Consistency  : Data stays valid after transaction
I - Isolation    : Concurrent transactions don't interfere
D - Durability   : Committed data survives crashes
```

### Indexing

**What to Index:**
- Primary keys (automatic)
- Foreign keys
- Columns in WHERE clauses
- Columns in ORDER BY
- Columns in JOIN conditions

**Don't Over-Index:**
- Each index slows down writes
- Index only frequently queried columns

### Database Schema Example

```sql
-- Users
users (id, email, name, password_hash, created_at)

-- Products  
products (id, name, price, stock, category_id, created_at)

-- Orders
orders (id, user_id, total, status, created_at)

-- Order Items
order_items (id, order_id, product_id, quantity, price)
```

### Normalization Quick Guide

```
1NF: No repeating groups (each cell has single value)
2NF: 1NF + No partial dependencies (all columns depend on full primary key)
3NF: 2NF + No transitive dependencies (columns depend only on primary key)
```

**When to Denormalize:**
- Read-heavy systems
- Need faster queries
- Avoid complex joins

---

## 3. Caching

### Why Cache?

- Reduce database load
- Faster response times
- Handle traffic spikes
- Save money (fewer DB queries)

### Cache Placement

```
Client Cache → CDN → Application Cache → Database Cache → Database
     ↑          ↑           ↑                  ↑
  Browser    Static      Redis/           Query
  Storage    Assets     Memcached         Cache
```

### Caching Strategies

**1. Cache-Aside (Lazy Loading)** - Most Common
```
Read:
1. Check cache
2. If miss → query DB → store in cache
3. Return data

Write:
1. Update DB
2. Delete cache (invalidate)
```

**2. Write-Through**
```
Write:
1. Write to cache
2. Cache writes to DB
3. Return success

Pros: Data always in sync
Cons: Higher write latency
```

**3. Write-Behind (Write-Back)**
```
Write:
1. Write to cache
2. Return success immediately
3. Cache writes to DB asynchronously

Pros: Fast writes
Cons: Risk of data loss
```

### Cache Eviction Policies

```
LRU - Least Recently Used    (remove oldest accessed)
LFU - Least Frequently Used  (remove least accessed)
TTL - Time To Live           (expire after time)
FIFO - First In First Out    (remove oldest added)
```

### What to Cache

✅ **Cache:**
- Frequently read data
- Expensive computations
- Session data
- Static content
- API responses

❌ **Don't Cache:**
- Rapidly changing data
- Sensitive data (without encryption)
- Large objects (unless needed)

### Redis Commands Cheat Sheet

```bash
# String operations
SET key value
GET key
SETEX key seconds value    # Set with expiry
INCR key                   # Increment
DEL key                    # Delete

# Hash operations
HSET user:1 name "John"
HGET user:1 name
HGETALL user:1

# List operations
LPUSH mylist value         # Add to left
RPUSH mylist value         # Add to right
LRANGE mylist 0 -1         # Get all

# Set operations
SADD myset value
SMEMBERS myset
SISMEMBER myset value

# Sorted Set (for leaderboards)
ZADD leaderboard 100 "player1"
ZREVRANGE leaderboard 0 9  # Top 10

# Expiry
EXPIRE key seconds
TTL key                    # Check remaining time
```

---

## 4. Load Balancing

### Why Load Balancer?

- Distribute traffic across servers
- High availability (no single point of failure)
- Handle more traffic
- Enable zero-downtime deployments

### Load Balancing Algorithms

| Algorithm | How It Works | Use When |
|-----------|--------------|----------|
| Round Robin | Rotate through servers | Servers are equal |
| Weighted Round Robin | More requests to powerful servers | Unequal servers |
| Least Connections | Send to server with fewest active connections | Long-lived connections |
| IP Hash | Same client IP → same server | Need session affinity |
| Random | Random server selection | Simple distribution |

### Basic Architecture

```
                    Internet
                        │
                   ┌────▼────┐
                   │  Load   │
                   │Balancer │
                   └────┬────┘
         ┌──────────────┼──────────────┐
         │              │              │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │Server 1 │    │Server 2 │    │Server 3 │
    └─────────┘    └─────────┘    └─────────┘
```

### Health Checks

Load balancer checks if servers are healthy:
- **Active:** LB pings servers periodically
- **Passive:** LB monitors response errors

Unhealthy servers are removed from rotation.

---

## 5. Scaling

### Vertical vs Horizontal Scaling

| Vertical (Scale Up) | Horizontal (Scale Out) |
|---------------------|------------------------|
| Bigger server | More servers |
| More CPU, RAM, Disk | Add more machines |
| Simple | Complex |
| Has limits | No limits |
| Single point of failure | Better fault tolerance |
| More expensive at scale | Cost-effective |

### Scaling Strategy

```
Stage 1: Single Server
- Web + DB on one server
- Good for < 1000 users

Stage 2: Separate DB
- Web server + separate DB server
- Good for < 10,000 users

Stage 3: Add Caching
- Add Redis/Memcached
- Reduces DB load
- Good for < 100,000 users

Stage 4: Multiple Web Servers
- Add load balancer
- Multiple app servers
- Good for < 1,000,000 users

Stage 5: Database Scaling
- Read replicas
- Database sharding
- Good for millions of users
```

### Stateless vs Stateful Services

**Stateful (Bad for scaling):**
```
User logs into Server 1
Session stored on Server 1
Next request goes to Server 2
User appears logged out! ❌
```

**Stateless (Good for scaling):**
```
User logs into Server 1
Session stored in Redis
Next request goes to Server 2
Server 2 reads session from Redis ✓
```

**Rule:** Store session/state in shared cache (Redis), not on application servers.

---

## 6. Database Scaling

### Read Replicas

```
         Write
           │
    ┌──────▼──────┐
    │   Primary   │
    │  (Master)   │
    └──────┬──────┘
           │ Replication
    ┌──────┴──────┐
    │             │
┌───▼───┐    ┌────▼───┐
│Replica│    │Replica │
│  (R)  │    │  (R)   │
└───────┘    └────────┘
   Read        Read
```

- All writes go to Primary
- Reads distributed across Replicas
- Good for read-heavy systems (90% reads)

### Database Sharding

Split data across multiple databases:

```
User ID 1-1M    → Shard 1
User ID 1M-2M   → Shard 2
User ID 2M-3M   → Shard 3
```

**Sharding Strategies:**

| Strategy | How | Example |
|----------|-----|---------|
| Range | By range of values | User ID 1-1M, 1M-2M |
| Hash | Hash of key | user_id % num_shards |
| Geographic | By location | US, EU, Asia |
| Directory | Lookup table | Map key to shard |

**Sharding Challenges:**
- Joins across shards are hard
- Rebalancing is complex
- Some queries need to hit all shards

---

## 7. Message Queues

### Why Use Queues?

- Decouple services
- Handle async tasks
- Buffer during traffic spikes
- Retry failed operations
- Improve response time

### When to Use

✅ **Use for:**
- Sending emails/SMS
- Image/video processing
- Report generation
- Third-party API calls
- Notifications

❌ **Don't use for:**
- Real-time responses needed
- Simple synchronous operations

### Queue Architecture

```
┌──────────┐     ┌───────────┐     ┌──────────┐
│ Producer │────►│   Queue   │────►│ Consumer │
│(API Server)    │(RabbitMQ/ │     │(Worker)  │
└──────────┘     │  Kafka)   │     └──────────┘
                 └───────────┘
```

### Common Patterns

**1. Task Queue**
```
Web Server → Queue → Worker
(fast response)  (process async)
```

**2. Pub/Sub**
```
Publisher → Topic → Subscriber 1
                 → Subscriber 2
                 → Subscriber 3
```

### Popular Message Queues

| Queue | Best For |
|-------|----------|
| RabbitMQ | General purpose, complex routing |
| Kafka | High throughput, event streaming |
| AWS SQS | Simple, managed, AWS integration |
| Redis | Simple queues, already using Redis |

---

## 8. System Design Patterns

### Microservices vs Monolith

**Monolith:**
```
┌─────────────────────────────┐
│      Single Application     │
│  ┌─────┐ ┌─────┐ ┌─────┐   │
│  │User │ │Order│ │Pay  │   │
│  └─────┘ └─────┘ └─────┘   │
└─────────────────────────────┘
```
- Simpler to develop initially
- Single deployment
- Good for small teams

**Microservices:**
```
┌─────────┐  ┌─────────┐  ┌─────────┐
│User Svc │  │Order Svc│  │Pay Svc  │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  │
            API Gateway
```
- Independent scaling
- Technology flexibility
- Complex to manage

### API Gateway

```
Client → API Gateway → Service A
                    → Service B
                    → Service C

Responsibilities:
- Authentication
- Rate limiting
- Request routing
- Response aggregation
- SSL termination
```

### CDN (Content Delivery Network)

```
User (India) ──► CDN Edge (India) ──► Origin (US)
                 (Fast, cached)       (Slow, far)
```

**Use CDN for:**
- Static files (JS, CSS, images)
- Videos
- Documents
- Any content that doesn't change often

---

## 9. CAP Theorem

**You can only have 2 of 3:**

```
C - Consistency  : All nodes see same data
A - Availability : System always responds
P - Partition Tolerance : Works despite network failures
```

**In distributed systems, P is mandatory** (networks fail), so you choose between:

- **CP:** Consistent but may be unavailable (banking)
- **AP:** Available but may be inconsistent (social media)

### Consistency Models

| Model | Description | Example |
|-------|-------------|---------|
| Strong | All reads see latest write | Banking |
| Eventual | Will be consistent eventually | Social media likes |
| Read-your-writes | You see your own writes | Shopping cart |

---

## 10. Numbers to Remember

### Latency

```
L1 cache reference         :      0.5 ns
L2 cache reference         :        7 ns
RAM reference              :      100 ns
SSD random read            :      150 μs
HDD random read            :       10 ms
Network (same datacenter)  :      500 μs
Network (cross-continent)  :      150 ms
```

### Storage

```
1 Byte     = 8 bits
1 KB       = 1,000 bytes
1 MB       = 1,000 KB
1 GB       = 1,000 MB
1 TB       = 1,000 GB

Character  = 1-4 bytes (UTF-8)
Integer    = 4 bytes
Long       = 8 bytes
UUID       = 16 bytes
Timestamp  = 8 bytes
```

### Time

```
1 minute  = 60 seconds
1 hour    = 3,600 seconds
1 day     = 86,400 seconds ≈ 100,000 seconds
1 month   = 2.5 million seconds
1 year    = 30 million seconds
```

### Traffic Estimates

```
1 million requests/day = ~12 requests/second
100 million requests/day = ~1,200 requests/second

Formula: requests_per_day / 86400 = requests_per_second
```

---

## 11. Interview Framework (RADIO)

### R - Requirements (3-5 min)

**Ask:**
- What are the core features?
- Who are the users?
- What's the expected scale?
- Read-heavy or write-heavy?
- Latency requirements?
- Any specific constraints?

### A - API Design (3-5 min)

Define main endpoints:
```
POST /api/v1/resource    - Create
GET  /api/v1/resource    - List
GET  /api/v1/resource/id - Get one
PUT  /api/v1/resource/id - Update
DELETE /api/v1/resource/id - Delete
```

### D - Data Model (5 min)

Design database schema:
```sql
CREATE TABLE resource (
    id          BIGINT PRIMARY KEY,
    field1      VARCHAR(255),
    field2      INT,
    created_at  TIMESTAMP,
    INDEX idx_field1 (field1)
);
```

### I - High-Level Design (10-15 min)

Draw architecture:
```
Client → LB → App Servers → Cache → Database
                         → Queue → Workers
```

### O - Optimizations (10 min)

Discuss:
- Caching strategy
- Database scaling
- Failure handling
- Monitoring
- Security

---

## 12. Common Interview Questions

### Tier 1 (Most Common for 2 YOE)

1. **URL Shortener** - Generate short URLs, redirect
2. **Rate Limiter** - Limit API requests per user
3. **Notification System** - Send email/SMS/push
4. **Pastebin** - Share text snippets
5. **Key-Value Store** - Simple storage

### Tier 2 (Sometimes Asked)

6. **Chat Application** - 1-on-1 messaging
7. **News Feed** - Show posts from friends
8. **File Storage** - Upload/download files
9. **Booking System** - Reserve seats/appointments
10. **Leaderboard** - Real-time rankings

---

## 13. Quick Design Templates

### URL Shortener

```
Components:
- API Server (generate/redirect)
- Database (store mappings)
- Cache (hot URLs)
- Key Generator (unique codes)

Flow:
Create: long_url → generate code → store → return short_url
Read: short_code → check cache → check DB → redirect

Database:
urls (short_code, long_url, user_id, created_at, expires_at)
```

### Rate Limiter

```
Components:
- Middleware (check limits)
- Redis (store counters)

Algorithms:
1. Token Bucket - tokens refill at fixed rate
2. Sliding Window - count requests in time window

Redis:
SET user:123:requests 1 EX 60
INCR user:123:requests
```

### Notification System

```
Components:
- API Server (receive requests)
- Queue (buffer notifications)
- Workers (send via channels)
- Third-party (SendGrid, Twilio, Firebase)

Flow:
Request → Check preferences → Queue → Worker → Send

Channels:
- Email (SendGrid, SES)
- SMS (Twilio)
- Push (Firebase, APNs)
```

### Chat Application

```
Components:
- WebSocket Server (real-time)
- Message Queue (delivery)
- Database (history)
- Redis (online status)

Flow:
User A → WebSocket → Server → Check if B online
                            → If yes: WebSocket to B
                            → If no: Store for later

Database:
messages (id, conversation_id, sender_id, content, status, created_at)
```

---

## 14. Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Jump to solution immediately | Ask clarifying questions first |
| No diagrams | Always draw architecture |
| Over-engineer for small scale | Start simple, add complexity as needed |
| Ignore trade-offs | Discuss pros/cons of each decision |
| Forget about failures | Consider what happens when things break |
| Silent thinking | Talk through your thought process |
| Memorize without understanding | Understand WHY each component is needed |
| Ignore data size | Estimate storage and calculate if it fits |

---

## 15. Final Checklist Before Interview

- [ ] Can explain REST API design
- [ ] Know SQL vs NoSQL differences
- [ ] Understand caching strategies
- [ ] Can draw load-balanced architecture
- [ ] Know horizontal vs vertical scaling
- [ ] Understand message queues
- [ ] Can do back-of-envelope calculations
- [ ] Practiced URL Shortener design
- [ ] Practiced Rate Limiter design
- [ ] Know the RADIO framework
- [ ] Can explain trade-offs

---

## Quick Revision Card

```
┌────────────────────────────────────────────────────────┐
│                  SYSTEM DESIGN FLOW                    │
├────────────────────────────────────────────────────────┤
│ 1. REQUIREMENTS                                        │
│    - Functional: What features?                        │
│    - Non-functional: Scale? Latency? Availability?     │
│                                                        │
│ 2. API DESIGN                                          │
│    - REST endpoints                                    │
│    - Request/Response format                           │
│                                                        │
│ 3. DATA MODEL                                          │
│    - Tables and relationships                          │
│    - SQL vs NoSQL decision                             │
│    - Indexes                                           │
│                                                        │
│ 4. HIGH-LEVEL DESIGN                                   │
│    - Draw: Client → LB → Servers → Cache → DB          │
│    - Add queues if async needed                        │
│                                                        │
│ 5. DEEP DIVE                                           │
│    - Caching strategy                                  │
│    - Scaling approach                                  │
│    - Failure handling                                  │
└────────────────────────────────────────────────────────┘
```

---

*Good luck with your interviews!*
