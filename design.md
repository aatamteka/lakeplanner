# Design Document
## Introduction 
This document describes the design of the boating trip management platform described in the requirements.md. This platform shall consist of microservices responsible for third party API interactions, persistence, user management, user communication, and the UI itself. Each of these components shall be implemented as microservices that integrate using RESTful APIs and a message bus. All REST APIs shall expose a swagger documentation UI.

### Third party APIs
All of the third party APIs shall be abstracted by one or more services, as logically make sense to separate, except for the user communication API interactions (email, SMS, etc) which are handled by a separate service.
#### Weather service
The platform shall use the NOAA API, https://api.weather.gov/points/{lat},{lon}, to obtain forecasts for each lake

### Persistence
All user, forecast, lake metadata, and audit information shall be stored by a Postgres database through a microservice that exposes RESTful APIs as well as implements an observer on the message bus to record certain events.

### User Communication
Users shall be able to elect to reeive emails or SMSs for meetup and schedule suggestions as well as weather alerts. These notifications shall be handled by a microservice that integrates with an email service tracking delivery success/failure, open rates, etc, and an SMS provier such as twilio.

### UI
The end user UI shall enforce good security patterns for user credential management and API authentication/interactions with backend APIs.

### Amenity Contention Coordination Service
A critical requirement is minimizing contention for lake amenities (rope swings, picnic areas, fishing spots, etc.) among users. This service shall implement an intelligent scheduling algorithm that:

#### Core Functionality
1. **Temporal Distribution**: Analyzes planned outings across time slots to identify potential overcrowding at specific amenities
2. **Load Balancing**: Distributes user groups across available amenities based on their preferences and amenity capacity
3. **Dynamic Scoring**: Calculates contention scores for each amenity at each time slot based on:
   - Number of groups planning to visit
   - Amenity capacity/size (from GIS metadata)
   - Historical usage patterns
   - Duration of typical visits

#### Algorithm Design
The service shall use a constraint satisfaction approach:
- **Soft Constraints**: User amenity preferences (can be adjusted)
- **Hard Constraints**: Time availability, weather conditions, rental availability
- **Optimization Goal**: Minimize maximum contention across all amenities while maximizing user satisfaction

#### Integration Points
- Receives schedule requests from recommendation engine
- Queries database for existing planned outings and historical data
- Returns contention-aware amenity suggestions
- Publishes amenity allocation events to message bus for analytics

#### Conflict Resolution Strategy
When multiple groups want the same amenity at the same time:
1. Calculate alternative amenities with similar characteristics
2. Suggest time shifts (earlier/later slots)
3. Present contention probability to users (low/medium/high)
4. Allow users to override with awareness of crowding

### User Management Service
Handles authentication, authorization, user profiles, and friend network management. This service shall:
- Implement secure password hashing and session management
- Manage user profile data including schedule preferences
- Handle friend connections and relationship graphs
- Provide APIs for user search and friend requests
- Integrate with OAuth providers for social login options

### Recommendation Engine
Coordinates data from multiple services to generate optimal outing suggestions. This service shall:
- Aggregate availability from user schedules
- Match overlapping friend availability
- Filter by weather preferences
- Check rental boat availability
- Request amenity contention analysis
- Rank and sort recommendations by combined score
- Cache recommendations for performance

### Message Bus Architecture
All services communicate asynchronously via message bus (RabbitMQ or Kafka) for:
- Event-driven updates (new outing created, weather alerts, friend availability changes)
- Audit logging
- Analytics data collection
- Notification triggers

Event types include:
- `outing.planned`: Triggers amenity contention recalculation
- `weather.alert`: Triggers user notifications
- `friend.available`: Triggers recommendation refresh
- `rental.booked`: Updates availability data

### Data Models

#### User
- id, username, email, password_hash
- preferred_lake_id, owns_boat, preferred_marina_id
- schedule_preferences (JSON: weekday/weekend, morning/afternoon/evening availability)
- weather_preferences (max_precipitation_prob, max_wind_speed)
- notification_preferences

#### Lake
- id, name, latitude, longitude
- GIS boundary data

#### Amenity
- id, lake_id, type (rope_swing, picnic_area, fishing_spot)
- latitude, longitude, capacity_score
- hours_of_operation, seasonal_availability

#### BoatRamp
- id, lake_id, name, latitude, longitude
- hours_of_operation, seasonal_availability

#### Marina
- id, lake_id, name, latitude, longitude
- rental_inventory (JSON array of boat types and quantities)

#### Outing
- id, user_id, lake_id, planned_date, time_slot
- target_amenities (array of amenity_ids)
- invited_friends (array of user_ids)
- rsvp_status (JSON map of user_id to status)

#### AmenityContention
- id, amenity_id, date, time_slot
- planned_groups_count, contention_score
- updated_at

### Security Considerations
- All APIs require JWT authentication
- Rate limiting on public endpoints
- Input validation and sanitization
- SQL injection prevention via parameterized queries
- HTTPS/TLS for all communications
- Secrets management via environment variables or vault
- CORS configuration for UI access

### Scalability
- Stateless services for horizontal scaling
- Database read replicas for query performance
- Redis caching for recommendations and frequent queries
- CDN for UI static assets
- Load balancers for API gateways

### Monitoring and Observability
- Centralized logging (ELK stack or similar)
- Metrics collection (Prometheus/Grafana)
- Distributed tracing (Jaeger/Zipkin)
- Health check endpoints on all services
- Alert rules for service degradation

